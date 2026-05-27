"""Board 3: what shipped in 90 days.

Pilot architecture (dummy data through the CLI in this repo) plus the
outcome numbers.
"""

from build_boards import (
    ORANGE, RED, BLUE, GREEN, YELLOW, WHITE, VIOLET, MUTED,
    arrow_svg, render, rough_rect_svg, text_svg,
    excal_rect, excal_text, excal_arrow, write_scene,
)

WIDTH, HEIGHT = 1240, 760


def box_block(x, y, w, h, lines, fill, first_size=14, rest_size=12, width_chars=None):
    wc = width_chars or max(16, int(w / 6.6))
    out = rough_rect_svg(x, y, w, h, fill)
    cursor = y + 22
    for i, line in enumerate(lines):
        size = first_size if i == 0 else rest_size
        weight = "bold" if i == 0 else "normal"
        color = "#1e1e1e" if i == 0 else MUTED
        out += text_svg(x + 12, cursor, line, size=size, weight=weight, color=color, width_chars=wc)
        cursor += (17 if i == 0 else 15)
    return out


def build_pilot_board():
    body = ""

    flow_y = 96
    box_w, box_h = 190, 96
    steps = [
        (["Synthetic alert", "(dummy data)"], BLUE, 40),
        (["Attribute compare", "name, DOB, address,", "nationality, occupation"], BLUE, 250),
        (["Confidence tally", "match vs mismatch count"], YELLOW, 460),
        (["Auto close with", "rationale note", "obvious false positives"], GREEN, 670),
        (["Escalate to L1", "everything else"], ORANGE, 880),
    ]
    for lines, color, x in steps:
        body += box_block(x, flow_y, box_w, box_h, lines, color, width_chars=24)

    for i in range(len(steps) - 1):
        x1 = steps[i][2] + box_w
        x2 = steps[i + 1][2]
        y = flow_y + box_h / 2
        body += arrow_svg(x1 + 4, y, x2 - 4, y)

    body += text_svg(40, flow_y - 20, "The pilot, in this repo", size=15.5, weight="bold")
    body += text_svg(1090, flow_y + box_h / 2 - 6, "back to\nL1 queue", size=11.5, color=MUTED, width_chars=14)

    section_y = 250
    body += text_svg(40, section_y, "Where the code lives", size=15.5, weight="bold")
    code_items = [
        "models.py, the alert and watchlist hit shapes",
        "attributes.py, the same comparisons an analyst runs by hand",
        "scoring.py, match and mismatch tally",
        "decision.py, auto close or escalate, with a written rationale",
        "cli.py, the runnable demo, python -m sanctions_triage.cli",
        "tests/, 11 passing tests over the decision logic",
    ]
    dx, dy, dw, dh, gap = 40, section_y + 22, 560, 46, 10
    for i, item in enumerate(code_items):
        yy = dy + i * (dh + gap)
        body += box_block(dx, yy, dw, dh, [item], WHITE, first_size=13, width_chars=68)

    out_x = 660
    body += text_svg(out_x, section_y, "90 day outcome", size=15.5, weight="bold")
    outcomes = [
        ("Deployed in 90 days", "One individual contributor, Claude Code, real L1 case patterns", VIOLET),
        ("More than $1,000,000 saved over 3 years", "versus licensing UiPath or WorkFusion for this workflow", GREEN),
        ("Under $10,000 a year", "to run and maintain internally, no license renewal", GREEN),
        ("Every auto close carries a rationale", "written for audit, nothing closes silently", WHITE),
    ]
    ow, oh, ogap = 540, 62, 10
    for i, (big, small, color) in enumerate(outcomes):
        yy = dy + i * (oh + ogap)
        body += box_block(out_x, yy, ow, oh, [big, small], color, width_chars=58)

    render("board-3-pilot-and-outcomes", WIDTH, HEIGHT, body, title="What shipped in 90 days")

    # ---- excalidraw scene ----
    elements = []
    for lines, color, xx in steps:
        elements.append(excal_rect(xx, flow_y, box_w, box_h, bg=color))
        elements.append(excal_text(xx + 10, flow_y + 10, "\n".join(lines), font_size=12.5, width=box_w - 20, height=box_h - 20))
    for i in range(len(steps) - 1):
        x1 = steps[i][2] + box_w
        x2 = steps[i + 1][2]
        y = flow_y + box_h / 2
        elements.append(excal_arrow(x1 + 4, y, x2 - 4, y))

    elements.append(excal_text(40, section_y - 14, "Where the code lives", font_size=16, width=400))
    for i, item in enumerate(code_items):
        yy = dy + i * (dh + gap)
        elements.append(excal_rect(dx, yy, dw, dh, bg=WHITE))
        elements.append(excal_text(dx + 10, yy + 12, item, font_size=12, width=dw - 20, height=dh - 20))

    elements.append(excal_text(out_x, section_y - 14, "90 day outcome", font_size=16, width=400))
    for i, (big, small, color) in enumerate(outcomes):
        yy = dy + i * (oh + ogap)
        elements.append(excal_rect(out_x, yy, ow, oh, bg=color))
        elements.append(excal_text(out_x + 10, yy + 8, f"{big}\n{small}", font_size=12, width=ow - 20, height=oh - 12))

    write_scene("board-3-pilot-and-outcomes", elements)


if __name__ == "__main__":
    build_pilot_board()
