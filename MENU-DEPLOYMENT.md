# Kurda table menu

## Permanent address and QR code

The permanent menu address is **https://www.kurda.com/menu**. It uses the existing website and needs no additional Vercel domain or DNS setup.

- Menu: `https://www.kurda.com/menu`
- Printable A6 table card: `https://www.kurda.com/menu/qr/table-card.html`
- QR PNG: `https://www.kurda.com/menu/qr/kurda-menu-qr.png?v=2`
- QR SVG: `https://www.kurda.com/menu/qr/kurda-menu-qr.svg?v=2`

Both QR files encode exactly **https://www.kurda.com/menu**. Use these updated files instead of the earlier subdomain QR. The QR stays the same when prices or dishes change.

## Routing

The menu is served from the existing `/menu` directory in the same buildless Vercel project. No subdomain is required. The unused subdomain-specific routes have been removed; the existing homepage, redirects, security and cache headers remain in place. Canonical, social sharing and structured-data URLs all use the permanent menu address. The main robots file references the menu sitemap.

## Menu content and future edits

The authoritative editable data is `dist/menu/menu-data.json`: **53 items, 10 categories**, all prices in **IQD**, transcribed and visually verified against the four pages of the supplied `MENU BOARDS.pdf`.

Edit names, flavours or prices there, then run:

```powershell
python scripts/build-menu.py
```

Commit both the JSON and generated `dist/menu/index.html`, then push to `main`. Vercel deploys the already-built `dist` directory; no Node build or runtime dependencies are needed. Edit the page shell in `menu-source/template.html`, styles in `dist/menu/menu.css` and interactions in `dist/menu/menu.js`.

The full menu is rendered in HTML and remains readable without JavaScript. Search, category filters, price/name sorting and locally saved picks progressively enhance it. Sorting by price uses the lowest **available** listed size. My picks is a shortlist, not an order or payment flow. No invented ingredients, allergens, availability, popularity rankings or extras are added.

Important source details retained:

- White Mocha has **medium 5,000 / large 6,000 IQD**, with no small size listed.
- Iced Spanish Latte is **7,500 / 10,500 / 11,500 IQD**.
- Iced Latte Flavour and Double Shot Iced Shaken Espresso each have a single listed price, without an invented size.
- All six gifts, including four teddy-bear sizes, are included.

## Artwork and performance

The illustrated iced coffees, hot chocolate, tea glass and mountain home were extracted from the user's own PDF vector artwork, rendered with transparency and compressed to WebP. They are illustrations, not photographs of specific served items. The existing original English and Kurdish logos are reused. Fonts are self-hosted. The 251 MB source PDF is deliberately excluded from the website and GitHub; the menu does not download it.

Continuous motion can be paused and respects the operating system's reduced-motion setting. Only visible cards animate. There are no third-party trackers, remote font requests, frameworks or backend services.

`menu-source/social.html` is the 1200 × 630 source layout for the menu's social sharing image. The QR is high error-correction, with a four-module quiet zone. The A6 card can be printed or saved as PDF in the browser's print dialog.
