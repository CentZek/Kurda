# Kurda table menu

## Permanent address and QR code

The permanent menu address is **https://www.kurda.com/menu**. It uses the existing website and needs no additional Vercel domain or DNS setup.

- Menu: `https://www.kurda.com/menu`
- Table-card print page: `https://www.kurda.com/menu/qr/table-card.html`
- Print-ready A4 PDF: `https://www.kurda.com/menu/qr/kurda-table-cards-85x54mm-a4.pdf`
- QR PNG: `https://www.kurda.com/menu/qr/kurda-menu-qr.png?v=2`
- QR SVG: `https://www.kurda.com/menu/qr/kurda-menu-qr.svg?v=2`

Both QR files encode exactly **https://www.kurda.com/menu**. Use these updated files instead of the earlier subdomain QR. The QR stays the same when prices or dishes change.

The print sheet contains **11 cards, each 85 mm wide × 54 mm high** for landscape holders. Five are upright on the sheet and six are rotated for efficient use of A4. It uses 3 mm gutters, external crop ticks, solid black 0.8 pt trim outlines and 1 pt corner ticks, and at least 4 mm clear printer margins. Print A4 portrait at **Actual size / 100%**, one PDF page per sheet; disable Fit to page. The PDF QR codes are vector graphics with a four-module quiet zone. All eleven were decoded successfully from the 150 dpi Poppler-rendered sheet, and all trim rectangles were checked against the requested physical dimensions.

Rebuild the PDF with `python scripts/build-table-cards.py` (ReportLab, qrcode and fonttools; Windows Georgia font). The script creates a local deliverable in `output/pdf/` and copies it into `dist/menu/qr/`. Regenerate the WebP preview from the PDF after design changes. The print page links directly to the PDF so browser layout scaling does not affect the supplied card sizes.

## Routing

The menu is served from the existing `/menu` directory in the same buildless Vercel project. No subdomain is required. The unused subdomain-specific routes have been removed; the existing homepage, redirects, security and cache headers remain in place. Canonical, social sharing and structured-data URLs all use the permanent menu address. The main robots file references the menu sitemap.

## Menu content and future edits

The authoritative editable data is `dist/menu/menu-data.json`: **255 entries, 35 categories, 339 fixed price points**, in **IQD**. The replacement list supplied and confirmed by the owner on 23 October 2026 supersedes both earlier PDFs. Use only the prices **outside brackets**. Bracketed values are not included in the published data, HTML or structured data. Unlisted old items have been removed. Tobacco sales listings are excluded.

Edit names, flavours or prices there, then run:

```powershell
python scripts/build-menu.py
python scripts/check-menu.py
```

Commit the JSON and all generated language pages, then push to `main`. Vercel deploys the already-built `dist` directory; no Node build or runtime dependencies are needed. Edit the page shell in `menu-source/template.html`, styles in `dist/menu/menu.css` and interactions in `dist/menu/menu.js`.

The full menu is rendered in HTML and remains readable without JavaScript. With JavaScript enabled it opens on Food (54 entries); sticky Food, Drinks (63), Bar (104), and Shop (34) tabs remain available while scrolling. Shop contains gifts, sweets, nuts, market snacks, mobile cards and eSIMs. Mocktails are under Drinks. Illustrated category tiles and a native category selector provide two ways to browse.

Search covers all groups, all three languages, English brand names, flavours and availability notes. Saved picks span all groups and persist locally. Sorting operates within each category and uses the lowest listed size. The two variable-price mobile services say "Ask cashier", explain that the customer chooses the amount with the cashier, have no invented price or schema offer, and sort after fixed-price items. My picks is a shortlist, not an order or payment flow.

## Languages

- English: `https://www.kurda.com/menu`
- Sorani Kurdish: `https://www.kurda.com/menu/ckb/`
- Arabic: `https://www.kurda.com/menu/ar/`

All 255 names, 35 categories, controls, 30 listed flavour options, serving sizes and availability notes are localized. The translations live in `menu-source/translations.json`, keyed by stable item IDs; update this file alongside new source items. The builder fails on missing translations. Both Sorani and Arabic use right-to-left layouts, a local Arabic font and isolated left-to-right price numerals. Brand names are transliterated; their original English names remain searchable. The language switch preserves section, category, search, sorting and saved-picks view through URL parameters. Saved items persist locally across languages. Each language has its own canonical URL, structured menu data and hreflang alternatives. The original table QR remains valid.

The mobile redesign was checked in WebKit at widths 320, 390 and 430 px, plus 844 × 390 landscape, and Chromium at 1440 px. Checks covered all categories, all prices, cross-language search, saved picks, language changes, missing prices, image loading, horizontal overflow and no-JavaScript fallback. Automated WCAG A/AA checks reported no violations in the inspected English and RTL views. Human language review can be applied directly in the translation file without altering prices.

Important replacement-list details:

- Espresso Single / Double: **6,500 / 8,000 IQD**. Espresso Macchiato uses **Small / Medium**, exactly as supplied.
- White Chocolate Mocha: **Small 8,500 / Medium 9,500 / Large 10,500 IQD**.
- Creme Frappe and White Chocolate Creme Frappe: **8,000 / 9,000 / 10,500 IQD**. Creme flavours are Vanilla, Hazelnut and Chocolate.
- Iced Spanish Latte: **10,000 / 11,000 / 12,000 IQD**.
- Eight pizza choices all have **Small 10,500 / Medium 15,000 / Large 19,500 IQD**.
- Iced Latte, Iced Mocha, Magnum, Cornetto, Freez and Rani show the complete supplied flavour lists with their shared prices. Previous overlapping records are consolidated into those choices.
- Teddy Bear has **Small / Medium / Large**, and Flower has **Medium / Large**. The old extra-large bear is removed.
- Kurda Nuts appears once under Sweets & nuts; it was repeated with identical sizes and prices in the source list.
- 1800 Tequila now has a fixed price of **19,000 IQD**.
- Heineken Draught explicitly shows **35 cl / 9,500** and **50 cl / 15,000**; Krombacher Pils shows **500 ml / 13,500**. No other serving volumes are invented from the previous PDFs.
- Jameson Ginger Ale is **17,500 IQD** under Cocktails. Jameson Caskmate is **13,500 IQD** under Irish Whiskey. The old Jameson Caskmates cocktail entry is removed.
- Central meals display **K5 only** in the category heading and on every item in all three languages.
- Mobile cards and eSIMs have variable amounts, not a zero or fixed price.

`scripts/check-menu.py` checks coverage, approved price/size fixtures, removed records, flavours, localized strings, HTML item IDs and schema offers. Browser checks also compare every displayed price and size in all languages against the data, check all category filters, cross-language search, saved picks, narrow-screen layouts and accessibility.

## Artwork and performance

The illustrated iced coffees, hot chocolate, tea glass and mountain home were extracted from the user's own PDF vector artwork, rendered with transparency and compressed to WebP. The new visual category design adds watercolor food/coffee art and illustrations extracted from the bar PDF. See `MENU-IMAGERY.md` for provenance and generation prompts. These are category illustrations, not photographs of specific served items. The existing original English and Kurdish logos are reused. Fonts are self-hosted. The source PDFs are deliberately excluded from the website and GitHub; the menu does not download them.

Continuous motion can be paused and respects the operating system's reduced-motion setting. Only visible cards animate. There are no third-party trackers, remote font requests, frameworks or backend services.

`menu-source/social.html` is the 1200 × 630 source layout for the menu's social sharing image. The QR is high error-correction, with a four-module quiet zone. Use the A4 PDF linked above to print the 85 × 54 mm table cards.
