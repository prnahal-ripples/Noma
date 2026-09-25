# Product renders — the three purifier SKUs

Owner-supplied, 2026-08-17. Real photography of `HW-PUR-200` / `500` / `MAX`
(src/hardware/devices.json), replacing the CSS-drawn purifier everywhere a
purifier is depicted in first run: the node-6 chooser thumbnails, the filter
unwrap, the plug-in scene and the Bluetooth scenes. The node-9 Wi-Fi light
stays drawn — the owner called that one fine as is.

| File | SKU | Source (repo copy) | web/ |
|---|---|---|---|
| `air-pro-200.png` | HW-PUR-200 | 1200px working copy | 427×640 webp |
| `air-pro-500.png` | HW-PUR-500 | 1200px working copy | 332×640 webp |
| `air-pro-max.png` | HW-PUR-MAX | 1200px working copy | 524×640 webp |

**Provenance.** Supplied as `~/Downloads/200.png` / `500.png` / `Max.png` —
3840–7680px, 5–32 MB, real alpha. The repo keeps a 1200px working copy rather
than the originals (32 MB of PNG in a design repo helps nobody); if print-res
is ever needed, the originals are the owner's masters, not this folder.

**The crop.** Each render carries a very wide, very faint floor shadow. The
crop keeps the product plus 8% lateral air and a little grounding shadow under
the base, and cuts the rest — a contain-fit of the raw bbox made the product
tiny inside its own image.

**Consumers.** `docs/features/first-run/build-prototype.py` embeds the `web/`
derivatives as CSS variables (`--rnd200` / `--rnd500` / `--rndmax`); every
rendering of the flow inherits them from there. Replace a file here and re-run
the builders — no code change.

⚠ These are marked `prototype-only` in spirit, like the SKU specs: nobody has
confirmed these renders are the shipping industrial design.
