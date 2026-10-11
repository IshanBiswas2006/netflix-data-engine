# UI Template Analysis Report

## Project Name: Netflix Movies and TV Shows Analysis
**Reference Template**: Neha Yadav Design Portfolio (`d:\Work\netflix\index.html`, `assets/`)

---

## A. Existing Template Structure

The supplied reference template is a portfolio website with a dark design language.
1. **Header & Navigation**:
   - Fixed / Sticky header with `position: sticky; top: 0; z-index: 10`.
   - Frosted glass effect: `backdrop-filter: blur(10px); background-color: rgba(11, 13, 14, 0.6);`.
   - Centered pill navigation menu containing rounded buttons and active state pill styling (`data-framer-page-link-current="true"`).
2. **Hero Section**:
   - Deep charcoal/black canvas (`#0b0d0e`).
   - Ambient glowing background orbs with `radial-gradient(50% 50%, #928dab 0%, #1f1c2c 100%)` and `filter: blur(100px)`.
   - Large bold typography utilizing custom uppercase display font **Tanker** and geometric sans **Space Grotesk**.
   - Floating visual elements, stickers, and tags.
3. **Showcase / Content Cards**:
   - Dark cards (`#161616` and `#0a0a0a`) with subtle hairline borders (`1px solid #292929` or `1px solid rgba(255, 255, 255, 0.1)`).
   - Generous border radius (`16px` to `24px`).
   - Metadata pill tags (`background-color: rgba(255, 255, 255, 0.15); border-radius: 20px; padding: 4px 12px; font-size: 13px; color: #fff;`).
   - Clean horizontal and vertical flex/grid alignments.
4. **Data & Statistics Representation**:
   - Grid of metric boxes with large values and subtle descriptions.
   - High-contrast visual cards with hover scaling (`transform: translateY(-4px)`).
5. **Footer**:
   - Clean bottom bar with subtle branding, social/external links, copyright, and smooth top-scroll interaction.

---

## B. Visual Design Rules

- **Palette**:
  - Main Background: `#0b0d0e` (Deep charcoal obsidian)
  - Card Surfaces: `#161616`, `#0a0a0a`
  - High-Contrast Text: `#ffffff`
  - Secondary Text / Subtitles: `rgba(255, 255, 255, 0.6)` / `#acabb2`
  - Subtle Borders: `1px solid #292929` or `1px solid rgba(255, 255, 255, 0.1)`
  - Accent Red/Orange: `#ff462e` / `#e50914` (harmonious with Netflix brand accent)
  - Accent Green: `#14c700`
  - Accent Blue: `#009dff`
  - Ambient Glows: `radial-gradient(circle, rgba(146, 141, 171, 0.25) 0%, rgba(31, 28, 44, 0.05) 70%, transparent 100%)`
- **Typography**:
  - Display Titles: `Tanker`, `sans-serif` (uppercase, letter-spacing: 1.2px)
  - Section Headings & Badges: `Space Grotesk`, `sans-serif` (weights 500, 600, 700)
  - Body Text & Tables: `Inter`, `sans-serif` (weights 400, 500)
- **Spacings & Proportions**:
  - Max Content Width: `1200px` to `1440px` centered
  - Section Padding: `80px 40px` (Desktop), `40px 20px` (Mobile)
  - Card Gap: `24px` to `32px`

---

## C. Components That Must Remain Visually Consistent

1. **Sticky Frosted Header**: Navigation bar with blur and pill buttons.
2. **Ambient Glow Backgrounds**: Blurred radial gradients behind headers and key stats.
3. **Pill Badges & Tag Labels**: Rounded chips indicating categories, metrics, and filters.
4. **Card Container Styles**: `#161616` background, `16px` border-radius, `1px solid #292929` outline.
5. **Typography Stack**: Tanker for heroic statements, Space Grotesk for metrics and section titles, Inter for body descriptions.
6. **Footer Layout**: Minimalist footer with bottom alignment.

---

## D. Components That Must Be Adapted for This Project

1. **Hero Content**:
   - *Original*: Personal portfolio introduction.
   - *Adapted*: Netflix Analytics Overview — headline "NETFLIX CATALOG INTELLIGENCE", key summary badges (6,234 Titles, 12 Feature Dimensions, 2 Content Types).
2. **Project Cards**:
   - *Original*: Design case studies.
   - *Adapted*: Feature highlights linking to Analysis, Visualizations, and SQL Engine.
3. **Visual Showcase Area**:
   - *Original*: Artwork & UI screenshots.
   - *Adapted*: High-resolution Matplotlib analytical charts displaying verified catalog distributions.
4. **Data Presentation Area**:
   - *Original*: Skill tags and experience list.
   - *Adapted*: Interactive SQL analytical query inspector, results tables, and metric breakdowns.

---

## E. Pages Required by the Project

1. **`GET /` (Home)**:
   - Hero banner with catalog statistics.
   - Metric overview cards (Total Titles, Movies %, TV Shows %, Top Countries, Peak Release Year).
   - Recent catalog additions showcase.
2. **`GET /analysis` (Analysis)**:
   - Detailed exploratory findings.
   - Categorical breakdowns (Movie vs TV Show ratios, rating distributions, duration stats, genre dominance).
3. **`GET /visualizations` (Visualizations)**:
   - Full gallery of the 8 Matplotlib charts with explanations and key insights.
4. **`GET /sql-queries` (SQL Analysis)**:
   - 10 Analytical questions with SQL queries and interactive result tables.
   - Verification status and execution details.
5. **`GET /about` (About)**:
   - Project methodology, data cleaning steps, technology stack, and limitations.

---

## F. Missing Information & Uncertainties

- Some Framer animation sequences rely on client-side React bundle hydration. For standard Flask SSR delivery, all visual styling, sticky navigation, card transitions, glowing ambiances, and hover transforms are implemented in native, highly performant CSS and vanilla JavaScript, ensuring zero reliance on proprietary Framer CDN bundles and guaranteed offline execution.
