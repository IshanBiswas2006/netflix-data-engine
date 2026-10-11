const fs = require('fs');

for (const file of ['index_raw.html', 'about_raw.html']) {
  const content = fs.readFileSync(file, 'utf8');
  const links = new Set();
  const re = /href=["']([^"']+)["']/gi;
  let m;
  while ((m = re.exec(content)) !== null) {
    links.add(m[1]);
  }
  console.log(`=== Links in ${file} ===`);
  for (const l of links) {
    if (!l.startsWith('http') || l.includes('nehayadav') || l.includes('framer')) {
      console.log(' - Internal/Framer link:', l);
    } else {
      console.log(' - External link:', l);
    }
  }
}
