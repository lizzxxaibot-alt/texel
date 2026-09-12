// Texel Density — one-page reference.
// Every figure is read from tables.json, which make_tables.py computes by
// running core/uvmap.py OUT OF THE SHIPPED ZIP. Do not type a number into this
// file; add it to the generator instead.
#let d = json("tables.json")

#let ink    = rgb("#26241e")
#let charc  = rgb("#141317")
#let muted  = rgb("#6f6a5e")
#let hair   = rgb("#d9d2c2")
#let ground = rgb("#fbf6ea")
#let panel  = rgb("#f3ecdb")
#let ember  = rgb("#c4581a")
#let gold   = rgb("#9a6b0f")

// A4 by default; `typst compile --input paper=us-letter` builds the US sheet.
// US Letter is 17.6mm SHORTER than A4, so it gets tighter margins or the
// content spills to a second page - which build.py refuses to ship.
#let paper = sys.inputs.at("paper", default: "a4")
#let letter = paper == "us-letter"

#set page(
  paper: paper,
  margin: (x: if letter { 11mm } else { 13mm },
           top: 0mm, bottom: if letter { 7mm } else { 10mm }),
  fill: ground,
  footer: context [
    #set text(7.2pt, fill: muted, font: "IBM Plex Mono")
    #grid(columns: (1fr, auto),
      align: (left, right),
      [Made by Pixelkiln · Released CC0 — use it, print it, put it in your wiki],
      [z3er1n.itch.io/texel],
    )
  ],
)
#set text(font: "Newsreader 16pt", size: 8.9pt, fill: ink)
#set par(leading: 0.48em, justify: false)

#let mono(x) = text(font: "IBM Plex Mono", size: 8.4pt, x)
#let lbl(x) = text(font: "Sora", size: 7.4pt, fill: gold, weight: 600,
                   tracking: 0.09em, upper(x))
#let hd(n, x) = block(above: 8pt, below: 4pt)[
  #grid(columns: (auto, 1fr), gutter: 7pt, align: horizon,
    text(font: "IBM Plex Mono", size: 8pt, fill: ground,
         box(fill: ember, inset: (x: 4pt, y: 2.5pt), radius: 1.5pt, [#n])),
    text(font: "Sora", size: 11pt, weight: 600, fill: charc, x))
]

// ---------------------------------------------------------------- masthead
#block(fill: charc, width: 100%, inset: (x: 0mm, y: 5mm), outset: (x: if letter { 11mm } else { 13mm }))[
  #grid(columns: (1fr, auto), column-gutter: 10mm,
        align: (left + bottom, right + bottom),
    [
      #text(font: "Young Serif", size: 23pt, fill: rgb("#fff8ec"))[Texel density]
      #v(5pt, weak: true)
      #text(font: "Newsreader 16pt", size: 10pt, fill: rgb("#c9bfa8"))[
        How many texture pixels land on one metre of model — and how to make that
        one number true everywhere in a scene.]
    ],
    [#text(font: "IBM Plex Mono", size: 7.2pt, fill: rgb("#e7b23a"), tracking: 0.14em)[
      ONE-PAGE REFERENCE \
      FOR PIXEL ART ON 3D]],
  )
]
#v(5pt)

// ---------------------------------------------------------------- formula
#block(fill: panel, width: 100%, inset: 7pt, radius: 2pt, stroke: 0.5pt + hair)[
  #grid(columns: (1fr, 1fr), gutter: 10pt,
    [
      #lbl[The whole thing]
      #v(3pt, weak: true)
      #mono[px/unit = sqrt( UV area × S² ÷ world area )]
      #v(3pt, weak: true)
      #text(size: 8.4pt, fill: muted)[
        #mono[S] is the texture's longest edge in pixels; world area is in m²,
        measured #emph[after] object scale.]
    ],
    [
      #lbl[The form you will actually use]
      #v(3pt, weak: true)
      #mono[px/unit = S ÷ M]
      #v(3pt, weak: true)
      #text(size: 8.4pt, fill: muted)[
        …for a square face that uses the whole #mono[S×S] texture and spans
        #mono[M] metres. A 64 px texture across 2 m is 32 px/unit.]
    ])
]

