#!/usr/bin/env python3
"""Draw the Hyprland layer plan on the Killer Whale DUO's Remap layout.

The key positions come from Remap's own definition
(qmk_firmware/killer_whale_duo.json), so the pictures look like the board in
Remap. The layers below are the single source for the pictures in
hyprland/img/; keep README.md in step when changing them.

    python3 hyprland/tools/render.py          # writes hyprland/img/*.svg
    python3 hyprland/tools/render.py --png    # also PNGs (needs node +
                                              # playwright with Chromium)
"""
import json
import subprocess
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT = HERE.parent / "img"
DUO = REPO / "qmk_firmware" / "killer_whale_duo.json"
KBD = REPO / "qmk_firmware" / "keyboards" / "killerwhale" / "duo" / "keyboard.json"

# Our names for the keys, in keyboard.json's LAYOUT order (left, then right).
NAMES = (
    "ESC 1 2 3 4 5  TAB Q W E R T  CTL A S D F G  Z X C V B  LSCRL "
    "LSIDE1 LSIDE2  LUP LDOWN LLEFT LRIGHT LJOY  LADD1 LADD2 LTOG "
    "6 7 8 9 0 BSPC  Y U I O P ENT  H J K L SCLN RSFT  N M COMM DOT SLSH  RSCRL "
    "RSIDE1 RSIDE2  RUP RDOWN RLEFT RRIGHT RJOY  RADD1 RADD2 RTOG"
).split()

# Wheels as Remap numbers them: e0/e1 left top wheels, e2 left side-unit
# wheel (by the joystick), e3 left ADD wheel; e4–e7 the same on the right.
WHEELS = {
    0: "top", 1: "top", 2: "side", 3: "ADD",
    4: "top", 5: "top", 6: "side", 7: "ADD",
}

# Keys the DUO here doesn't have: the right side unit is a trackball.
ABSENT = {"RUP", "RDOWN", "RLEFT", "RRIGHT", "RJOY"}
# No wheel top unit on this DUO.
ABSENT_WHEELS = {"top"}

# kinds: key (plain), mod, layer (layer key), here (the key holding this
# layer), hypr (SUPER + …), media, mouse, sym, nav, cfg (stock special key),
# none (KC_NO). Anything not listed in a layer is transparent.
BASE_KEYS = {
    "ESC": "Esc", "TAB": "Tab", "CTL": ("Esc|Ctrl", "mod"),
    "4": ("4|ball⚙", "key"), "7": ("7|ball⚙", "key"),
    "S": ("S|mouse", "key"), "L": ("L|mouse", "key"),
    "Z": ("Z|Shift", "mod"), "RSFT": ("Shift", "mod"),
    "SCLN": ";", "COMM": ",", "DOT": ".", "SLSH": "/", "BSPC": "Bksp",
    "ENT": "Enter",
    "LSCRL": ("Super", "mod"), "RSCRL": ("ball|scroll", "mouse"),
    "LSIDE1": ("Hypr", "layer"), "LSIDE2": "Space",
    "RSIDE1": ("Nav", "layer"), "RSIDE2": ("Sym", "layer"),
    "LUP": "↑", "LDOWN": "↓", "LLEFT": "←", "LRIGHT": "→",
    "LJOY": ("stick|mode", "cfg"),
    "LADD1": ("Alt", "mod"), "LADD2": ("Click", "mouse"),
    "RADD1": ("Click", "mouse"), "RADD2": ("Right|click", "mouse"),
    "LTOG": ("Game", "layer"), "RTOG": ("free", "layer"),
}
for k in "1 2 3 5 6 8 9 0 Q W E R T A D F G X C V B Y U I O P H J K N M".split():
    BASE_KEYS.setdefault(k, k)

