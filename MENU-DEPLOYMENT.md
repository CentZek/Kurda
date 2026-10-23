# Kurda table menu

## Permanent address and QR code

The permanent menu address is **https://www.kurda.com/menu**. It uses the existing website and needs no additional Vercel domain or DNS setup.

- Menu: `https://www.kurda.com/menu`
- Table-card print page: `https://www.kurda.com/menu/qr/table-card.html`
- Print-ready A4 PDF: `https://www.kurda.com/menu/qr/kurda-table-cards-85x54mm-a4.pdf`
- QR PNG: `https://www.kurda.com/menu/qr/kurda-menu-qr.png?v=2`
- QR SVG: `https://www.kurda.com/menu/qr/kurda-menu-qr.svg?v=2`

Both QR files encode exactly **https://www.kurda.com/menu**. Use these updated files instead of the earlier subdomain QR. The QR stays the same when prices or dishes change.

The print sheet contains **11 cards, each 85 mm wide × 54 mm high** for landscape holders. Five are upright on the sheet and six are rotated for efficient use of A4. It uses 3 mm gutters, external crop ticks, dotted trim outlines, and at least 4 mm clear printer margins. Print A4 portrait at **Actual size / 100%**, one PDF page per sheet; disable Fit to page. The PDF QR codes are vector graphics with a four-module quiet zone. All eleven were decoded successfully from the 150 dpi Poppler-rendered sheet, and all trim rectangles were checked against the requested physical dimensions.

Rebuild the PDF with `python scripts/build-table-cards.py` (ReportLab, qrcode and fonttools; Windows Georgia font). The script creates a local deliverable in `output/pdf/` and copies it into `dist/menu/qr/`. Regenerate the WebP preview from the PDF after design changes. The print page links directly to the PDF so browser layout scaling does not affect the supplied card sizes.

## Routing

The menu is served from the existing `/menu` directory in the same buildless Vercel project. No subdomain is required. The unused subdomain-specific routes have been removed; the existing homepage, redirects, security and cache headers remain in place. Canonical, social sharing and structured-data URLs all use the permanent menu address. The main robots file references the menu sitemap.

## Menu content and future edits

The authoritative editable data is `dist/menu/menu-data.json`: **126 items, 24 categories**, with listed prices in **IQD**. The original 53 items come from the four-page `MENU BOARDS.pdf`; 73 bar drinks in 14 categories come from the two-page `MENU - KURDA .pdf`. All new drink names and prices were checked visually and by matching their row positions in the PDF.

Edit names, flavours or prices there, then run:

```powershell
python scripts/build-menu.py
```

Commit the JSON and all generated language pages, then push to `main`. Vercel deploys the already-built `dist` directory; no Node build or runtime dependencies are needed. Edit the page shell in `menu-source/template.html`, styles in `dist/menu/menu.css` and interactions in `dist/menu/menu.js`.

The full menu is rendered in HTML and remains readable without JavaScript. With JavaScript enabled it opens on Food (12 items); sticky Food, Drinks (35), Bar (73), and Gifts (6) tabs keep navigation available while scrolling. Illustrated category tiles and a native category selector provide two ways to browse. Search covers every group and all three languages, including English brand names while viewing Arabic or Kurdish. Saved picks also span all groups. Sorting operates within each category and uses the lowest **available** listed size. Items with a null price are shown as "Ask your server", sorted last in both price directions, and omitted from structured-data offers. My picks is a shortlist, not an order or payment flow. No invented ingredients, allergens, availability, popularity rankings or extras are added.

## Languages

- English: `https://www.kurda.com/menu`
- Sorani Kurdish: `https://www.kurda.com/menu/ckb/`
- Arabic: `https://www.kurda.com/menu/ar/`

All 126 names, 24 categories, controls, flavours and serving sizes are localized. The translations live in `menu-source/translations.json`, keyed by stable item IDs; update this file alongside new source items. The builder fails on missing translations. Both Sorani and Arabic use right-to-left layouts, a local Arabic font and isolated left-to-right price numerals. Brand names are transliterated; their original English names remain searchable. The language switch preserves section, category, search, sorting and saved-picks view through URL parameters. Saved items persist locally across languages. Each language has its own canonical URL, structured menu data and hreflang alternatives. The original table QR remains valid.

The mobile redesign was checked in WebKit at widths 320, 390 and 430 px, plus 844 × 390 landscape, and Chromium at 1440 px. Checks covered all categories, all prices, cross-language search, saved picks, language changes, missing prices, image loading, horizontal overflow and no-JavaScript fallback. Automated WCAG A/AA checks reported no violations in the inspected English and RTL views. Human language review can be applied directly in the translation file without altering prices.

Important source details retained:

- White Mocha has **medium 5,000 / large 6,000 IQD**, with no small size listed.
- Iced Spanish Latte is **7,500 / 10,500 / 11,500 IQD**.
- Iced Latte Flavour and Double Shot Iced Shaken Espresso each have a single listed price, without an invented size.
- All six gifts, including four teddy-bear sizes, are included.
- 1800 Tequila (4 cl) has no price printed in the bar PDF. It is included with a null price and "Ask your server", as agreed with the user.
- Bar serving sizes are shown as 4 cl only where the PDF specifies this. No serving volume is invented for beer, cocktails, Irish whiskey, rum or wine.
- Jameson Caskmates appears separately under cocktails (17,500 IQD) and Irish whiskey (13,500 IQD), exactly as listed.

## Artwork and performance

The illustrated iced coffees, hot chocolate, tea glass and mountain home were extracted from the user's own PDF vector artwork, rendered with transparency and compressed to WebP. The new visual category design adds watercolor food/coffee art and illustrations extracted from the bar PDF. See `MENU-IMAGERY.md` for provenance and generation prompts. These are category illustrations, not photographs of specific served items. The existing original English and Kurdish logos are reused. Fonts are self-hosted. The source PDFs are deliberately excluded from the website and GitHub; the menu does not download them.

Continuous motion can be paused and respects the operating system's reduced-motion setting. Only visible cards animate. There are no third-party trackers, remote font requests, frameworks or backend services.

`menu-source/social.html` is the 1200 × 630 source layout for the menu's social sharing image. The QR is high error-correction, with a four-module quiet zone. Use the A4 PDF linked above to print the 85 × 54 mm table cards.
