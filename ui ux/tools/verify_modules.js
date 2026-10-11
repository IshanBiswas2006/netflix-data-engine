const fs = require('fs');
const path = require('path');

const jsDir = path.join(__dirname, 'assets', 'js');
const files = fs.readdirSync(jsDir).filter(f => f.endsWith('.mjs') || f.endsWith('.js'));

console.log('=== Verifying module dependency resolution ===');
let missingCount = 0;

for (const file of files) {
  const code = fs.readFileSync(path.join(jsDir, file), 'utf8');
  // Match relative imports
  const re = /(?:import|from)\s*['"](\.\/[^'"]+)['"]/g;
  let m;
  while ((m = re.exec(code)) !== null) {
    const target = path.join(jsDir, m[1]);
    if (!fs.existsSync(target)) {
      console.log(`[MISSING] ${file} -> ${m[1]}`);
      missingCount++;
    }
  }

  // Match dynamic imports
  const dynRe = /import\s*\(\s*['"](\.\/[^'"]+)['"]\s*\)/g;
  while ((m = dynRe.exec(code)) !== null) {
    const target = path.join(jsDir, m[1]);
    if (!fs.existsSync(target)) {
      console.log(`[MISSING DYN] ${file} -> ${m[1]}`);
      missingCount++;
    }
  }
}

if (missingCount === 0) {
  console.log('SUCCESS: All relative module imports resolve perfectly!');
} else {
  console.log(`WARNING: ${missingCount} unresolved imports.`);
}
