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

The authoritative editable data is `dist/menu/menu-data.json`: **255 entries across 35 categories**. The owner requested removal of all prices on 24 October 2026. The catalog contains item names, flavours, size options and availability notes only. There are no monetary values in the served JSON, embedded page data or search-engine structured data, and no Offer objects. Every language tells guests that prices are available at the cashier and asks them to order there.

The item list supplied on 23 October 2026 supersedes the earlier PDFs. Unlisted old items remain removed. Tobacco sales listings are excluded.

Edit names, flavours or sizes there, then run:

```powershell
python scripts/build-menu.py
python scripts/check-menu.py
```

Commit the JSON and all generated language pages, then push to `main`. Vercel deploys the already-built `dist` directory; no Node build or runtime dependencies are needed. Edit the page shell in `menu-source/template.html`, styles in `dist/menu/menu.css` and interactions in `dist/menu/menu.js`.

The full menu is rendered in HTML and remains readable without JavaScript. With JavaScript enabled it opens on Food (54 entries); sticky Food, Drinks (63), Bar (104), and Shop (34) tabs remain available while scrolling. Shop contains gifts, sweets, nuts, market snacks, mobile cards and eSIMs. Mocktails are under Drinks. Illustrated category tiles and a native category selector provide two ways to browse.

Search covers all groups, all three languages, English brand names, flavours and availability notes. Saved picks span all groups and persist locally. Sorting offers menu order or alphabetical order within a category; old price-sorting URL parameters fall back to menu order. Size options remain visible as small labels. Mobile services still explain that the customer chooses the amount with the cashier. My picks is a shortlist, not an order or payment flow.

## Languages

- English: `https://www.kurda.com/menu`
- Sorani Kurdish: `https://www.kurda.com/menu/ckb/`
- Arabic: `https://www.kurda.com/menu/ar/`

All 255 names, 35 categories, controls, 30 listed flavour options, serving sizes and availability notes are localized. The translations live in `menu-source/translations.json`, keyed by stable item IDs; update this file alongside new source items. The builder fails on missing translations. Both Sorani and Arabic use right-to-left layouts, a local Arabic font and translated size labels. Brand names are transliterated; their original English names remain searchable. The language switch preserves section, category, search, sorting and saved-picks view through URL parameters. Saved items persist locally across languages. Each language has its own canonical URL, structured menu data and hreflang alternatives. The original table QR remains valid.

The mobile redesign was checked in WebKit at widths 320, 390 and 430 px, plus 844 × 390 landscape, and Chromium at 1440 px. Checks covered all categories, price removal, sizes, cross-language search, saved picks, language changes, cashier messaging, image loading, horizontal overflow and no-JavaScript fallback. Automated WCAG A/AA checks reported no violations in the inspected English and RTL views. Human language review can be applied directly in the translation file without altering the catalog.

Catalog details retained:

- Espresso Macchiato has Small / Medium; White Chocolate Mocha, both creme frappes, Iced Spanish Latte and all eight pizzas have Small / Medium / Large.
- All listed flavours remain available, including nine Magnum options and seven Cornetto options.
- Teddy Bear has Small / Medium / Large, and Flower has Medium / Large.
- Kurda Nuts appears once under Sweets & nuts; it was repeated in the supplied list.
- Heineken Draught explicitly shows 35 cl and 50 cl; Krombacher Pils shows 500 ml. No additional serving volumes are inferred.
- Central meals display K5 only in the category heading and on every item in all three languages.

`scripts/check-menu.py` checks catalog coverage, size and flavour preservation, translations, removed records, HTML item IDs and absence of prices or offers in generated pages. Browser checks cover mobile English, Arabic and Sorani layouts, the cashier message, size labels, category filtering, search, alphabetical sorting and saved picks.

## Artwork and performance

The illustrated iced coffees, hot chocolate, tea glass and mountain home were extracted from the user's own PDF vector artwork, rendered with transparency and compressed to WebP. The new visual category design adds watercolor food/coffee art and illustrations extracted from the bar PDF. See `MENU-IMAGERY.md` for provenance and generation prompts. These are category illustrations, not photographs of specific served items. The existing original English and Kurdish logos are reused. Fonts are self-hosted. The source PDFs are deliberately excluded from the website and GitHub; the menu does not download them.

Continuous motion can be paused and respects the operating system's reduced-motion setting. Only visible cards animate. There are no third-party trackers, remote font requests, frameworks or backend services.

`menu-source/social.html` is the 1200 × 630 source layout for the menu's social sharing image. The QR is high error-correction, with a four-module quiet zone. Use the A4 PDF linked above to print the 85 × 54 mm table cards.