// ---------------------------------------------------------------- step 1
#hd(1)[Pick one density for the whole game, and make it a power of two]

#grid(columns: (1.02fr, 1fr), gutter: 11pt, align: top,
  [
    #table(
      columns: (auto, 1fr, 1fr, auto),
      stroke: none,
      inset: (x: 4pt, y: 3.4pt),
      fill: (_, y) => if y == 0 { charc } else if calc.odd(y) { panel } else { none },
      table.header(
        ..([px/unit], [#d.character_m m character], [1 m floor tile], [0.5 m prop])
          .map(h => text(font: "Sora", size: 7.2pt, weight: 600,
                         fill: rgb("#f2e6c8"), tracking: 0.05em, upper(h)))),
      ..d.ladder.map(r => (
        text(font: "IBM Plex Mono", size: 9pt, weight: 700, fill: ember)[#r.d],
        mono[#r.char_px px tall],
        mono[#r.tile_px × #r.tile_px px],
        mono[#r.half_px px],
      )).flatten(),
    )
  ],
  [
    #strong[Why a power of two, and not a round character height.] You can have
    one or the other, never both. At #mono[32] px/unit a 0.5 m prop gets exactly
    #mono[16] px and its edges land on texel corners. Solve instead for a
    character exactly 32 px tall and the density becomes #mono[17.8] px/unit —
    that same prop now gets #mono[8.9] px, and every object in the scene sits
    half a texel off the grid.

    #v(3pt)
    Density is inherited by #emph[everything else in the level]; the character is
    one object. Round the number that propagates.
  ])

// ---------------------------------------------------------------- step 2
#hd(2)[Size every texture from that one number]

#table(
  columns: (1.5fr,) + (auto,) * 8,
  stroke: none,
  inset: (x: 3.5pt, y: 3.2pt),
  align: (left,) + (center,) * 8,
  fill: (_, y) => if y <= 1 { charc } else if calc.even(y) { panel } else { none },
  table.header(
    table.cell(rowspan: 2, align: left + horizon,
      text(font: "Sora", size: 7.2pt, weight: 600, fill: rgb("#f2e6c8"),
           tracking: 0.05em)[LONGEST EDGE]),
    ..d.densities.map(x => table.cell(colspan: 2, align: center,
      text(font: "Sora", size: 7.2pt, weight: 600, fill: rgb("#e7b23a"))[#x px/unit])),
    ..d.densities.map(_ => (
      text(font: "IBM Plex Mono", size: 6.4pt, fill: rgb("#9a9187"))[needs],
      text(font: "IBM Plex Mono", size: 6.4pt, fill: rgb("#9a9187"))[use],
    )).flatten(),
  ),
  ..d.grid.map(r => (
    [#text(size: 8.6pt)[#r.name] #h(3pt) #text(font: "IBM Plex Mono", size: 7pt,
      fill: muted)[#r.m m]],
    ..r.cells.map(c => (
      text(font: "IBM Plex Mono", size: 7.6pt, fill: muted)[#c.need],
      text(font: "IBM Plex Mono", size: 8.2pt, weight: 700, fill: charc)[#c.tex],
    )).flatten(),
  )).flatten(),
)
#v(3pt)
#text(size: 8.4pt, fill: muted)[
  #strong[needs] = density × metres, the exact pixel count. #strong[use] = the
  next power of two, because that is what the GPU wants and what keeps mipmaps
  honest. Round #emph[up]: a texture larger than needed wastes memory, a texture
  smaller than needed is the blur you were trying to avoid.]

// ---------------------------------------------------------------- step 3
#hd(3)[Expect it to drift, because the default unwrap guarantees it]

#grid(columns: (1fr, 0.88fr), gutter: 11pt, align: top,
  [
    Unwrap a cube in Blender and you get the same UV layout whatever size the
    cube is. #mono[UV area] is therefore constant while #mono[world area] is not,
    so density falls as #mono[1 ÷ size] — and the spread across a scene comes out
    as #emph[exactly the size ratio of its objects].

    #v(4pt)
    A #mono[#d.drift.wall_m m] wall beside a #mono[#d.drift.crate_m m] crate is a
    ratio of #mono[#d.drift.ratio×]. Measured on that scene across
    #mono[#d.drift.faces] faces on one #mono[#d.drift.tex px] texture, Blender
    reported:

    #v(4pt)
    #block(fill: panel, width: 100%, inset: 6pt, radius: 2pt, stroke: 0.5pt + hair)[
      #mono[#d.drift.before]
      #v(2pt, weak: true)
      #text(size: 7.6pt, fill: muted)[…and after correcting every face:]
      #v(2pt, weak: true)
      #mono[#d.drift.after]
    ]
    #v(4pt)
    #text(size: 8.4pt, fill: muted)[
      This is why one wall in a corridor reads crisp and the crate in front of it
      reads mushy, on the same texture, at the same distance.]
  ],
  [
    #lbl[The correction]
    #v(3pt, weak: true)
    A face of area #mono[A] m² needs a UV island whose side covers this fraction
    of the texture:
    #v(4pt)
    #block(fill: panel, width: 100%, inset: 6pt, radius: 2pt, stroke: 0.5pt + hair)[
      #align(center, mono[UV side = D × sqrt(A) ÷ S])]
    #v(5pt)
    #lbl[Worked]
    #v(3pt, weak: true)
    #text(size: 8.4pt)[
      A #mono[#d.example.w × #d.example.h m] panel (#mono[#d.example.area m²]) at
      #mono[#d.example.d px/unit] on a #mono[#d.example.s px] texture:
      #v(2pt, weak: true)
      #mono[#d.example.d × sqrt(#d.example.area) ÷ #d.example.s = #d.example.uv]
      #v(2pt, weak: true)
      so the island spans #mono[#d.example.uv_pct%] of UV space, about
      #mono[#d.example.px_across px] across. Scale the island to that and the
      face measures back at exactly #mono[#d.example.d].]
    #v(5pt)
    #text(size: 8pt, fill: muted)[
      Over #mono[1.0] means the face needs more pixels than the texture has —
      tile it, or move up a texture size.]
  ])

// ---------------------------------------------------------------- gotchas
#hd(4)[Four things that quietly make the number a lie]

#grid(columns: (1fr, 1fr), gutter: 11pt, align: top, row-gutter: 4pt,
  [#strong[Unapplied object scale.] Density is measured in world space. A cube
   scaled #mono[2×] in the viewport is twice the size the mesh data thinks it is.
   #mono[Ctrl+A -> Scale] before you measure anything.],
  [#strong[Non-uniform scale.] Scale #mono[x] but not #mono[y] and the face has
   two different densities at once. No single number describes it; fix the scale
   rather than the UVs.],
  [#strong[Linear filtering.] Perfect density with a smoothed texture still looks
   like mud. Set the image node's interpolation to #strong[Closest] — the one
   people check last and should check first.],
  [#strong[Mixed texture sizes.] Two objects can share a density without sharing
   a texture. The density is what must match across the scene; the texture size
   is per object, and step 2 is how you pick it.],
)

#v(4pt)
#block(width: 100%, inset: (y: 5pt), stroke: (top: 0.6pt + hair))[
  #grid(columns: (1fr, auto), align: (left + horizon, right + horizon), gutter: 8pt,
    [#text(size: 8.4pt)[
      Every figure here is computed by running #mono[core/uvmap.py] out of the
      shipped #mono[texel-0.2.0.zip] — the same arithmetic the add-on runs — not
      typed in. The generator is in the download.]],
    [#stack(dir: ttb, spacing: 4pt,
      text(font: "Sora", size: 8pt, weight: 600, fill: charc)[
        Texel measures and applies this for you],
      align(right, text(font: "IBM Plex Mono", size: 7.6pt, fill: ember)[
        z3er1n.itch.io/texel]))],
  )
]
