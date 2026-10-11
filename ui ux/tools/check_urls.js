const fs = require('fs');

for (const file of ['index.html', 'about.html']) {
  const content = fs.readFileSync(file, 'utf8');
  console.log(`\n=== Checking external URLs in ${file} ===`);
  const urls = new Set();
  const re = /(https?:\/\/[^\s"'<>)]+)/gi;
  let m;
  while ((m = re.exec(content)) !== null) {
    urls.add(m[1]);
  }
  for (const u of urls) {
    if (u.includes('framerusercontent.com') || u.includes('fonts.gstatic.com')) {
      console.log(' - Remaining external asset URL:', u);
    }
  }
}
