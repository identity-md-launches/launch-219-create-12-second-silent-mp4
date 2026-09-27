#!/usr/bin/env python3
"""Render the three-scene frog story as SVG frames and a browser-ready MP4."""

from __future__ import annotations

import math
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
FRAMES = ROOT / "test" / "scratch" / "frames"
OUTPUT = ROOT / "artifacts" / "video.mp4"
FPS = 24
COUNT = 12 * FPS

INK = "#183342"
GREEN = "#58C882"
GREEN_DARK = "#34A76A"
BELLY = "#B8E9AE"
ORANGE = "#F49A49"
PLUM = "#715A91"
CREAM = "#FFF9ED"
BLUE = "#AEDCE2"


def ease(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3 - 2 * value)


def E(value: object) -> str:
    return escape(str(value), {'"': "&quot;"})


def rect(x, y, w, h, fill, stroke="none", sw=0, rx=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def circle(x, y, r, fill, stroke="none", sw=0):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def ellipse(x, y, rx, ry, fill, stroke="none", sw=0):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def path(d, fill="none", stroke="none", sw=0, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def text(x, y, content, size=24, color=INK, weight=700, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}" {extra}>{E(content)}</text>'


def frog(x: float, y: float, scale: float, kind: str, blink: bool = False) -> str:
    """One shared frog design; clothing distinguishes the two recurring characters."""
    p = [f'<g transform="translate({x:.2f} {y:.2f}) scale({scale})">']
    p += [ellipse(-61, 147, 46, 20, GREEN_DARK, INK, 5),
          ellipse(61, 147, 46, 20, GREEN_DARK, INK, 5),
          ellipse(0, 61, 76, 101, GREEN, INK, 6)]
    if kind == "engineer":
        p += [path("M-69 34 L-49 145 L48 145 L69 34 Q0 57 -69 34Z", ORANGE, INK, 5),
              rect(-43, 79, 86, 48, "#FFD091", INK, 4, 12),
              path("M-52 37 L-30 81 M52 37 L30 81", stroke=INK, sw=12),
              circle(0, 56, 9, INK)]
    else:
        p += [path("M-72 28 L-50 139 L50 139 L72 28 Q0 57 -72 28Z", PLUM, INK, 5),
              path("M-27 51 L0 84 L27 51", stroke="#DFC6EC", sw=10),
              circle(0, 112, 9, "#F8D379", INK, 3)]
    # Side arms are kept with the frog so the characters remain recognizable.
    p += [path("M-69 39 Q-117 91 -96 117", stroke=INK, sw=29),
          path("M-69 39 Q-117 91 -96 117", stroke=GREEN, sw=19),
          circle(-96, 117, 17, GREEN, INK, 4),
          path("M69 39 Q115 80 93 119", stroke=INK, sw=29),
          path("M69 39 Q115 80 93 119", stroke=GREEN, sw=19),
          circle(93, 119, 17, GREEN, INK, 4),
          ellipse(0, -78, 108, 79, GREEN, INK, 6),
          circle(-61, -132, 39, GREEN, INK, 6),
          circle(61, -132, 39, GREEN, INK, 6),
          ellipse(-60, -133, 23, 25, "#FFFFFF"),
          ellipse(60, -133, 23, 25, "#FFFFFF")]
    if blink:
        p += [path("M-77 -132 L-43 -132 M43 -132 L77 -132", stroke=INK, sw=5)]
    else:
        p += [circle(-54, -130, 10, INK), circle(66, -130, 10, INK),
              circle(-50, -134, 3, "#FFFFFF"), circle(70, -134, 3, "#FFFFFF")]
    p += [circle(-18, -74, 4, GREEN_DARK), circle(18, -74, 4, GREEN_DARK),
          path("M-32 -54 Q0 -29 32 -54", stroke=INK, sw=5),
          circle(-78, -67, 7, "#E98D81"),
          circle(78, -67, 7, "#E98D81")]
    if kind == "engineer":
        p += [path("M-81 -149 Q-74 -202 0 -204 Q74 -202 81 -149Z", ORANGE, INK, 6),
              rect(-95, -155, 190, 17, "#E9863F", INK, 5, 8),
              path("M0 -200 L0 -155", stroke="#FFD091", sw=8)]
    else:
        p += [circle(-58, -119, 34, "none", INK, 5),
              circle(60, -119, 34, "none", INK, 5),
              path("M-24 -119 Q0 -130 26 -119", stroke=INK, sw=5),
              path("M-92 -121 L-104 -130 M94 -121 L106 -130", stroke=INK, sw=5)]
    p.append("</g>")
    return "".join(p)


def block(x: float, y: float, color: str, number: str = "") -> str:
    p = [rect(x, y, 88, 88, color, INK, 5, 8),
         path(f"M{x+12} {y+17} L{x+74} {y+17}", stroke="#FFFFFF", sw=4, extra='opacity="0.55"')]
    if number:
        p.append(text(x + 44, y + 63, number, 35, INK, 800, "middle"))
    return "".join(p)


def header(scene: int, title: str, bg: str, accent: str) -> str:
    p = [rect(0, 0, 1280, 720, bg),
         rect(0, 593, 1280, 127, "#D9E7DB"),
         path("M0 593 H1280", stroke=INK, sw=5),
         text(71, 73, title, 43, INK, 800),
         circle(1176, 57, 34, accent, INK, 4),
         text(1176, 68, f"{scene:02d}", 27, INK, 800, "middle")]
    for i in range(3):
        p.append(rect(71 + i * 383, 674, 358, 13, accent if i == scene - 1 else "#A9C3BC", "none", 0, 7))
    return "".join(p)


def scene_build(t: float) -> str:
    p = [header(1, "BUILD", "#FFF7E9", ORANGE)]
    # Workshop wall graphics and workbench.
    p += [rect(886, 128, 282, 231, "#E4F3E4", INK, 5, 18),
          text(1027, 164, "BLOCK PLAN", 19, INK, 800, "middle"),
          block(959, 229, "#F8C26E"), block(1048, 229, "#84BFE1"),
          rect(956, 327, 184, 8, INK, rx=4),
          rect(435, 453, 679, 36, "#F2B882", INK, 5, 8),
          rect(483, 487, 27, 105, "#416778", INK, 5, 4),
          rect(1039, 487, 27, 105, "#416778", INK, 5, 4),
          ellipse(275, 573, 126, 14, "#BCD0C6")]
    p += [block(689, 365, "#F8C26E", "1"), block(779, 365, "#8FC5E8", "2")]
    # The third block travels from the engineer's hands to the top of the stack.
    travel = ease(t / 2.15)
    drop = ease((t - 2.15) / 0.42)
    bx = 448 + (734 - 448) * travel
    by = 296 - 73 * travel + 51 * drop
    # Behind-body arm, hand at the moving block's lower left edge.
    hand_x, hand_y = bx + 11, by + 66
    p += [path(f"M340 436 Q410 398 {hand_x:.1f} {hand_y:.1f}", stroke=INK, sw=29),
          path(f"M340 436 Q410 398 {hand_x:.1f} {hand_y:.1f}", stroke=GREEN, sw=19),
          circle(hand_x, hand_y, 17, GREEN, INK, 4),
          frog(262, 408, 1, "engineer", 3.4 < t < 3.51),
          block(bx, by, "#E99E9A", "3")]
    p += [text(73, 629, "An engineer sets the last block in place.", 22, INK, 600)]
    return "".join(p)


def scene_check(t: float) -> str:
    p = [header(2, "CHECK", "#EFF9EE", "#90CABE")]
    p += [rect(71, 154, 207, 256, "#FCFFFA", INK, 5, 16),
          text(174, 196, "CHECKLIST", 20, INK, 800, "middle")]
    for i, label in enumerate(("shape", "fit", "stack")):
        y = 244 + i * 65
        p += [rect(100, y - 22, 33, 33, "#FFFFFF", INK, 4, 5),
              text(151, y + 3, label, 20, INK, 600)]
        if t > 0.7 + i * 0.8:
            p.append(path(f"M106 {y-6} L116 {y+2} L130 {y-17}", stroke=GREEN_DARK, sw=6))
    p += [rect(350, 453, 476, 36, "#B2D5B7", INK, 5, 8),
          rect(389, 488, 27, 105, "#416778", INK, 5, 4),
          rect(758, 488, 27, 105, "#416778", INK, 5, 4),
          block(485, 365, "#F8C26E", "1"), block(575, 365, "#8FC5E8", "2"),
          block(530, 274, "#E99E9A", "3"),
          ellipse(935, 573, 128, 14, "#C1D6CA"),
          frog(938, 408, 1, "inspector", 3.42 < t < 3.54)]
    # A moving magnifier scans the stack. The glass is translucent so blocks show through.
    scan = ease(t / 3.1)
    lens_x = 603 + 93 * scan
    lens_y = 330 + 54 * math.sin(scan * math.pi)
    p += [path(f"M868 440 Q806 423 {lens_x+75:.1f} {lens_y+58:.1f}", stroke=INK, sw=27),
          path(f"M868 440 Q806 423 {lens_x+75:.1f} {lens_y+58:.1f}", stroke=GREEN, sw=17),
          path(f"M{lens_x+38:.1f} {lens_y+39:.1f} L{lens_x+78:.1f} {lens_y+79:.1f}", stroke=INK, sw=16),
          circle(lens_x, lens_y, 60, "#DDF6FC", INK, 9),
          path(f"M{lens_x-29:.1f} {lens_y-24:.1f} Q{lens_x-3:.1f} {lens_y-46:.1f} {lens_x+14:.1f} {lens_y-34:.1f}", stroke="#FFFFFF", sw=8)]
    p += [text(73, 629, "A second frog checks the finished stack.", 22, INK, 600)]
    return "".join(p)


def scene_deliver(t: float) -> str:
    p = [header(3, "DELIVER", "#EAF5F9", "#85BED5")]
    # Receiving bay and fixed destination platform.
    p += [rect(93, 177, 374, 415, "#BADBCF", INK, 6, 17),
          rect(119, 213, 322, 338, "#DFF1E6", INK, 4, 8),
          text(280, 159, "RECEIVING", 24, INK, 800, "middle"),
          rect(91, 555, 395, 38, "#779DA2", INK, 5, 7),
          path("M145 479 H409", stroke="#9FBEB0", sw=5, extra='stroke-dasharray="11 12"')]
    move = ease(t / 3.0)
    cx = 920 - 480 * move
    fy = 427 + 2 * math.sin(t * 10) * (1 - move)
    # Character and trolley positions share the same offset.
    p += [ellipse(cx + 168, 574, 181, 15, "#C3D8D2"),
          frog(cx + 373, fy, 0.73, "engineer", False),
          frog(cx + 523, fy, 0.73, "inspector", False),
          rect(cx - 156, 509, 322, 23, "#4A7680", INK, 5, 7),
          circle(cx - 112, 550, 22, INK), circle(cx + 115, 550, 22, INK),
          circle(cx - 112, 550, 9, "#EAF5F9"), circle(cx + 115, 550, 9, "#EAF5F9"),
          path(f"M{cx+168:.1f} 518 L{cx+270:.1f} 485", stroke=INK, sw=14),
          path(f"M{cx+168:.1f} 518 L{cx+270:.1f} 485", stroke="#4A7680", sw=8)]
    # Folded cardboard flaps, generous label, and high-contrast SOURCE text.
    p += [rect(cx - 139, 296, 278, 212, "#D8A66C", INK, 6, 9),
          path(f"M{cx-139:.1f} 329 L{cx:.1f} 355 L{cx+139:.1f} 329", stroke=INK, sw=5),
          path(f"M{cx:.1f} 355 V508", stroke="#A97549", sw=5),
          path(f"M{cx-139:.1f} 297 L{cx-89:.1f} 269 H{cx+89:.1f} L{cx+139:.1f} 297Z", "#ECC18D", INK, 6),
          rect(cx - 112, 387, 224, 77, CREAM, INK, 4, 8),
          text(cx, 437, "SOURCE", 36, INK, 800, "middle"),
          path(f"M{cx+279:.1f} 483 Q{cx+305:.1f} 496 {cx+316:.1f} 511", stroke=INK, sw=23),
          path(f"M{cx+279:.1f} 483 Q{cx+305:.1f} 496 {cx+316:.1f} 511", stroke=GREEN, sw=14)]
    p += [text(73, 629, "The labeled box reaches the receiving bay.", 22, INK, 600)]
    return "".join(p)


def frame(index: int) -> str:
    second = index / FPS
    if second < 4:
        content = scene_build(second)
    elif second < 8:
        content = scene_check(second - 4)
    else:
        content = scene_deliver(second - 8)
    return '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">' + content + '</svg>\n'


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    for i in range(COUNT):
        (FRAMES / f"frame_{i:03d}.svg").write_text(frame(i), encoding="utf-8")
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-framerate", str(FPS), "-i", str(FRAMES / "frame_%03d.svg"),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-frames:v", str(COUNT), "-t", "12",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "96k", "-ar", "48000",
        "-movflags", "+faststart", str(OUTPUT),
    ], check=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
