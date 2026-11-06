"""Line artwork, drawn once, in the brand palette.

Technical drawings rather than fake renders: they are what the object is, drawn
to scale-ish, with dimensions. Nothing here pretends to be a photograph.
"""

NAVY = "#173D7A"
RED = "#C8102E"
INK = "#0F1A2C"
SKIN = "#F6D8CE"
FAT = "#FBE8DF"
MUSC = "#E9B4A6"
RIB = "#D8C9C2"
LUNG = "#DCE4F1"
CREAM = "#FFFCFA"


def _band(y, h, fill, curve=6):
    """A soft horizontal layer with a gentle anatomical curve."""
    y2 = y + h
    return (
        f'<path d="M28 {y} C 160 {y - curve} 360 {y + curve} 492 {y} '
        f'L 492 {y2} C 360 {y2 + curve} 160 {y2 - curve} 28 {y2} Z" fill="{fill}"/>'
    )


def chest_section():
    return f"""<svg class="chestwall" viewBox="0 0 560 560" role="img" aria-label="A cross-section through the chest wall: the stethoscope head on the skin, and the sound losing its high frequencies as it crosses fat, muscle and rib.">
  <defs>
    <clipPath id="cw">
      <rect x="24" y="104" width="404" height="356" rx="8"/>
    </clipPath>
  </defs>

  <g clip-path="url(#cw)">
    {_band(104, 14, SKIN, 4)}
    {_band(118, 92, FAT, 5)}
    {_band(210, 74, MUSC, 5)}
    {_band(284, 34, RIB, 3)}
    {_band(318, 22, "#F3E9E4", 4)}
    {_band(340, 120, LUNG, 6)}
  </g>
  <rect x="24" y="104" width="404" height="356" rx="8" fill="none" stroke="{NAVY}" stroke-width="1" opacity="0.18"/>

  <!-- the sound, losing its top end -->
  <g stroke="{RED}" fill="none" stroke-linecap="round">
    <path d="M150 120 C 184 158 116 196 150 232 C 184 268 116 306 150 342" stroke-width="2.8" opacity="0.9"/>
    <path d="M196 120 C 230 158 162 196 196 232 C 230 268 162 306 196 342" stroke-width="2.1" opacity="0.55"/>
    <path d="M242 120 C 276 158 208 196 242 232 C 276 268 208 306 242 342" stroke-width="1.4" opacity="0.3"/>
  </g>

  <!-- stethoscope head -->
  <g stroke="{NAVY}" fill="none" stroke-width="2">
    <circle cx="150" cy="74" r="32" fill="{CREAM}"/>
    <circle cx="150" cy="74" r="21" opacity="0.5"/>
    <path d="M150 42 L150 10" stroke-linecap="round"/>
  </g>
  <circle cx="150" cy="74" r="5" fill="{RED}"/>

  <!-- labels -->
  <g font-family="'Instrument Sans', sans-serif" font-size="19" fill="{INK}">
    <g stroke="{INK}" stroke-width="1" opacity="0.28">
      <path d="M436 112 H 468"/>
      <path d="M306 165 H 468"/>
      <path d="M306 248 H 468"/>
      <path d="M306 301 H 468"/>
    </g>
    <text x="476" y="119">Skin</text>
    <text x="476" y="172">Fat</text>
    <text x="476" y="255">Muscle</text>
    <text x="476" y="308">Rib</text>
  </g>

  <g font-family="'JetBrains Mono', monospace" font-size="13" fill="{RED}" letter-spacing="1.5">
    <text x="24" y="504">−25 dB AT 300 Hz</text>
  </g>
  <g font-family="'JetBrains Mono', monospace" font-size="12" fill="{NAVY}" opacity="0.55" letter-spacing="1.3">
    <text x="24" y="534">WHAT A 38 MM WALL TAKES OUT</text>
  </g>
</svg>"""


