# Tracy Najjingo · Portfolio

Personal portfolio for Tracy Najjingo, brand and marketing strategist in Dubai.

## Structure
- `build.py`: all site content (brands, projects, journey, contact details) and the page templates
- `src/styles.css`, `src/site.js`: design and interactions
- `assets/`: portrait, brand logos and project screenshots
- `dist/`: the finished website (this is what gets published)

## Update the site
1. Edit the content at the top of `build.py`.
2. Run `python3 build.py`.
3. Commit and push. Netlify publishes `dist/` automatically.

## Hosting (Netlify)
Add new site → Import from GitHub → this repo. Build command: `python3 build.py`. Publish directory: `dist`.
