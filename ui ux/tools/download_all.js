const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// Directories to create
const DIRS = {
  js: path.join(__dirname, 'assets', 'js'),
  css: path.join(__dirname, 'assets', 'css'),
  fonts: path.join(__dirname, 'assets', 'fonts'),
  images: path.join(__dirname, 'assets', 'images'),
  videos: path.join(__dirname, 'assets', 'videos'),
  data: path.join(__dirname, 'assets', 'data'),
  icons: path.join(__dirname, 'assets', 'icons'),
};

for (const d of Object.values(DIRS)) {
  fs.mkdirSync(d, { recursive: true });
}

// Map original URLs to local relative paths
const urlToLocalMap = new Map();
const downloadedUrls = new Set();
const failedUrls = [];
const queue = new Set();

// Helper to determine asset category and clean filename
function categorizeUrl(rawUrl) {
  const urlObj = new URL(rawUrl);
  const cleanPath = urlObj.pathname;
  let filename = path.basename(cleanPath);
  let ext = path.extname(cleanPath).toLowerCase();

  // If no extension or query-based
  if (!ext || ext === '.com') {
    if (rawUrl.includes('searchIndex')) ext = '.json';
    else if (rawUrl.includes('embeds/')) ext = '.js';
    else if (rawUrl.includes('/script?')) ext = '.js';
    else ext = '.bin';
  }

  // Sanitize filename
  filename = filename.replace(/[^a-zA-Z0-9_\-\.]/g, '_');
  if (!filename || filename === '.' || filename === '_') {
    filename = 'asset_' + Math.abs(hashCode(rawUrl));
  }
  if (!filename.toLowerCase().endsWith(ext)) {
    filename += ext;
  }

  // Favicons and icons
  if (cleanPath.includes('/icons/') || filename.includes('favicon') || filename.includes('touch-icon')) {
    return { dir: DIRS.icons, relPath: './assets/icons/' + filename, filename };
  }

  // JS & MJS
  if (ext === '.mjs' || ext === '.js') {
    return { dir: DIRS.js, relPath: './assets/js/' + filename, filename };
  }

  // Fonts
  if (['.woff2', '.woff', '.ttf', '.otf', '.eot'].includes(ext)) {
    return { dir: DIRS.fonts, relPath: './assets/fonts/' + filename, filename };
  }

  // Images
  if (['.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif', '.ico', '.avif'].includes(ext)) {
    return { dir: DIRS.images, relPath: './assets/images/' + filename, filename };
  }

  // Videos
  if (['.mp4', '.webm', '.ogg', '.mov'].includes(ext)) {
    return { dir: DIRS.videos, relPath: './assets/videos/' + filename, filename };
  }

  // JSON
  if (ext === '.json') {
    return { dir: DIRS.data, relPath: './assets/data/' + filename, filename };
  }

  // CSS
  if (ext === '.css') {
    return { dir: DIRS.css, relPath: './assets/css/' + filename, filename };
  }

  return { dir: DIRS.data, relPath: './assets/data/' + filename, filename };
}

function hashCode(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0;
  }
  return hash;
}

// Download function with retries and redirect support
function downloadFile(targetUrl, localFilePath) {
  return new Promise((resolve, reject) => {
    function tryFetch(currentUrl, redirectCount = 0) {
      if (redirectCount > 5) {
        return reject(new Error('Too many redirects: ' + currentUrl));
      }

      const client = currentUrl.startsWith('https') ? https : http;
      const req = client.get(currentUrl, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
          'Accept': '*/*',
          'Referer': 'https://nehayadav.framer.website/'
        }
      }, (res) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          const nextUrl = new URL(res.headers.location, currentUrl).href;
          res.resume();
          return tryFetch(nextUrl, redirectCount + 1);
        }

        if (res.statusCode !== 200) {
          res.resume();
          return reject(new Error(`HTTP ${res.statusCode} for ${currentUrl}`));
        }

        const fileStream = fs.createWriteStream(localFilePath);
        res.pipe(fileStream);

        fileStream.on('finish', () => {
          fileStream.close(() => resolve({ size: fs.statSync(localFilePath).size, contentType: res.headers['content-type'] }));
        });

        fileStream.on('error', (err) => {
          fs.unlink(localFilePath, () => {});
          reject(err);
        });
      });

      req.on('error', (err) => reject(err));
      req.setTimeout(25000, () => {
        req.destroy();
        reject(new Error('Timeout downloading ' + currentUrl));
      });
    }

    tryFetch(targetUrl);
  });
}