def step_capture():
    return f"""<svg viewBox="0 0 320 120" role="img" aria-label="Two microphones looking into the acoustic channel.">
  <g stroke="{NAVY}" fill="none" stroke-width="1.6">
    <rect x="24" y="34" width="86" height="52" rx="10"/>
    <circle cx="52" cy="60" r="7" fill="{RED}" stroke="none"/>
    <circle cx="52" cy="60" r="12"/>
    <circle cx="84" cy="60" r="6"/>
    <path d="M110 60 H 150" stroke-dasharray="3 4"/>
  </g>
  <path d="M150 82 C 162 82 164 38 176 38 C 188 38 190 82 202 82 C 214 82 216 38 228 38 C 240 38 242 80 254 80"
        fill="none" stroke="{RED}" stroke-width="2" stroke-linecap="round"/>
  <text x="24" y="20" font-family="'JetBrains Mono', monospace" font-size="9"
        letter-spacing="1.5" fill="{NAVY}">PORT · REFERENCE</text>
</svg>"""


def step_noise():
    return f"""<svg viewBox="0 0 320 120" role="img" aria-label="The reference microphone measures the room, and the room is subtracted.">
  <g stroke="{NAVY}" fill="none" stroke-width="1.5" opacity="0.9">
    <path d="M20 40 q 8 -14 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0"/>
    <path d="M20 66 q 8 -10 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0" opacity="0.5"/>
  </g>
  <path d="M196 53 H 232" stroke="{RED}" stroke-width="1.6"/>
  <path d="M226 49 l 8 4 l -8 4" fill="none" stroke="{RED}" stroke-width="1.6"/>
  <path d="M244 66 q 8 -8 16 0 t 16 0 t 16 0 t 16 0" fill="none" stroke="{RED}" stroke-width="2"/>
  <text x="20" y="24" font-family="'JetBrains Mono', monospace" font-size="9"
        letter-spacing="1.4" fill="{NAVY}">ROOM · REFERENCE · CLEAN</text>
</svg>"""


def step_correct():
    return f"""<svg viewBox="0 0 320 120" role="img" aria-label="The wall's transfer function is inverted, and the spectrum is flattened.">
  <g stroke="{NAVY}" fill="none" stroke-width="1.5">
    <path d="M24 34 C 90 34 100 96 180 96 C 230 96 250 92 296 92" opacity="0.45"/>
    <path d="M24 34 C 90 34 100 96 180 96 C 230 96 250 92 296 92" stroke="{NAVY}" stroke-width="0"/>
  </g>
  <path d="M24 96 C 90 96 100 34 180 34 C 230 34 250 36 296 36"
        fill="none" stroke="{RED}" stroke-width="2" stroke-linecap="round"/>
  <circle cx="160" cy="64" r="4" fill="{RED}"/>
  <path d="M160 64 L 160 24" stroke="{RED}" stroke-width="1" stroke-dasharray="2 3"/>
  <text x="24" y="114" font-family="'JetBrains Mono', monospace" font-size="9"
        letter-spacing="1.4" fill="{NAVY}">BEFORE · AFTER</text>
</svg>"""


def device_front():
    return f"""<svg viewBox="0 0 360 360" role="img" aria-label="Front view of the insert: a circular plate with a collar, a retention latch and the acoustic port.">
  <g stroke="{NAVY}" fill="none" stroke-width="1.5">
    <circle cx="180" cy="180" r="132" stroke-dasharray="5 6" opacity="0.45"/>
    <circle cx="180" cy="180" r="118" fill="{CREAM}"/>
    <circle cx="180" cy="180" r="96"/>
    <circle cx="180" cy="180" r="86" opacity="0.5"/>
    <path d="M180 62 v 22 M180 276 v 22 M62 180 h 22 M276 180 h 22" opacity="0.4"/>
  </g>
  <circle cx="180" cy="180" r="14" fill="{RED}"/>
  <circle cx="180" cy="180" r="24" fill="none" stroke="{NAVY}" stroke-width="1.2"/>
  <g fill="{NAVY}">
    <circle cx="255" cy="105" r="4"/><circle cx="105" cy="105" r="4"/>
    <circle cx="255" cy="255" r="4"/><circle cx="105" cy="255" r="4"/>
  </g>
  <rect x="168" y="44" width="24" height="12" rx="4" fill="{RED}"/>
  <g font-family="'JetBrains Mono', monospace" font-size="9.5" fill="{NAVY}" letter-spacing="1.2">
    <text x="180" y="352" text-anchor="middle">SCALE 1:1 · 44–48 MM SEAT</text>
  </g>
</svg>"""


