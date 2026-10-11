# Interaction Inventory

| Interaction Component | Interaction Behavior | Visual State | Target Route / Action |
| :--- | :--- | :--- | :--- |
| **Navigation Menu Bar** | Click on navigation pill links | Active link highlighted with border / brighter pill background | Routes: `/`, `/analysis`, `/visualizations`, `/sql-queries`, `/about` |
| **Hero CTA Buttons** | Primary action button with pill shape and accent | Hover highlights border and subtle scale | Jumps to `/analysis` or `/visualizations` |
| **SQL Query Accordion** | Click on SQL query questions | Expands/collapses full query SQL statement and execution result table | Interactive DOM toggle in `/sql-queries` |
| **Chart Lightbox / Zoom** | Click on chart preview card | Opens high-resolution modal view of visualization with summary stats | Lightbox modal in `/visualizations` |
| **Data Filter / Search** | Type in search input on Analysis / Queries page | Dynamically filters rows or tables | Instant client-side DOM filter in `main.js` |
| **Mobile Menu Toggle** | Hamburger button tap on viewport < 810px | Drops down navigation drawer with glassmorphism backdrop | Responsive mobile drawer toggle |