// Scan JS/MJS code for imports and asset URLs
function extractUrlsFromCode(content, baseUrl) {
  const urls = [];
  // Match standard imports/exports: import ... from "..." or export ... from "..."
  const importRe = /(?:import|from)\s+['"]([^'"]+)['"]/g;
  let m;
  while ((m = importRe.exec(content)) !== null) {
    urls.push(m[1]);
  }
  // Match dynamic imports: import("...")
  const dynImportRe = /import\s*\(\s*['"]([^'"]+)['"]\s*\)/g;
  while ((m = dynImportRe.exec(content)) !== null) {
    urls.push(m[1]);
  }
  // Match framerusercontent URLs
  const framerRe = /https:\/\/[a-zA-Z0-9_\-\.]*framerusercontent\.com[^\s"'<>\)]+/g;
  while ((m = framerRe.exec(content)) !== null) {
    urls.push(m[0]);
  }
  // Match fontshare / google fonts
  const fontRe = /https:\/\/(?:fonts\.gstatic\.com|api\.fontshare\.com)[^\s"'<>\)]+/g;
  while ((m = fontRe.exec(content)) !== null) {
    urls.push(m[0]);
  }

  const resolved = [];
  for (let u of urls) {
    u = u.replace(/[\"',;\)]+$/, '');
    if (u.startsWith('http://') || u.startsWith('https://')) {
      resolved.push(u);
    } else if (u.startsWith('./') || u.startsWith('../')) {
      if (baseUrl) {
        try {
          resolved.push(new URL(u, baseUrl).href);
        } catch (e) {}
      }
    }
  }
  return resolved;
}

// Scan CSS code for url(...) declarations
function extractUrlsFromCss(cssContent) {
  const urls = [];
  const re = /url\(\s*['"]?([^'")]+)['"]?\s*\)/g;
  let m;
  while ((m = re.exec(cssContent)) !== null) {
    let u = m[1].trim();
    if (u.startsWith('http://') || u.startsWith('https://')) {
      urls.push(u);
    }
  }
  return urls;
}

async function main() {
  console.log('=== Starting Complete Framer Asset Downloader ===\n');

  // Load URLs from captured network and HTML
  const captured = JSON.parse(fs.readFileSync('captured_network_urls.json', 'utf8'));
  const urlsJson = JSON.parse(fs.readFileSync('urls.json', 'utf8'));

  for (const u of captured.urls) queue.add(u);
  for (const u of urlsJson.all) queue.add(u);
  for (const u of urlsJson.framer) queue.add(u);

  // Add sitemap and robots
  queue.add('https://nehayadav.framer.website/robots.txt');
  queue.add('https://nehayadav.framer.website/sitemap.xml');

  // Add known search indexes from meta tags
  queue.add('https://nehayadav.framer.website/searchIndex-Pph9ovAqGYTK.json');
  queue.add('https://nehayadav.framer.website/searchIndex-OdBZhYOcqiBp.json');

  console.log(`Initial download queue size: ${queue.size} URLs\n`);

  const manifest = {};
  const processedUrls = new Set();

  while (queue.size > 0) {
    const urlList = Array.from(queue);
    queue.clear();

    for (const rawUrl of urlList) {
      if (processedUrls.has(rawUrl)) continue;
      processedUrls.add(rawUrl);

      // Skip external domains that are links, not assets
      if (
        rawUrl.startsWith('https://drive.google.com') ||
        rawUrl.startsWith('https://www.figma.com') ||
        rawUrl.startsWith('https://www.linkedin.com') ||
        rawUrl.startsWith('https://mydesignproject.framer.website') ||
        rawUrl.startsWith('https://www.framer.com') && !rawUrl.includes('/m/') && !rawUrl.includes('/edit/') ||
        rawUrl.startsWith('https://player.vimeo.com') ||
        rawUrl.startsWith('https://www.clarity.ms') ||
        rawUrl.startsWith('https://a.clarity.ms') ||
        rawUrl.startsWith('http://www.w3.org') ||
        rawUrl.startsWith('mailto:') ||
        rawUrl.startsWith('#') ||
        rawUrl === 'https://fonts.gstatic.com' ||
        rawUrl.startsWith('https://events.framer.com/anonymous')
      ) {
        continue;
      }

      // If it is the main website pages
      if (rawUrl === 'https://nehayadav.framer.website/' || rawUrl === 'https://nehayadav.framer.website') {
        continue;
      }
      if (rawUrl === 'https://nehayadav.framer.website/about' || rawUrl === 'https://nehayadav.framer.website/about/') {
        continue;
      }

      const { dir, relPath, filename } = categorizeUrl(rawUrl);
      const targetPath = path.join(dir, filename);

      urlToLocalMap.set(rawUrl, relPath);

      // If already downloaded
      if (fs.existsSync(targetPath) && fs.statSync(targetPath).size > 0) {
        manifest[rawUrl] = {
          localPath: relPath,
          size: fs.statSync(targetPath).size,
          status: 'cached'
        };
        downloadedUrls.add(rawUrl);
        continue;
      }

      process.stdout.write(`Downloading: ${rawUrl.substring(0, 80)}... `);
      try {
        const info = await downloadFile(rawUrl, targetPath);
        process.stdout.write(`OK (${(info.size / 1024).toFixed(1)} KB)\n`);
        downloadedUrls.add(rawUrl);
        manifest[rawUrl] = {
          localPath: relPath,
          size: info.size,
          contentType: info.contentType,
          status: 'success'
        };

        // If JS/MJS or CSS, recursively scan for additional assets
        const ext = path.extname(targetPath).toLowerCase();
        if (ext === '.mjs' || ext === '.js') {
          const content = fs.readFileSync(targetPath, 'utf8');
          const found = extractUrlsFromCode(content, rawUrl);
          for (const newUrl of found) {
            if (!processedUrls.has(newUrl)) {
              queue.add(newUrl);
            }
          }
        } else if (ext === '.css') {
          const content = fs.readFileSync(targetPath, 'utf8');
          const found = extractUrlsFromCss(content);
          for (const newUrl of found) {
            if (!processedUrls.has(newUrl)) {
              queue.add(newUrl);
            }
          }
        }
      } catch (err) {
        process.stdout.write(`FAILED (${err.message})\n`);
        failedUrls.push({ url: rawUrl, error: err.message });
      }
    }
  }

  console.log(`\n=== Download Phase Complete ===`);
  console.log(`Successfully downloaded: ${downloadedUrls.size} assets`);
  console.log(`Failed: ${failedUrls.length}`);

  // Save manifest
  fs.writeFileSync('assets_manifest.json', JSON.stringify({
    downloadedCount: downloadedUrls.size,
    failedCount: failedUrls.length,
    manifest,
    failed: failedUrls
  }, null, 2));

  // Now process index.html and about.html
  console.log('\n=== Rewriting HTML with Local Asset Links ===');

  function processHtml(sourceHtmlFile, outputHtmlFile) {
    let html = fs.readFileSync(sourceHtmlFile, 'utf8');

    // Replace all known original URLs with local relative paths
    // Sort keys by descending length so substrings aren't replaced prematurely
    const sortedUrls = Array.from(urlToLocalMap.entries()).sort((a, b) => b[0].length - a[0].length);

    for (const [origUrl, localRel] of sortedUrls) {
      if (html.includes(origUrl)) {
        html = html.split(origUrl).join(localRel);
      }
      // Also check URL without query string
      const cleanUrl = origUrl.split('?')[0];
      if (cleanUrl !== origUrl && html.includes(cleanUrl)) {
        html = html.split(cleanUrl).join(localRel);
      }
    }

    // Also rewrite internal navigation links:
    // https://nehayadav.framer.website/about -> ./about.html
    // https://nehayadav.framer.website/ -> ./index.html
    html = html.replace(/https:\/\/nehayadav\.framer\.website\/about/g, './about.html');
    html = html.replace(/https:\/\/nehayadav\.framer\.website\//g, './index.html');
    html = html.replace(/href="\.\/about"/g, 'href="./about.html"');
    html = html.replace(/href="\.\/"/g, 'href="./index.html"');

    // Rewrite fonts.gstatic.com or fontshare if any inline
    // Extract inline font-face urls
    const inlineFontUrls = extractUrlsFromCss(html);
    for (const fUrl of inlineFontUrls) {
      if (urlToLocalMap.has(fUrl)) {
        html = html.split(fUrl).join(urlToLocalMap.get(fUrl));
      }
    }

    fs.writeFileSync(outputHtmlFile, html, 'utf8');
    console.log(`Generated rewritten: ${outputHtmlFile} (${(Buffer.byteLength(html) / 1024).toFixed(1)} KB)`);
  }

  processHtml('index_raw.html', 'index.html');
  processHtml('about_raw.html', 'about.html');

  // Copy robots.txt and sitemap.xml to root if downloaded
  for (const f of ['robots.txt', 'sitemap.xml']) {
    const local = path.join(DIRS.data, f);
    if (fs.existsSync(local)) {
      fs.copyFileSync(local, f);
      console.log(`Copied ${f} to root.`);
    }
  }

  console.log('\n=== All operations finished successfully! ===');
}

main().catch(err => {
  console.error('Fatal error in main:', err);
  process.exit(1);
});
