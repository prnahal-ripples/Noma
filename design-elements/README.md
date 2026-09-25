# Design elements — approved component registry

Real, running components skinned with NOMA tokens — not mockups. Each lives in
its own folder with its own README covering derivation, verification status,
and open gaps. This file is the index; **`.claude/rules/design-system.md`
Approved Components is the gate** — a component is "in the design system" once
it has a row there, not merely because a folder exists under here.

| Component | What it is | Formats | Status |
|---|---|---|---|
| **[Bottom Sheets](./bottom-sheets/)** | [`@magic-spells/bottom-sheet`](https://github.com/magic-spells/bottom-sheet) + [`dialog-panel`](https://github.com/magic-spells/dialog-panel), restyled — 10 sheet types (basic, action menu, confirmation, scrollable, snap points, inset, form, filter, detail, media) | Static HTML/CSS | Built, runs, gesture physics vendored untouched |
| **[Bottom Navigation Bar](./bottom-nav/)** | Minimizable floating tab bar, iOS 26/27 Liquid Glass pattern — rebuilt from a Kavsoft SwiftUI tutorial by stepping the reference video frame by frame | SwiftUI package + static HTML mobile-preview | HTML: built, runs, verified in-browser (measured, not eyeballed). SwiftUI: builds clean, **never executed** — see its README's verification table |
| **[3D Icons](./3d-icons/)** | Tier-1 icon set (info, appearance, notifications, family) — the higher-visibility half of a two-tier system, tier 2 being the flat monoline icons already in `_kit.py` | PNG source + 288px WebP derivatives under `web/` | Files present (owner pasted them 2026-08-14), all four live as L2 page headers in both settings prototypes, verified in-browser. **Two open palette conflicts** on appearance and notifications — see the folder manifest |
| **[Engraved icons](./engraved-icons/)** | A third icon register — large glyphs pressed into the surface (Bluetooth, Wi-Fi, check, notifications), one per page | Owner SVG, embedded as data URIs | Live on four first-run nodes. ⚠ **Neither of the icon gate's two tiers** — that rule is now wrong as written; see the folder README |
| **[Brand](./brand/)** | The real NOMA wordmark — one static mark, not a set | PNG source + 640px WebP derivative | Live in the sign-in flow (splash + login sheet), verified in-browser. **Not a component or an icon set** — neither existing gate fits it; see the folder README |

## Why both are here, and why one is "more done" than the other

**Bottom Sheets and the Bottom Navigation Bar's HTML preview are both proven —
opened in a browser, exercised, and checked against numbers, not just looked
at.** The Bottom Navigation Bar's *SwiftUI* package is the one asterisk in
this registry: there is no Xcode on the machine that built it, only Command
Line Tools, so it typechecks and builds for macOS but has never run on a
simulator or device. That distinction is carried in the component's own
README, not smoothed over here — **verified** and **builds but unverified**
are different claims and this index does not conflate them.

**3D Icons has since stopped being an asterisk of that kind.** It was listed
here while it was an empty scaffold — a folder waiting on asset files, with
nothing to verify. The owner pasted the four PNGs in on 2026-08-14, and they
are now normalised, re-encoded to WebP for embedding, and rendering as page
headers on four L2 screens across the two settings prototypes, checked in a
browser rather than assumed. What it still does not have is a row in
Approved Components, and that is deliberate: two of the four icons carry
colours outside the product's own two-green rule (the painter's palette, the
red notification badge). Whether a 3D render of a real-world object is bound
by a rule written for the product's own surfaces is an owner call, not
mine — so the gate stays uncleared until that call is made.

## Adding a component here

1. Build it in its own folder, README included, following the shape of the
   two above (derivation, tokens used, motion-gate compliance, verification
   status stated honestly — including what was *not* checked and why).
2. Add a row to the table above.
3. Add it to **Approved Components** in
   [`.claude/rules/design-system.md`](../.claude/rules/design-system.md) — that
   list is the actual gate; this README is the map to it.
4. If it's the app's first native (non-web) component in a given
   stack, say so — it's the kind of fact that changes what "the repo has no
   application code" (`memory/session-handoff.md`) still means.

⚠ **No `templates/` entry exists for "new design-system component."**
CLAUDE.md rule 5 requires every new event, persona, feature or motion pattern
to start from a `templates/` file — components are not in that list, and
neither Bottom Sheets nor the Bottom Navigation Bar started from one. Not a
new gap introduced here — bottom-sheets already set this precedent — but
worth an owner decision before a third component makes it a firm pattern.