LAYERS = [
    {
        "file": "layer0-base", "title": "0 · Base",
        "note": "QWERTY. Tap/hold keys show tap above hold.",
        "keys": BASE_KEYS, "full": True,
        "wheels": {
            2: ("Vol −", "Vol +"), 3: ("Vol −", "Vol +"),
            6: ("Scroll ↑", "Scroll ↓"), 7: ("Scroll ↑", "Scroll ↓"),
        },
    },
    {
        "file": "layer4-hypr", "title": "4 · Hypr  (hold left side key 1)",
        "note": "Every blue key is SUPER + key. Hold Z (Shift) with a number "
                "to move the window to that workspace.",
        "here": "LSIDE1",
        "keys": {
            "ESC": ("Power", "hypr"), "TAB": ("Last|wksp", "hypr"),
            **{n: (f"Wksp|{n}", "hypr") for n in "1 2 3 4 5 6 7 8 9".split()},
            "0": ("Wksp|10", "hypr"),
            "Q": ("Close", "hypr"), "W": ("Wksp|OSD", "hypr"),
            "E": ("", "none"), "R": ("", "none"), "T": ("Tray", "hypr"),
            "A": ("Ctrl|center", "hypr"), "S": ("Screen|shot", "hypr"),
            "D": ("Apps", "hypr"), "F": ("Full|screen", "hypr"),
            "G": ("Float", "hypr"),
            "X": ("", "none"), "C": ("Clock", "hypr"),
            "V": ("Clip|board", "hypr"), "B": ("Battery", "hypr"),
            "BSPC": ("", "none"),
            "Y": ("", "none"), "U": ("", "none"), "I": ("", "none"),
            "O": ("", "none"), "P": ("", "none"), "ENT": ("Term", "hypr"),
            "H": ("Focus|←", "hypr"), "J": ("Focus|↓", "hypr"),
            "K": ("Focus|↑", "hypr"), "L": ("Focus|→", "hypr"),
            "SCLN": ("", "none"),
            "N": ("Notifs", "hypr"), "M": ("", "none"), "COMM": ("", "none"),
            "DOT": ("", "none"), "SLSH": ("", "none"),
            "LSIDE2": ("Glance", "hypr"), "RSIDE1": ("HUD|toggle", "hypr"),
            "RSIDE2": ("", "none"),
            "LUP": ("Move|win ↑", "hypr"), "LDOWN": ("Move|win ↓", "hypr"),
            "LLEFT": ("Move|win ←", "hypr"), "LRIGHT": ("Move|win →", "hypr"),
        },
        "wheels": {
            2: ("Bright −", "Bright +"), 3: ("Bright −", "Bright +"),
            6: ("Wksp ←", "Wksp →"), 7: ("Wksp ←", "Wksp →"),
        },
    },
    {
        "file": "layer5-nav", "title": "5 · Nav  (hold right side key 1)",
        "note": "Arrows on h j k l. Left Ctrl and Shift still work for "
                "word jumps and selecting.",
        "here": "RSIDE1",
        "keys": {
            **{str(i): (f"F{i}", "nav") for i in range(1, 10)},
            "0": ("F10", "nav"), "BSPC": ("Del", "nav"),
            "Q": ("F11", "nav"), "W": ("F12", "nav"),
            "E": ("Prev", "media"), "R": ("Play", "media"),
            "T": ("Next", "media"),
            "A": ("Mute", "media"), "S": ("Vol −", "media"),
            "D": ("Vol +", "media"), "F": ("Bright|−", "media"),
            "G": ("Bright|+", "media"),
            "X": ("", "none"), "C": ("Print", "media"), "V": ("", "none"),
            "B": ("", "none"),
            "Y": ("Home", "nav"), "U": ("PgDn", "nav"), "I": ("PgUp", "nav"),
            "O": ("End", "nav"), "P": ("Ins", "nav"),
            "H": ("←", "nav"), "J": ("↓", "nav"), "K": ("↑", "nav"),
            "L": ("→", "nav"), "SCLN": ("", "none"),
            "N": ("", "none"), "M": ("", "none"), "COMM": ("", "none"),
            "DOT": ("", "none"), "SLSH": ("", "none"),
        },
        "wheels": {
            2: ("←", "→"), 3: ("←", "→"),
            6: ("PgUp", "PgDn"), 7: ("PgUp", "PgDn"),
        },
    },
    {
        "file": "layer6-sym", "title": "6 · Sym  (hold right side key 2)",
        "note": "Top row unshifted (Shift gives the partner), second row "
                "shifted. ' sits right of ; as usual.",
        "here": "RSIDE2",
        "keys": {
            "Y": ("`", "sym"), "U": ("[", "sym"), "I": ("]", "sym"),
            "O": ("-", "sym"), "P": ("=", "sym"), "ENT": ("\\", "sym"),
            "H": ("~", "sym"), "J": ("{", "sym"), "K": ("}", "sym"),
            "L": ("_", "sym"), "SCLN": ("+", "sym"), "RSFT": ("'", "sym"),
            "N": ("|", "sym"), "M": ("(", "sym"), "COMM": (")", "sym"),
            "DOT": ("<", "sym"), "SLSH": (">", "sym"),
        },
        "wheels": {},
    },
    {
        "file": "layer7-mouse", "title": "7 · Mouse  (auto: move the trackball)",
        "note": "Stock auto-mouse layer plus a middle click on U; Super stays Super "
                "so SUPER + drag works while the ball moves.",
        "keys": {
            "D": ("Right|click", "mouse"), "F": ("Click", "mouse"),
            "G": ("Scroll", "mouse"), "Z": ("Slow", "mouse"),
            "H": ("Scroll", "mouse"), "J": ("Click", "mouse"),
            "K": ("Right|click", "mouse"), "U": ("Middle", "mouse"),
            "SLSH": ("Slow", "mouse"),
        },
        "wheels": {},
    },
    {
        "file": "layer1-game", "title": "1 · Game  (left toggle switch on)",
        "note": "Number row = F1–F10, J K L = mouse buttons, numbers around "
                "them. Hold left side key 2 for Game 2.",
        "here": "LTOG",
        "keys": {
            "CTL": ("Ctrl", "mod"), "Z": ("Z", "key"), "S": ("S", "key"),
            **{n: (f"F{n}", "nav") for n in "1 2 3 4 5 6 7 8 9".split()},
            "0": ("F10", "nav"),
            "LSIDE1": ("Space", "key"), "LSIDE2": ("Game 2", "layer"),
            "J": ("Click", "mouse"), "K": ("Right|click", "mouse"),
            "L": ("Middle", "mouse"),
            "Y": ("1", "key"), "U": ("2", "key"), "I": ("3", "key"),
            "O": ("4", "key"), "P": ("5", "key"),
            "N": ("6", "key"), "M": ("7", "key"), "COMM": ("8", "key"),
            "DOT": ("9", "key"), "SLSH": ("0", "key"),
        },
        "wheels": {},
    },
    {
        "file": "layer3-game2", "title": "3 · Game 2  (in Game: hold left side key 2)",
        "note": "Everything Game moved away: the numbers, the letters "
                "under the clicks and numbers, F11 / F12, auto mouse on / off.",
        "here": "LSIDE2", "here_label": "Game 2", "below": "layer1-game",
        "keys": {
            "ESC": ("F11", "nav"), "BSPC": ("F12", "nav"),
            **{n: (n, "key") for n in "1 2 3 4 5 6 7 8 9 0".split()},
            **{n: (n, "key") for n in "Y U I O P H J K L N M".split()},
            "SCLN": (";", "key"), "COMM": (",", "key"), "DOT": (".", "key"),
            "SLSH": ("/", "key"),
            "LSCRL": ("Auto|mouse", "cfg"),
        },
        "wheels": {},
    },
]

