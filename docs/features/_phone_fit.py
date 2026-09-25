"""Fit the 390x844 phone preview into whatever viewport it is handed.

CANONICAL HOME for phone-scaling, with one documented exception below.

WHY THIS EXISTS AS A MODULE. Six harnesses draw the same 390x844 phone. Two
had no scaling at all and cropped (the settings surfaces via _kit.py, and the
onboarding spine); two had grown their own near-identical `fit()` (the
first-run flow and the first-run export). Rather than write a fifth copy the
function moved here, and those four now share it (CLAUDE.md rule 2).

THE EXCEPTION: docs/features/my-home/build-home.py keeps its own. It is not
duplication left un-tidied — it measures a different thing. My Home draws a
physical bezel around the screen, so its outer box is 414x872 rather than
390x844; it allows scaling slightly UP (1.05) because that harness is
sometimes viewed alone; and it writes the scaled size back onto the phone's
wrapper so the caption beneath it sits tight. Generalising this module to
cover all three differences would make it worse for the four callers that
need none of them. If My Home ever loses its bezel, fold it in.

WHAT WAS ACTUALLY BROKEN. The Vercel dashboard embeds these in
`.flow-stage`, which is `height: min(1000px, calc(100vh - 260px))` with
`min-height: 720px`. On any normal laptop that resolves to ~720px. A phone
at natural size needs 844 plus the harness's own padding — about 912 — so
the bottom ~190px was cut off on every screen. Reported by the owner
2026-08-14 against the settings flows.

WHY TRANSFORM AND NOT A SMALLER PHONE. These prototypes are design
references: the phone has to keep meaning "390 x 844 points" or the type
sizes, tap targets and line breaks stop being reviewable. Scaling the whole
element preserves the design and only changes how big it appears. Resizing
the box would reflow the content into a device that does not exist.

WHY NOT PURE CSS. `transform: scale()` needs a unitless number, and CSS
cannot divide two lengths to produce one — `calc(100vh / 844px)` is invalid.
So the factor is measured in JS. `zoom` would work in current browsers but
it scales layout rather than paint, which reintroduces the reflow problem
above.

A scaled element still occupies its ORIGINAL size in layout, so every
harness that uses this puts the phone in a centred `.stage` that clips —
otherwise the unscaled 844px box keeps forcing a scrollbar even though the
phone now looks smaller.
"""

# Stage + phone geometry. Any harness including this gets a phone that is
# centred in the space left over, clips rather than scrolls, and scales about
# its own centre.
CSS = """
/* ---- fit-to-viewport (docs/features/_phone_fit.py) ---------------------
   The phone is scaled, never resized: it must keep meaning 390 x 844pt.
   `.stage` is what it is scaled to fit, and it clips, because a scaled
   element still takes up its full unscaled size in layout. */
.stage{flex:1;display:flex;align-items:center;justify-content:center;
  min-width:0;min-height:0;overflow:hidden;position:relative}
.phone{transform-origin:center center}
"""

# The measurement itself. Kept free of any harness's specifics — callers pass
# their own stage selector, padding and any sibling captions to subtract.
JS = """
/* fitPhone(opts) — scale .phone to fit .stage. See docs/features/_phone_fit.py
   opts: {phone, stage, padY, padX, subtract:[selector,...], min}
   `subtract` is for harnesses that put a caption in the stage beside the
   phone — My Home does — so the phone fits the space actually left. */
function fitPhone(opts){
  var o = opts || {};
  var p = document.querySelector(o.phone || '.phone');
  var st = document.querySelector(o.stage || '.stage');
  if (!p || !st) return;
  var sub = 0;
  (o.subtract || []).forEach(function(sel){
    var e = document.querySelector(sel);
    if (e) sub += e.offsetHeight;
  });
  var padY = o.padY == null ? 24 : o.padY;
  var padX = o.padX == null ? 24 : o.padX;
  var sc = Math.min(1,
    (st.clientHeight - padY - sub) / 844,
    (st.clientWidth - padX) / 390);
  /* A stage measured before layout settles can report 0; clamping keeps the
     phone visible instead of collapsing it to nothing. */
  p.style.transform = 'scale(' + Math.max(o.min == null ? 0.25 : o.min, sc) + ')';
}

/* Re-fit on anything that can change the space available. ResizeObserver
   rather than window resize alone: inside the Vercel dashboard these run in
   an iframe whose element can be resized without the inner window firing
   anything, which is exactly the case that was cropping. */
function watchPhoneFit(opts){
  var run = function(){ fitPhone(opts); };
  run();
  addEventListener('resize', run);
  addEventListener('load', run);
  if (window.ResizeObserver) {
    var st = document.querySelector((opts || {}).stage || '.stage');
    if (st) new ResizeObserver(run).observe(st);
  }
  /* Web fonts land after first paint and can change a caption's height. */
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(run);
  return run;
}
"""
