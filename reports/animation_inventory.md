# Animation Inventory

| Animation Target | Initial State | Trigger | Final / Active State | Duration & Easing | Implementation Method |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sticky Header** | `top: 0`, static | Scroll down | Fixed top, `backdrop-filter: blur(10px)`, `bg: rgba(11,13,14,0.6)` | Instant on sticky threshold | CSS `position: sticky` |
| **Card Hover Lift** | `translateY(0)` | Pointer `:hover` | `translateY(-4px)`, border: `1px solid rgba(255,255,255,0.25)` | 0.25s `cubic-bezier(0.16, 1, 0.3, 1)` | CSS transition |
| **Ambient Glow Orbs** | `scale(1)`, `opacity: 0.25` | Page load / infinite | `scale(1.06)`, `opacity: 0.35` | 8s alternate `ease-in-out` | CSS `@keyframes glow-pulse` |
| **Pill Badge Hover** | `bg: rgba(255,255,255,0.15)` | Pointer `:hover` | `bg: rgba(255,255,255,0.25)` | 0.2s `ease` | CSS transition |
| **Table Row Highlight** | `bg: transparent` | Pointer `:hover` | `bg: rgba(255,255,255,0.04)` | 0.15s `ease` | CSS transition |
| **Chart Reveal** | `opacity: 0.9` | Pointer `:hover` | `opacity: 1`, `scale(1.01)` | 0.3s `ease` | CSS transition |