COLORS = {  # fill, text
    "key": ("#f4f4f4", "#222"),
    "mod": ("#d9f0d9", "#1d5c1d"),
    "layer": ("#ffd9a8", "#7a4300"),
    "here": ("#ff9d2e", "#fff"),
    "hypr": ("#cfe0ff", "#173d8a"),
    "nav": ("#e3dcff", "#3d2a8a"),
    "media": ("#ffe0ef", "#8a1f55"),
    "sym": ("#fff3b0", "#6b5600"),
    "mouse": ("#e2f4f7", "#145866"),
    "cfg": ("#e8e8e8", "#555"),
    "none": ("#fafafa", "#bbb"),
    "trns": ("#fafafa", "#9a9a9a"),
    "absent": ("#fafafa", "#ccc"),
}
LEGEND = [("hypr", "SUPER + key (Hyprland / HyprOSD)"),
          ("layer", "layer key"), ("here", "held for this layer"),
          ("mod", "modifier"), ("nav", "navigation / F-keys"),
          ("media", "media"), ("sym", "symbol"), ("mouse", "mouse"),
          ("trns", "▽ = from the layer below")]

U = 58           # pixels per key unit
PAD = 24


def kle_positions():
    """(x, y, w, h, matrix or 'eN', color) from Remap's KLE layout, option 0."""
    rows = json.load(open(DUO))["layouts"]["keymap"]
    out, y = [], 0.0
    for row in rows:
        x, w, h, c = 0.0, 1, 1, "#cccccc"
        for item in row:
            if isinstance(item, dict):
                x += item.get("x", 0); y += item.get("y", 0)
                w = item.get("w", w); h = item.get("h", h); c = item.get("c", c)
                continue
            parts = item.split("\n")
            if len(parts) > 3 and parts[3] and parts[3] != "0,0":
                x += w; w = h = 1; continue     # other layout option
            enc = parts[9] if len(parts) > 9 else ""
            out.append((x, y, w, h, enc or parts[0], c))
            x += w; w = h = 1
        y += 1
    return out


def matrix_names():
    layout = json.load(open(KBD))["layouts"]["LAYOUT"]["layout"]
    assert len(layout) == len(NAMES), (len(layout), len(NAMES))
    return {"%d,%d" % tuple(k["matrix"]): n for k, n in zip(layout, NAMES)}


def label_of(entry):
    if isinstance(entry, tuple):
        return entry
    return (entry, "key")


def svg_text(cx, cy, text, color, size, weight=600):
    lines = ([text] if text == "|" else text.split("|")) if text else []
    out = []
    for i, line in enumerate(lines):
        dy = (i - (len(lines) - 1) / 2) * size * 1.15
        out.append(
            f'<text x="{cx:.1f}" y="{cy + dy:.1f}" fill="{color}" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="middle" '
            f'dominant-baseline="central">{escape(line)}</text>')
    return "".join(out)


