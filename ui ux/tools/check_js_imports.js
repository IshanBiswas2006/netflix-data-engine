const fs = require('fs');
const path = require('path');

const jsDir = path.join(__dirname, 'assets', 'js');
const files = fs.readdirSync(jsDir).filter(f => f.endsWith('.mjs') || f.endsWith('.js'));

console.log('=== Checking imports in JS files ===');
for (const file of files) {
  const code = fs.readFileSync(path.join(jsDir, file), 'utf8');
  const importRe = /(?:import|from)\s+['"]([^'"]+)['"]/g;
  let m;
  const external = [];
  while ((m = importRe.exec(code)) !== null) {
    if (m[1].startsWith('http')) external.push(m[1]);
  }
  if (external.length > 0) {
    console.log(`${file} imports external URLs:`, external);
  }
}
