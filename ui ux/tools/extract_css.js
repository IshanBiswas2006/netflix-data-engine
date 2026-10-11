const fs = require('fs');
const path = require('path');

const cssDir = path.join(__dirname, 'assets', 'css');
fs.mkdirSync(cssDir, { recursive: true });

function extractStyles(htmlFile, outputCssFile) {
  const html = fs.readFileSync(htmlFile, 'utf8');
  const styleRe = /<style[^>]*>([\s\S]*?)<\/style>/gi;
  let m;
  const blocks = [];
  while ((m = styleRe.exec(html)) !== null) {
    blocks.push(m[1].trim());
  }
  const combined = blocks.join('\n\n/* ========================================== */\n\n');
  fs.writeFileSync(outputCssFile, combined, 'utf8');
  console.log(`Extracted CSS from ${htmlFile} -> ${outputCssFile} (${(Buffer.byteLength(combined) / 1024).toFixed(1)} KB)`);
}

extractStyles('index.html', path.join(cssDir, 'index.css'));
extractStyles('about.html', path.join(cssDir, 'about.css'));
