# Design Collaborative: Homepage Concept (Round 4)

**v4 (current) follows Studio Krista's client sites.** I studied cocomaisondesign.com, fullhousegroup.uk, michaellondon.com,
stephenyoungdesign.com, dartstudio.ca, opa.space and greyinteriors.co.uk. The patterns carried over:
- a filmic full-screen hero under a warm tint, with a centred statement and a scroll cue
- a MENU button that opens a full-screen overlay (Squarespace: force the native mobile menu on at all widths)
- Didot-style serif headings with italic accents, mixed with tracked uppercase sans
- overlapping photo collages beside centred text
- a row of tall portrait service panels
- warm taupe, cream and olive grounds, with a black gallery chapter for projects
- links that start with a short horizontal rule
- an olive footer with italic serif column labels

**Fonts:** Bodoni Moda for headings (Google Fonts, added via Code Injection), and DC's existing Proxima Nova for text.
The preview substitutes Figtree for Proxima. Photography comes from the live DC site.
Earlier rounds are kept as `homepage-concept-v1/v2/v3.html`.

A working visual preview of the new homepage, built from the approved copy in
*DRAFT 1 - Design Collaborative SEO Website Copywriting* (Home tab). This round is for **review only**.
Nothing here has been put into Squarespace yet.

| File | What it is |
| --- | --- |
| `homepage-concept.html` | The full homepage concept, responsive on desktop and phone, with all copy, links, and structured data |
| `design-system.html` | Visual identity board covering palette, type scale, motifs, components, grid, and principles |
| `images/` | Drop photography here using the file names below. The concept picks it up automatically |

## Viewing it

Open `homepage-concept.html` in any browser. Until real photos are added, each frame shows a
tonal placeholder with a label naming the shot it needs. You can preview photos in two ways:

1. **Drag a photo** from your computer onto any frame. This lasts for that browser session only.
2. **Save the photos** into `images/` using these names (they double as the SEO file-name plan):

| Frame | File name | Crop |
| --- | --- | --- |
| Hero (main) | `bluff-estate-shell-beach-staircase.jpg` | Portrait 4:5, 2500px long side |
| Hero (arched detail) | `gold-coast-spanish-avila-beach-hand-painted-tile.jpg` | 3:4.3 |
| Introduction (arch) | `gold-coast-spanish-avila-beach-limestone-fireplace.jpg` | 3:4.2 |
| Services hover: Residential | `residential-interior-design-living-room.jpg` | 4:5 |
| Services hover: Hospitality | `hospitality-interior-design-boutique-hotel.jpg` | 4:5 |
| Services hover: Commercial | `commercial-interior-design-imdex-office.jpg` | 4:5 |
| Services hover: Construction | `interior-design-construction-documents-sheet.jpg` | 4:5 |
| Who we work with (full-bleed) | `luxury-residential-interior-design-great-room.jpg` | 16:7 desktop, 4:5 phone |
| Two homes: California | `interior-designer-san-luis-obispo-central-coast.jpg` | 4:5 |
| Two homes: Idaho | `interior-designer-boise-idaho-mountain-home.jpg` | 4:5 |
| Project: Bluff Estate | `bluff-estate-shell-beach-reflecting-pool.jpg` | 4:3 |
| Project: Gold Coast Spanish | `gold-coast-spanish-avila-beach-living-room.jpg` | 3:4 |
| Project: El Hacón | `el-hacon-san-luis-obispo-hillside-home.jpg` | 4:5 (arched) |
| Project: Paris Valley Road | `paris-valley-road-estate-winery-paso-robles.jpg` | 3:2 |
| Closing (arch) | `design-collaborative-interior-evening.jpg` | 3:4 |

## What was preserved from the copy doc

- Every word of the Home tab copy, in the original order, as crawlable HTML text.
- SEO title, meta description, and **one H1** ("Luxury Interior Designers in San Luis Obispo and Boise").
- Heading outline: H1 → 8 × H2, one per section → H3 for the four services, three steps, and four projects.
- Internal links, all with descriptive anchor text: Residential, Hospitality, Commercial, Construction
  Documents (twice), both location pages (section and footer), all four project pages (per the
  implementation note), Selected Works, and Inquire.
- Organization + InteriorDesigner (LocalBusiness) JSON-LD for both offices.
- Project URLs use the new slugs from each project tab (Bluff Estate → `/selected-works/shell-beach-house`).

## Added for design or accessibility (please review)

- **Alt text** on every image follows the pattern in the copy doc. The hero uses the doc's example verbatim.
  The rest are drafts written to the shot list, so update them once the real photos are chosen.
- **Decorative only, hidden from screen readers and minor in content:** section folio numerals (01)–(07),
  service numerals i–iv, the "&" ornament, the office coordinates, image captions naming the project, and
  the drawn kitchen elevation in the construction section. None of these add marketing copy.
- **Footer:** office addresses and phone numbers are taken from the Inquire tab. The footer line
  "NCIDQ-certified interior designers · San Luis Obispo & Boise" is new, so cut it if you'd rather not have it.

## Performance budget

- Fonts: 2 families (Cormorant Garamond 300/400 + italics, Jost 300/400/500) via Google Fonts, both
  available natively in Squarespace's font picker.
- JavaScript: about 2 KB for reveals, the header state, and the services hover image. No libraries.
- The hero image is eager with `fetchpriority="high"`. Everything below the fold lazy-loads.
- Everything renders without JavaScript and respects `prefers-reduced-motion`.

## Next step (after approval)

A Squarespace 7.1 implementation pack:
1. Site Styles settings (colors, fonts, buttons) to set natively.
2. One global Custom CSS file (tokens, header, footer, components).
3. Per-section Code Block HTML, with images uploaded to Squarespace and served via the CDN with `srcset`.
4. A Footer Code Injection script and the homepage Header Code Injection JSON-LD.
5. A map of which sections stay native (header, footer, and optionally the text blocks) and which are custom,
   with the trade-off for each in editability.
