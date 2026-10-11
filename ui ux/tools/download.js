const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const indexHtml = fs.readFileSync('index_raw.html', 'utf8');
const aboutHtml = fs.readFileSync('about_raw.html', 'utf8');

function extractUrls(html) {
  const set = new Set();
  // match URLs starting with https:// or http:// or absolute paths
  const re = /(https?:\/\/[a-zA-Z0-9_\-\.\/]+(?:\?[a-zA-Z0-9_\-=\&\.\%\+]*)?)/gi;
  let match;
  while ((match = re.exec(html)) !== null) {
    let url = match[1];
    // clean trailing quotes or parentheses or commas
    url = url.replace(/[\"\'\)\,\;\<\>]+$/, '');
    set.add(url);
  }
  return Array.from(set);
}

const allUrls = Array.from(new Set([...extractUrls(indexHtml), ...extractUrls(aboutHtml)]));
console.log('Total URLs found in HTML files:', allUrls.length);

const framerUrls = allUrls.filter(u => u.includes('framerusercontent.com') || u.includes('framer.com'));
console.log('Framer asset URLs count:', framerUrls.length);

const summary = {};
for (const u of framerUrls) {
  const clean = u.split('?')[0];
  const ext = path.extname(clean).toLowerCase() || 'no_ext';
  summary[ext] = (summary[ext] || 0) + 1;
}
console.log('Asset breakdown by extension:', summary);
fs.writeFileSync('urls.json', JSON.stringify({ all: allUrls, framer: framerUrls }, null, 2));
