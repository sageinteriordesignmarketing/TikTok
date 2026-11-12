# Installing the homepage on the hidden "Home V2 (Draft)" page

This puts the approved v4 design onto **Home V2 (Draft)** only, so it looks exactly like the preview.

**Nothing else on the site changes.** Everything lives inside one Code Block on that page:
- every style rule is scoped to that page
- the script and fonts only load there
- nothing goes into the site-wide Custom CSS, site-wide Code Injection or Site Styles

Do **not** paste any of this into Website › Custom Code › Custom CSS or Settings › Advanced › Code Injection.
Those affect every page.

## What you'll paste

| File | Where it goes | When |
| --- | --- | --- |
| `1-code-block.html` | One **Code Block** on the draft page | Now |
| `2-homepage-header-injection.html` | Real homepage › Settings › Advanced › **Page Header Code Injection** | At launch only |

`1-code-block.html` holds everything: layout, styles, a small script, fonts, and every photo.
The photos load from the images **already in her Squarespace library**, so nothing needs uploading.
They use responsive sizes (750 / 1500 / 2500 px), so phones download small files.

## Before you start

- **Plan:** Code Blocks that run JavaScript need a Squarespace plan that allows custom code
  (Core/Business or higher). Check under Settings › Billing. On a plan without custom code,
  the layout still shows but the menu button and scroll fade-ins won't work.
- **Leave Site Styles alone.** The code switches off Squarespace's block animations and spacing for
  this page only.

## Steps (about 5 minutes)

1. **Pages** › Not Linked › open **Home V2 (Draft)**.
2. Delete the sections already on that page, so it's empty.
3. **Add Section** › choose any blank section › **Add Block** › **Code**.
4. Open the Code Block, delete its sample text, and paste the **entire** contents of `1-code-block.html`.
   - Make sure **Display Source** is OFF.
   - Leave the mode on HTML.
5. Don't add any other blocks to that section. The code makes its section full-width and hides the
   site's normal header and footer **on this page only**, because the design has its own.
6. On **Home V2 (Draft)'s** own gear icon › **SEO**, turn ON *Hide page from search engines*. This is a
   page-level setting. Your page shows greyed out, which means it's disabled, so the public can't see it anyway.
7. **Save**, exit the editor, and view the page while you're **logged in**. A disabled page can't be
   opened in a private window.
   - Squarespace pauses scripts in edit mode, so the editor won't show the menu or fade-ins.
     The page will once you exit the editor.

### Check it

- The page looks like `previews/desktop-*.png` and `previews/mobile-*.png`.
- MENU opens the full-screen menu, and Escape closes it.
- The project strip scrolls sideways (drag with a mouse, swipe on a phone).
- *View page source* › search for `<h1`. There should be exactly **one**.

## Things to know

- **Fonts:**
  - Proxima Nova (labels and navigation) comes from her site's existing font settings, so it's the real brand font.
  - Bodoni Moda (headings) and Spectral (text) load from Google Fonts inside the code.
- **Links to pages that don't exist yet:** the Residential, Commercial, Hospitality, Construction
  Documents, San Luis Obispo and Boise links use the new URLs from the copy doc. They'll 404 until
  those pages are built. Build them, or hold off on launch.
- **Older browsers:** hiding the native header and footer uses the CSS `:has()` selector (Safari 15.4+,
  Chrome 105+, Firefox 121+). On older browsers the normal Squarespace header simply shows above the
  design. Nothing breaks.
- **Editing copy later:** edit the text directly in the Code Block. Or change `homepage-concept.html`
  and run `python3 squarespace/build.py` to regenerate this file.
- **Header and footer on other pages:** this design's header and footer exist only on this page.
  Phase 2 is restyling the native Squarespace header and footer site-wide to match, so every page
  shares the look.

## At launch (when the draft is approved)

1. On the draft page: **Page Settings › General › Set as Homepage**.
2. **Page Settings › SEO**, using the copy doc:
   - SEO title: `Design Collaborative | Luxury Interior Design San Luis Obispo`
   - Description: `Luxury interior designers for Central Coast and Idaho homes and businesses, with construction-ready drawings that carry your project to the finish.`
   - Turn OFF *Hide page from search engines*.
3. On this page's own **Page Settings › Advanced › Page Header Code Injection** (page-level, not the site-wide one), paste `2-homepage-header-injection.html`.
   This is the structured data for both offices.
4. Disable or delete the old homepage, and fix the footer "Home" link from `/home` to `/`.
5. Test with Google's Rich Results Test, then request indexing in Search Console.
