# Cowboy Disco Party

Event website for the **Cowboy Disco Party** — **date TBD** · **6:30 PM** · **6900 East Greenlake Way N, Seattle** (Woodlawn entrance).

**Live site:** [cowboy-disco-party.vercel.app](https://cowboy-disco-party.vercel.app)

## Quick start

```bash
npm install
npx serve .
```

Visit `http://localhost:3000`. API routes require Vercel or `vercel dev` locally.

Process hero image assets (after replacing the source JPG in project root):

```bash
python scripts/optimize-assets.py
```

Regenerate the printable QR code after changing `SITE_URL` in `js/config.js`:

```bash
python scripts/generate-qr.py
```

Smoke-test production:

```bash
python scripts/smoke-test.py
```

## What's included

- Hero with party poster, TBD date mode, QR code, and post-party mode
- **At the Party** hub — gallery, ice breakers, votes, and TV slideshow
- Photo gallery with optional moderation
- Best Outfit vote **by contestant number** (closes 9 PM party night when date is set)
- Printable contestant number tags
- Next-party poll saved to Blob
- **Host dashboard** — checklist, system status, live vote tally, quick links
- **Poll results dashboard** — date rankings and feedback
- Inline **cowboy-disco ice breakers** with shuffle deck
- PWA support, offline caching, and printable QR sign

## Deploy

```bash
git push origin main
npx vercel deploy --prod --yes
```

Create a **new** Vercel project for this repo (do not reuse the Canadian Tuxedo Party project). Connect Vercel Blob storage on first deploy.

## Environment variables (Vercel)

| Variable | Purpose |
|----------|---------|
| `BLOB_READ_WRITE_TOKEN` | Auto-set when Vercel Blob is connected |
| `GALLERY_ADMIN_CODE` | Host admin code — gallery moderation, poll results, host dashboard |
| `VOTE_CLOSE_TIME` | Optional ISO datetime for vote cutoff (set when party date is known) |
| `VOTE_MAX_NUMBER` | Optional max contestant number (default: 99) |

Gallery uploads support photos and videos up to **5 GB** via direct-to-Blob client uploads (multipart for files over 100 MB).

Set admin code:

```bash
npx vercel env add GALLERY_ADMIN_CODE production
```

## Host pages

| Page | URL |
|------|-----|
| Host dashboard | [/host.html](https://cowboy-disco-party.vercel.app/host.html) |
| Gallery admin | [/admin.html](https://cowboy-disco-party.vercel.app/admin.html) |
| Poll results | [/poll-results.html](https://cowboy-disco-party.vercel.app/poll-results.html) |
| Print QR sign | [/qr.html](https://cowboy-disco-party.vercel.app/qr.html) |
| Print number tags | [/numbers.html](https://cowboy-disco-party.vercel.app/numbers.html) |
| Photo slideshow (TV) | [/slideshow.html](https://cowboy-disco-party.vercel.app/slideshow.html) |
| Ice breakers | [/ice-breaker.html](https://cowboy-disco-party.vercel.app/ice-breaker.html) |
| Party planning (committee) | [/plan.html](https://cowboy-disco-party.vercel.app/plan.html) |

## Party planning workbook

The committee planning site at `plan.html` is admin-gated (same code as the host dashboard). It is generated from `Project Plan for the 41st Birthday Party.xlsx`.

After editing the Excel workbook, regenerate the embedded data:

```bash
python scripts/export-plan.py
```

Task status changes on the planning page are saved in the browser only. Re-export from Excel to refresh task text, schedule, signs, and committee roles.

## Party-night checklist

1. Set `GALLERY_ADMIN_CODE` in Vercel and redeploy
2. Set party date in `js/config.js` (see below) and redeploy
3. Print QR sign from [qr.html](https://cowboy-disco-party.vercel.app/qr.html) → post at Woodlawn entrance
4. Print number tags from [numbers.html](https://cowboy-disco-party.vercel.app/numbers.html) → hand out at the door
5. Test gallery upload + vote by number on a phone over **cellular**
6. Open [slideshow.html](https://cowboy-disco-party.vercel.app/slideshow.html) on the TV
7. Open [ice-breaker.html](https://cowboy-disco-party.vercel.app/ice-breaker.html) full-screen for warm-ups
8. Use [host.html](https://cowboy-disco-party.vercel.app/host.html) during the party

## Custom domain

1. Vercel → **Settings → Domains** → add your domain
2. Update DNS per Vercel instructions
3. Change `SITE_URL` and `SHARE_MESSAGE` in `js/config.js`, run `python scripts/generate-qr.py`, and redeploy

## Customize

- **Party date TBD mode:** `js/config.js` → `PARTY_DATE_TBD: true` (default until date is set)
- Party date / countdown: `js/config.js` → set `PARTY_DATE_TBD: false`, then `PARTY_DATE`, `PARTY_END`, `VOTE_CLOSE_TIME`
- Max contestant number: `js/config.js` → `VOTE_MAX_NUMBER`
- Default tag count: `js/config.js` → `VOTE_TAG_COUNT`
- Site URL / QR / Open Graph: `js/config.js` → `SITE_URL`
- Guest invite text: `js/config.js` → `SHARE_MESSAGE`

When the date is set:

```javascript
PARTY_DATE_TBD: false,
PARTY_DATE: "2026-XX-XXT18:30:00-07:00",
PARTY_END: "2026-XX-XXT22:00:00-07:00",
VOTE_CLOSE_TIME: "2026-XX-XXT21:00:00-07:00",
```

Then update schedule table datetimes in `index.html`, footer date lines, meta descriptions, and redeploy.