def device_side():
    return f"""<svg viewBox="0 0 360 240" role="img" aria-label="Side section: 14 mm deep, silicone gasket on the chest face, collar on the stem side.">
  <g stroke="{NAVY}" fill="none" stroke-width="1.5">
    <rect x="72" y="86" width="216" height="58" rx="10" fill="{CREAM}"/>
    <path d="M72 100 H 288" opacity="0.45"/>
    <path d="M72 130 H 288" opacity="0.45"/>
    <rect x="96" y="64" width="168" height="12" rx="5" fill="{SKIN}" stroke="{SKIN}"/>
    <path d="M60 86 h 12 M60 144 h 12" opacity="0.5"/>
  </g>
  <path d="M180 86 v -22" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/>
  <g stroke="{RED}" stroke-width="1.2" fill="none">
    <path d="M300 86 v 58"/>
    <path d="M296 90 l 4 -4 l 4 4 M296 140 l 4 4 l 4 -4"/>
  </g>
  <text x="314" y="118" font-family="'JetBrains Mono', monospace" font-size="10"
        fill="{RED}" letter-spacing="1">14</text>
  <text x="72" y="184" font-family="'JetBrains Mono', monospace" font-size="9"
        fill="{NAVY}" letter-spacing="1.2">GASKET · COLLAR · PORT</text>
</svg>"""


def device_installed():
    return f"""<svg viewBox="0 0 380 380" role="img" aria-label="The insert fitted behind a conventional chestpiece, with the stem and tubing.">
  <g stroke="{NAVY}" fill="none" stroke-width="1.6">
    <path d="M190 250 C 190 300 150 300 150 336" stroke-width="8" stroke-linecap="round" opacity="0.9"/>
    <circle cx="190" cy="170" r="108" fill="{CREAM}"/>
    <circle cx="190" cy="170" r="88" opacity="0.55"/>
    <circle cx="190" cy="170" r="40" opacity="0.35"/>
    <rect x="128" y="248" width="124" height="30" rx="8" fill="{SKIN}" stroke="{NAVY}"/>
  </g>
  <circle cx="190" cy="170" r="10" fill="{RED}"/>
  <path d="M190 140 v -18" stroke="{RED}" stroke-width="2"/>
  <g font-family="'JetBrains Mono', monospace" font-size="9" fill="{NAVY}" letter-spacing="1.2">
    <text x="190" y="372" text-anchor="middle">STANDARD HEAD · INSERT BEHIND</text>
  </g>
</svg>"""


def device_exploded():
    layers = [
        ("Diaphragm face", 150, 10),
        ("Acoustic port", 168, 14),
        ("Dual MEMS board", 176, 9),
        ("Battery", 132, 12),
        ("Base shell", 182, 16),
        ("Retention collar", 120, 8),
    ]
    parts = []
    y = 60
    for i, (name, w, h) in enumerate(layers):
        x = 230 - w / 2
        fill = CREAM if i % 2 == 0 else "#FBE8DF"
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" '
            f'stroke="{NAVY}" stroke-width="1.4"/>'
        )
        lx = 230 + w / 2 + 16
        parts.append(
            f'<path d="M{230 + w / 2 + 4} {y + h / 2} H {lx - 4}" stroke="{INK}" '
            f'stroke-width="0.8" opacity="0.35"/>'
        )
        parts.append(
            f'<text x="{lx}" y="{y + h / 2 + 4}" font-family="\'JetBrains Mono\', monospace" '
            f'font-size="10" fill="{INK}" letter-spacing="0.8">{name.upper()}</text>'
        )
        y += h + 26

    return f"""<svg viewBox="0 0 520 470" role="img" aria-label="Exploded section of the insert: six stacked parts, from the diaphragm face to the retention collar.">
  <line x1="230" y1="40" x2="230" y2="430" stroke="{NAVY}" stroke-width="0.8" stroke-dasharray="4 6" opacity="0.4"/>
  {''.join(parts)}
  <text x="30" y="448" font-family="'JetBrains Mono', monospace" font-size="9"
        fill="{NAVY}" letter-spacing="1.4">SECTION · SIX PARTS · NO ADHESIVE</text>
</svg>"""


