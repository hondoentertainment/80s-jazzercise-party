# 80s Jazzercise Party

Event website for the **80s Jazzercise Party** — **date TBD** · **6:30 PM** · **6900 East Greenlake Way N, Seattle** (Woodlawn entrance).

**Live site:** [80s-jazzercise-party.vercel.app](https://80s-jazzercise-party.vercel.app)

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

Smoke-test production:

```bash
python scripts/smoke-test.py
```

## What's included

- Hero with Richard Simmons–inspired poster, TBD date mode, QR code, and post-party mode
- **At the Party** hub — gallery, ice breakers, votes, and TV slideshow
- Photo gallery with optional moderation
- Best Outfit vote **by contestant number** (closes 9 PM party night when date is set)
- Printable contestant number tags
- Next-party poll saved to Blob
- **Host dashboard** — checklist, system status, live vote tally, quick links
- **Poll results dashboard** — date rankings and feedback
- Inline **80s fitness ice breakers** with shuffle deck
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
| Host dashboard | [/host.html](https://80s-jazzercise-party.vercel.app/host.html) |
| Gallery admin | [/admin.html](https://80s-jazzercise-party.vercel.app/admin.html) |
| Poll results | [/poll-results.html](https://80s-jazzercise-party.vercel.app/poll-results.html) |
| Print QR sign | [/qr.html](https://80s-jazzercise-party.vercel.app/qr.html) |
| Print number tags | [/numbers.html](https://80s-jazzercise-party.vercel.app/numbers.html) |
| Photo slideshow (TV) | [/slideshow.html](https://80s-jazzercise-party.vercel.app/slideshow.html) |
| Ice breakers | [/ice-breaker.html](https://80s-jazzercise-party.vercel.app/ice-breaker.html) |

## Party-night checklist

1. Set `GALLERY_ADMIN_CODE` in Vercel and redeploy
2. Set party date in `js/config.js` (see below) and redeploy
3. Print QR sign from [qr.html](https://80s-jazzercise-party.vercel.app/qr.html) → post at Woodlawn entrance
4. Print number tags from [numbers.html](https://80s-jazzercise-party.vercel.app/numbers.html) → hand out at the door
5. Test gallery upload + vote by number on a phone over **cellular**
6. Open [slideshow.html](https://80s-jazzercise-party.vercel.app/slideshow.html) on the TV
7. Open [ice-breaker.html](https://80s-jazzercise-party.vercel.app/ice-breaker.html) full-screen for warm-ups
8. Use [host.html](https://80s-jazzercise-party.vercel.app/host.html) during the party

## Custom domain

1. Vercel → **Settings → Domains** → add your domain
2. Update DNS per Vercel instructions
3. Change `SITE_URL` and `SHARE_MESSAGE` in `js/config.js`, regenerate QR, and redeploy

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
