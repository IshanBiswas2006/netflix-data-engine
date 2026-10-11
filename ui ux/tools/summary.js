const fs = require('fs');
const path = require('path');

function getDirStats(dir) {
  let count = 0;
  let totalSize = 0;
  if (!fs.existsSync(dir)) return { count: 0, size: 0 };
  const items = fs.readdirSync(dir, { withFileTypes: true });
  for (const item of items) {
    const full = path.join(dir, item.name);
    if (item.isDirectory()) {
      const sub = getDirStats(full);
      count += sub.count;
      totalSize += sub.size;
    } else {
      count++;
      totalSize += fs.statSync(full).size;
    }
  }
  return { count, size: totalSize };
}

const folders = ['js', 'css', 'fonts', 'images', 'videos', 'data', 'icons'];
console.log('=== ASSETS DOWNLOAD SUMMARY ===');
let allCount = 0;
let allSize = 0;
for (const f of folders) {
  const p = path.join(__dirname, 'assets', f);
  const st = getDirStats(p);
  allCount += st.count;
  allSize += st.size;
  console.log('assets/' + f.padEnd(8) + ': ' + st.count.toString().padStart(4) + ' files, ' + (st.size / (1024 * 1024)).toFixed(2) + ' MB');
}
console.log('----------------------------------------');
console.log('TOTAL ASSETS   : ' + allCount.toString().padStart(4) + ' files, ' + (allSize / (1024 * 1024)).toFixed(2) + ' MB');