def icon_bodies():
    return f"""<svg viewBox="0 0 260 88" role="img" aria-label="Three chest walls of different thickness.">
  <g fill="none" stroke="{NAVY}" stroke-width="1.4">
    <path d="M14 70 q 34 -30 68 0" opacity="0.5"/>
    <path d="M14 62 q 34 -30 68 0"/>
    <path d="M96 70 q 34 -30 68 0" opacity="0.5"/>
    <path d="M96 54 q 34 -30 68 0"/>
    <path d="M178 70 q 34 -30 68 0" opacity="0.5"/>
    <path d="M178 44 q 34 -30 68 0"/>
  </g>
  <circle cx="48" cy="82" r="3" fill="{RED}"/>
  <circle cx="130" cy="82" r="3" fill="{RED}"/>
  <circle cx="212" cy="82" r="3" fill="{RED}"/>
</svg>"""


def icon_age():
    return f"""<svg viewBox="0 0 260 88" role="img" aria-label="A wall that stiffens with age.">
  <g fill="none" stroke="{NAVY}" stroke-width="1.4">
    <path d="M24 62 C 64 62 84 30 124 30 C 164 30 184 54 236 54"/>
    <path d="M24 62 C 64 62 84 30 124 30" stroke="{RED}" stroke-width="2.2"/>
  </g>
  <circle cx="124" cy="30" r="4" fill="{RED}"/>
  <text x="24" y="82" font-family="'JetBrains Mono', monospace" font-size="8.5"
        fill="{NAVY}" letter-spacing="1">STIFFER · LOWER RESONANCE</text>
</svg>"""


def icon_places():
    return f"""<svg viewBox="0 0 260 88" role="img" aria-label="A small clinic, a community health centre and a hospital ward.">
  <g fill="none" stroke="{NAVY}" stroke-width="1.4">
    <path d="M20 66 h 54 v -28 h -54 z"/>
    <path d="M32 66 v -16 h 12 v 16"/>
    <path d="M108 66 h 60 v -36 h -60 z"/>
    <path d="M122 66 v -18 h 14 v 18 M122 38 h 14"/>
    <path d="M200 66 h 44 v -22 h -44 z"/>
    <path d="M200 44 l 22 -16 l 22 16"/>
  </g>
  <path d="M20 66 h 226" stroke="{NAVY}" stroke-width="1.1" opacity="0.4"/>
</svg>"""


def icon_remote():
    return f"""<svg viewBox="0 0 260 88" role="img" aria-label="A recording shared with a specialist at another site.">
  <g fill="none" stroke="{NAVY}" stroke-width="1.4">
    <rect x="24" y="26" width="48" height="34" rx="4"/>
    <path d="M72 43 h 62"/>
    <circle cx="146" cy="43" r="12"/>
    <path d="M134 43 h -7 M158 43 h 7" opacity="0.6"/>
    <rect x="176" y="20" width="60" height="46" rx="4"/>
    <path d="M186 34 h 40 M186 44 h 40 M186 54 h 26" opacity="0.55"/>
  </g>
  <circle cx="146" cy="43" r="3" fill="{RED}"/>
</svg>"""
