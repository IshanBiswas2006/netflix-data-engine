# UI Replication Analysis

## Section A: Visual Structure
- **Canvas & Viewport**:
  - Max container width: 1440px with responsive breakpoints at 1440px, 1200px, 810px, and mobile (<810px).
  - Background color: `#0b0d0e` (Obsidian Charcoal).
  - Typography:
    - Display font: `Tanker` (Uppercase grotesque display).
    - Subhead / UI font: `Space Grotesk` (Weights 400, 500, 700).
    - Body font: `Inter` (Weights 400, 500).
  - Cards:
    - Background: `#161616` (Deep surface) and `#0a0a0a` (Contrasting inner surface).
    - Border: `1px solid #292929` and `1px solid rgba(255, 255, 255, 0.1)`.
    - Border radius: `16px` to `24px`.
    - Box-shadow / glow: Subtle ambient lighting.
  - Badges & Pills:
    - Background: `rgba(255, 255, 255, 0.15)`.
    - Border-radius: `20px`.
    - Padding: `6px 14px`.

## Section B: Animation Inventory
1. **Header Sticky & Blur**:
   - Element: `<header class="site-header">` / `#nav`
   - Initial State: Normal scroll position.
   - Final State: Fixed sticky top (`top: 0`), blurred background (`backdrop-filter: blur(12px)`).
2. **Card Hover Lift**:
   - Element: `.project-card`, `.stat-card`, `.chart-card`
   - Trigger: `:hover`
   - Transform: `translateY(-4px)`
   - Transition: `transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.25s ease`
   - Final state: Subtle border brightening (`rgba(255, 255, 255, 0.25)`).
3. **Ambient Glow Pulse**:
   - Element: `.glow-orb`
   - Keyframes: Subtle breath animation (scale 1 to 1.05, opacity 0.25 to 0.35).
   - Duration: 8s infinite alternate ease-in-out.
4. **Button & Link Hover**:
   - Element: `.nav-pill`, `.action-btn`
   - Trigger: `:hover`
   - Transform: Background lightening from `rgba(255,255,255,0.1)` to `rgba(255,255,255,0.2)`.

## Section C: Interaction Inventory
1. **Pill Navigation**:
   - Active page highlighted with solid pill background.
   - Seamless navigation across routes (`/`, `/analysis`, `/visualizations`, `/sql-queries`, `/about`).
2. **SQL Query Accordion / Tabs**:
   - Click to inspect specific query details, execution time, and data tables.
3. **Chart Lightbox / Fullscreen Zoom**:
   - Clicking on a Matplotlib visualization opens high-resolution preview with detailed analytical metrics.
4. **Mobile Responsive Menu**:
   - Toggle navigation overlay on screen widths < 810px.

## Section D: Dependencies
- Web Fonts: Space Grotesk, Tanker, Inter (located in `assets/fonts/` and served locally).
- CSS: `assets/css/styles.css`, `assets/css/fonts.css`, `static/css/style.css`.
- JS: Vanilla JS in `static/js/main.js` (no heavy external framework required).

## Section E: Asset Inventory
- Fonts: `assets/fonts/*.woff2` (32 local font files preserved).
- Images: `assets/images/*.png` (icons, badges, stickers preserved).
- Generated Charts: `static/images/charts/01_movies_vs_tv_shows.png` through `08_titles_added_over_time.png`.

## Section F: Page Mapping
- Template Home (`/`) -> Netflix Analytics Portal Home (`/`)
- Template Projects Section (`/#projects`) -> Netflix Analytics & Insights (`/analysis`)
- Template Visuals Showcase -> Matplotlib Visualization Gallery (`/visualizations`)
- Template Code / Specs Section -> SQL Analytics Engine (`/sql-queries`)
- Template About Page (`/about`) -> Project Overview, Methodology, and Limitations (`/about`)

## Section G: Uncertainties
- Client-side Framer telemetry and remote editor scripts (`events.js`, `init.mjs`) are non-functional offline; clean local replacements are implemented.
