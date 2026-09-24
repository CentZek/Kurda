# Publish Kurda on Vercel

The site is ready to upload. No build command, database or environment variables are needed.

## 1. Import from GitHub

1. Sign in at https://vercel.com. Use a plan that permits commercial websites: Vercel's Hobby plan is limited to personal, non-commercial use.
2. Choose Add New > Project, connect GitHub if needed, and import `CentZek/Kurda`.
3. Use the `main` branch and leave Root Directory at the repository root (`./`).
4. The included `vercel.json` configures Framework Preset Other, no build or install command, and Output Directory `dist`. No environment variables are needed.
5. Click Deploy and open the resulting Vercel URL. Test the menu, mountain introduction, logo animation, telephone and email links on your phone.

The temporary `vercel.app` address has an intentional noindex header. The production domain remains indexable. This avoids search engines indexing a duplicate preview.

## 2. Connect kurda.com

1. In your Vercel project, open Settings > Domains.
2. Add `kurda.com` and `www.kurda.com`.
3. The site uses `https://kurda.com` as its primary address. The included configuration redirects `www.kurda.com` to it. Do not configure an opposite redirect from kurda.com to www.
4. Vercel will display the DNS records required for your project. At the company managing your domain's DNS, update the website records to those exact values (typically an A record for the root and a CNAME for www).
5. Preserve existing email MX records and TXT verification/SPF/DKIM records. Changing nameservers is not necessary for this workflow.
6. Wait until Vercel reports a valid configuration and HTTPS is ready. Check both addresses, email delivery and phone links before retiring the old hosting.

DNS values depend on the Vercel project, so they should be copied from your dashboard rather than a generic tutorial. Domain propagation can take time.

## 3. Check the live website and Google

- Open `https://kurda.com/` on a phone and computer; check the full page and mobile menu.
- Confirm `https://www.kurda.com/` ends at `https://kurda.com/`.
- Open `/robots.txt` and `/sitemap.xml`; confirm an unknown URL gives the branded 404 page with a 404 response.
- Verify `kurda.com` in Google Search Console, then submit `https://kurda.com/sitemap.xml` and inspect the homepage.
- Run Google's Rich Results Test and PageSpeed Insights against the final domain. Rankings and search snippets are controlled by Google; technical preparation does not guarantee either.

The longer mountain introduction remains as requested. Its deliberate delay can affect perceived loading and performance scores. Visitors can skip it, and reduced-motion preferences bypass it.

## Later updates

After connecting this repository, push website changes to `main` to update the production website automatically. Use a separate branch and pull request when you want to review a Vercel preview before merging.

Keep `vercel.json` at the repository root and website files in `dist/`. Edit those files directly; this is a static site with no build step.

## What was prepared

- Phone/tablet layout fixes, minimum touch target sizes for key actions, responsive grids and enlarged-text reflow.
- Image aspect ratios preserved; optimized local images and a self-hosted, swap-loaded font.
- Search title and description, canonical URL, social sharing tags, local business/service structured data, sitemap and robots.txt.
- Vercel redirects, static asset caching, basic response headers and a branded error page.
- The contact actions open email or phone apps; there is no booking form or server backend to configure.

Browser checks cover Chromium at eight viewport sizes from 320 to 1440 pixels, menu behavior, reduced-motion behavior, intro completion/skip, and enlarged text at 200%. They are browser emulation checks, not physical iPhone/Safari testing. Domain routing and Vercel-specific headers must be checked after deployment.

Official references: [Vercel GitHub integration](https://vercel.com/docs/git/vercel-for-github), [Hobby plan restrictions](https://vercel.com/docs/plans/hobby), [domain setup](https://vercel.com/docs/domains/working-with-domains/add-a-domain), [build settings](https://vercel.com/docs/builds/configure-a-build), [Google Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start).
