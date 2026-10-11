# Neha Yadav Design Portfolio — Complete Offline Asset Mirror

Complete offline download of **[https://nehayadav.framer.website/](https://nehayadav.framer.website/)** including all HTML pages, CSS stylesheets, JavaScript/MJS bundles, fonts, images, video assets, icons, and metadata.

---

## 📁 Project Structure

```text
d:\Work\template\
├── index.html                  # Main Home page (fully rewritten with local asset paths)
├── about.html                  # About page (fully rewritten with local asset paths)
├── sitemap.xml                 # XML sitemap from original site
├── robots.txt                  # Robots exclusion standard file
├── server.js                   # Node.js local preview & dev server (with Range & CORS support)
├── package.json                # npm scripts (`npm start` / `npm run dev`)
├── assets_manifest.json        # Complete map of 300+ original URLs -> local paths & sizes
├── assets/
│   ├── css/                    # Extracted and structured CSS stylesheets
│   │   ├── index.css           # 145 KB layout, font-face, and responsive style rules
│   │   └── about.css           # 118 KB styles for the About page
│   ├── js/                     # 17 JavaScript & MJS module files
│   │   ├── script_main.*.mjs   # Framer main script bundle
│   │   ├── react.*.mjs         # React runtime bundle
│   │   ├── framer.*.mjs        # Framer component engine
│   │   ├── motion.*.mjs        # Framer Motion animations
│   │   └── ...                 # Route chunks and UI dependencies
│   ├── fonts/                  # 18 Web font files (WOFF2 & TTF)
│   │   ├── Space Grotesk       # Google Fonts (weights 400, 500, 700)
│   │   ├── Fontshare fonts     # Tanker, Cabinet Grotesk, Satoshi
│   │   └── Inter               # Multi-language unicode ranges
│   ├── images/                 # 59 High-resolution images (PNG, JPG, WebP, SVG)
│   ├── videos/                 # 2 MP4 video assets (interactive demo showcases)
│   ├── icons/                  # 4 Favicons and touch icons (light & dark modes)
│   └── data/                   # Search indexes & JSON metadata
└── tools/                      # Automated scraping, downloading, and validation utilities
```

---

## 🚀 How to Run Locally

### Option 1: Using npm (Recommended)
```bash
npm start
```

### Option 2: Using Node.js directly
```bash
node server.js
```

Then open your browser at:
- **Home Page**: [http://localhost:3000/](http://localhost:3000/)
- **About Page**: [http://localhost:3000/about](http://localhost:3000/about)

---

## 📊 Asset Summary

| Category | Count | Total Size | Description |
| :--- | :---: | :---: | :--- |
| **HTML Pages** | 2 | ~620 KB | `index.html` and `about.html` with relative asset links |
| **CSS Stylesheets** | 2 | ~263 KB | Extracted standalone stylesheets in `assets/css/` |
| **JavaScript / MJS** | 17 | ~1.67 MB | Framer engine, React runtime, motion libraries, and route bundles |
| **Fonts (WOFF2/TTF)** | 18 | ~370 KB | Space Grotesk, Fontshare, and Inter font families |
| **Images** | 59 | ~10.04 MB | Portfolio previews, project mockups, badges, and avatars |
| **Videos (MP4)** | 2 | ~4.16 MB | High-definition product showcase video clips |
| **Icons** | 4 | ~10 KB | Default light/dark favicons and touch icons |
| **Data / JSON** | 8 | ~10 KB | Site search indexes and configuration JSON |
| **TOTAL** | **112+** | **~17.1 MB** | **100% complete offline mirror** |

---

## ⚙️ Features & Verification

1. **Zero External Dependencies**: All asset URLs (`framerusercontent.com`, `fonts.gstatic.com`, etc.) have been downloaded locally and linked using relative paths.
2. **ES Module Resolution**: All JavaScript `.mjs` import trees and chunk relationships resolve cleanly locally.
3. **Range Video Streaming**: `server.js` supports HTTP 206 partial content streaming for smooth video playback.
4. **CORS & MIME Headers**: Correct `application/javascript`, `font/woff2`, and `video/mp4` headers configured for flawless modern browser rendering.
