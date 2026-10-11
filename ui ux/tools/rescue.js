const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const manifest = JSON.parse(fs.readFileSync('assets_manifest.json', 'utf8'));
const failed = manifest.failed;

const cleanUrls = new Set();
for (const f of failed) {
  let u = f.url;
  // Match clean URL ending in extension
  const m = u.match(/(https?:\/\/[a-zA-Z0-9_\-\.\/]+?\.(?:woff2|woff|ttf|png|jpg|jpeg|webp|svg|gif|mp4|webm|mjs|js|json|css))/i);
  if (m) {
    cleanUrls.add(m[1]);
  }
}

console.log('Clean URLs to download:', cleanUrls.size);
for (const u of cleanUrls) console.log(' -', u);

function downloadFile(targetUrl, localFilePath) {
  return new Promise((resolve, reject) => {
    function tryFetch(currentUrl, redirectCount = 0) {
      if (redirectCount > 5) return reject(new Error('Too many redirects'));

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
          return reject(new Error(`HTTP ${res.statusCode}`));
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
        reject(new Error('Timeout'));
      });
    }
    tryFetch(targetUrl);
  });
}

async function run() {
  for (const rawUrl of cleanUrls) {
    const urlObj = new URL(rawUrl);
    const filename = path.basename(urlObj.pathname);
    const ext = path.extname(filename).toLowerCase();
    let folder = 'data';
    if (ext === '.woff2' || ext === '.woff' || ext === '.ttf') folder = 'fonts';
    else if (['.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif'].includes(ext)) folder = 'images';
    else if (['.mp4', '.webm'].includes(ext)) folder = 'videos';
    else if (['.mjs', '.js'].includes(ext)) folder = 'js';

    const localPath = path.join(__dirname, 'assets', folder, filename);
    const relPath = `./assets/${folder}/${filename}`;

    process.stdout.write(`Fetching: ${filename} ... `);
    try {
      const info = await downloadFile(rawUrl, localPath);
      process.stdout.write(`OK (${(info.size / 1024).toFixed(1)} KB)\n`);
      manifest.manifest[rawUrl] = {
        localPath: relPath,
        size: info.size,
        contentType: info.contentType,
        status: 'success'
      };
    } catch (e) {
      process.stdout.write(`FAILED (${e.message})\n`);
    }
  }

  fs.writeFileSync('assets_manifest.json', JSON.stringify(manifest, null, 2));
}

run();