def render(layer, pos, names):
    keys, wheels = layer["keys"], layer["wheels"]
    maxx = max(p[0] + p[2] for p in pos)
    maxy = max(p[1] + p[3] for p in pos)
    width = maxx * U + 2 * PAD
    top = 70
    legend_h = 64
    height = top + maxy * U + PAD + legend_h
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
         f'height="{height:.0f}" font-family="DejaVu Sans, sans-serif">',
         f'<rect width="100%" height="100%" fill="#ffffff"/>',
         f'<text x="{PAD}" y="32" fill="#111" font-size="22" '
         f'font-weight="700">{escape(layer["title"])}</text>',
         f'<text x="{PAD}" y="52" fill="#555" font-size="14">'
         f'{escape(layer["note"])}</text>']
    for x, y, w, h, ref, color in pos:
        px, py = PAD + x * U, top + y * U
        if ref.startswith("e"):
            n = int(ref[1:])
            r = U * 0.47
            cx, cy = px + w * U / 2, py + h * U / 2
            pair = wheels.get(n)
            kind, text = "absent", ""
            if WHEELS[n] in ABSENT_WHEELS:
                fill, ink = COLORS["absent"]
                s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
                         f'fill="{fill}" stroke="#bbb" stroke-width="1.5" '
                         f'stroke-dasharray="4 3"/>')
                s.append(svg_text(cx, cy, "none|fitted", ink, 9))
                continue
            if pair is None and not layer.get("full"):
                text, kind = "▽", "trns"
            elif pair:
                text, kind = f"↺ {pair[0]}|↻ {pair[1]}", "media"
            fill, ink = COLORS["key" if kind == "media" else kind]
            s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
                     f'fill="{fill}" stroke="#888" stroke-width="2"/>')
            s.append(svg_text(cx, cy, text, ink, 9.5))
            s.append(svg_text(cx, cy + r + 8, WHEELS[n] + " wheel", "#999", 9, 400))
            continue
        name = names.get(ref)
        if name in ABSENT:
            kind, text = "absent", "·"
        elif name == layer.get("here"):
            text, kind = layer.get("here_label") or label_of(BASE_KEYS[name])[0], "here"
        elif name in keys:
            text, kind = label_of(keys[name])
            if kind == "none" and not text:
                text = "✕"
        elif layer.get("full"):
            text, kind = name, "key"
        else:
            below = next((l["keys"] for l in LAYERS
                          if l["file"] == layer.get("below")), {})
            text = label_of(below.get(name, BASE_KEYS.get(name, name)))[0]
            kind = "trns"
        fill, ink = COLORS[kind]
        stroke = "#c46a00" if kind == "here" else (
            "#555" if color == "#777777" else "#aaa")
        dash = ' stroke-dasharray="4 3"' if kind in ("trns", "absent") else ""
        s.append(f'<rect x="{px + 2:.1f}" y="{py + 2:.1f}" '
                 f'width="{w * U - 4:.1f}" height="{h * U - 4:.1f}" rx="6" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"{dash}/>')
        size = 15 if len(text.replace("|", "")) <= 2 else 11
        s.append(svg_text(px + w * U / 2, py + h * U / 2, text, ink, size))
    # legend
    lx, ly = PAD, top + maxy * U + PAD + 6
    for kind, desc in LEGEND:
        fill, ink = COLORS[kind]
        s.append(f'<rect x="{lx}" y="{ly}" width="18" height="18" rx="3" '
                 f'fill="{fill}" stroke="#aaa"/>')
        s.append(f'<text x="{lx + 24}" y="{ly + 13}" font-size="12" '
                 f'fill="#333">{escape(desc)}</text>')
        lx += 34 + len(desc) * 6.6
        if lx > width - 200:
            lx, ly = PAD, ly + 26
    s.append("</svg>")
    return "\n".join(s)


def main():
    OUT.mkdir(exist_ok=True)
    pos, names = kle_positions(), matrix_names()
    files = []
    for layer in LAYERS:
        path = OUT / (layer["file"] + ".svg")
        path.write_text(render(layer, pos, names))
        files.append(path)
    if "--png" in sys.argv:
        js = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 2 });
  for (const f of process.argv.slice(1)) {
    await p.goto('file://' + f);
    const el = await p.$('svg');
    await el.screenshot({ path: f.replace(/\\.svg$/, '.png') });
  }
  await b.close();
})();"""
        subprocess.run(["node", "-e", js, *map(str, files)], check=True)
    print("\n".join(str(f) for f in files))


if __name__ == "__main__":
    main()
