# Kurda table menu

## Open the menu

- Published preview path on the existing production site: `https://kurda.com/menu/`
- Intended permanent table-menu address: `https://menu.kurda.com/`
- Printable A6 table card: `https://kurda.com/menu/qr/table-card.html`
- Standalone QR files: `/menu/qr/kurda-menu-qr.svg` and `/menu/qr/kurda-menu-qr.png`

The QR encodes **https://menu.kurda.com/**. Confirm that address works over HTTPS on a phone before printing cards for customers. The QR remains the same when prices or dishes change.

## Connect menu.kurda.com

1. Open the existing **Kurda** project in Vercel, then **Settings → Domains**.
2. Add **menu.kurda.com** to **Production**. Do not choose a redirect to the main website.
3. Copy the exact CNAME target shown by Vercel for this subdomain.
4. In the existing DNS provider / cPanel Zone Editor for `kurda.com`, add one record:

   | Type | Name | Target | TTL |
   | --- | --- | --- | --- |
   | CNAME | `menu` (or `menu.kurda.com.` if the editor expects a full name) | Exact target Vercel displays | `300`, if supported |

5. Wait for Vercel to report **Valid Configuration**, then open `https://menu.kurda.com/` on a phone and check categories, images and prices.

Do not change nameservers, apex/www, mail records, or any other subdomain. Existing POS, inventory and other applications keep their own DNS records. Keep the current DNS/mail hosting active.

If `menu` already has a record, inspect it first instead of creating a conflicting CNAME. As checked during implementation on 22 October 2026, `menu.kurda.com` did not resolve publicly. Domain attachment and DNS changes still require dashboard access; publishing the code does not create DNS records.

## Routing

This remains a single buildless Vercel project. Explicit ordered routes in `vercel.json` send only `menu.kurda.com/`, its robots file, and its sitemap to the menu files **before** the filesystem phase. This avoids the existing root `index.html` winning over the subdomain route. The original homepage and its assets are unchanged. Existing security/cache headers, www redirect, legacy index redirects and preview noindex headers are retained.

References: [Vercel domain setup](https://vercel.com/docs/domains/working-with-domains/add-a-domain), [host-based routing](https://vercel.com/kb/guide/can-i-redirect-from-a-subdomain-to-a-subpath), [route configuration](https://vercel.com/docs/project-configuration/vercel-json).

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
