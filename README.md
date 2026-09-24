# Kurda catering redesign

A static, responsive website. The complete deliverable is in `dist/`. No build step or runtime dependencies are required. Serve that directory with any static web server.

Import `CentZek/Kurda` into Vercel with the repository root as Root Directory. The included `vercel.json` serves `dist/` with no build or install step. Follow [VERCEL-DEPLOYMENT.md](VERCEL-DEPLOYMENT.md) for domain setup and future updates.

Business content and contact details were checked against https://kurda.com/ on 24 September 2026. The source image collection remains untouched in the parent workspace. Optimized assets are stored locally; food and kitchen photographs come from the existing Kurda website. DM Sans is self-hosted with font-display: swap and local fallback fonts. Its OFL license is included in assets.

Interactions: anchor navigation, a keyboard-accessible mobile menu, email and telephone links, intersection-based section reveals, gentle scroll parallax and stacking service cards on desktop and mobile. Native scrolling is preserved. Reduced-motion preferences disable animated motion and stacking. Contact links open the visitor's email or telephone application; there is no simulated form submission or booking backend.

The home page opens with a brief mountain reveal, with Skip intro and Escape controls, reduced-motion and direct-anchor bypasses, and a bounded fail-open timeout. Heritage artwork uses its natural aspect ratio in the document flow; the family photograph is displayed uncropped.

The mountain introduction holds for 2.8 seconds after assets are ready, then parts over 2.3 seconds. The hero uses the existing Kurdish PNG with sequential SVG reveal masks; its sun is visible from the start, and only the white lettering paints beneath it. The sun and lettering are isolated by their actual colors, so the sun layer cannot include a white stem. Reduced-motion users see the completed mark immediately. A nine-second hard deadline keeps the introduction from blocking access.

The lower reveal follows the original curved stroke. All lettering is covered by the animated mask itself, without a finishing overlay or displaced edges. Mask coverage is checked against the original lettering pixels.

Service cards use their measured height and the small viewport height to set the sticky position. Oversized cards scroll through their content before pinning, including on phones, landscape screens and enlarged text. ResizeObserver updates the measurement when fonts or layout change.
