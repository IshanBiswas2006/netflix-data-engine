const fs = require('fs');

const indexHtml = fs.readFileSync('index_raw.html', 'utf8');

// Check <link rel="stylesheet">
const links = [];
const linkRe = /<link[^>]+rel=["']stylesheet["'][^>]*>/gi;
let m;
while ((m = linkRe.exec(indexHtml)) !== null) {
  links.push(m[0]);
}
console.log('Stylesheet links:', links);

// Check <style> tags
const styleRe = /<style[^>]*>([\s\S]*?)<\/style>/gi;
let styleCount = 0;
let totalCssLen = 0;
while ((m = styleRe.exec(indexHtml)) !== null) {
  styleCount++;
  totalCssLen += m[1].length;
}
console.log(`Found ${styleCount} inline <style> tags, total CSS length: ${totalCssLen} characters (${(totalCssLen / 1024).toFixed(1)} KB)`);
