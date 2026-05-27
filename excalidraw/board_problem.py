"""Board 1: the problem, as it existed before this pilot.

AS-IS alert review flow, plus the pain points and staffing reality that
made this worth solving.
"""

from build_boards import (
    ORANGE, RED, BLUE, GREEN, YELLOW, WHITE, MUTED, STROKE,
    arrow_svg, render, rough_rect_svg, text_svg,
    excal_rect, excal_text, excal_arrow, write_scene,
)

WIDTH, HEIGHT = 1240, 900


def box_block(x, y, w, h, lines, fill, first_size=14.5, rest_size=12, width_chars=None):
    wc = width_chars or max(16, int(w / 6.6))
    out = rough_rect_svg(x, y, w, h, fill)
    cursor = y + 24
    for i, line in enumerate(lines):
        size = first_size if i == 0 else rest_size
        weight = "bold" if i == 0 else "normal"
        color = "#1e1e1e" if i == 0 else MUTED
        out += text_svg(x + 12, cursor, line, size=size, weight=weight, color=color, width_chars=wc)
        cursor += (18 if i == 0 else 15)
    return out


def build_problem_board():
    body = ""

    flow_y = 96
    box_w, box_h = 200, 100
    steps = [
        (["Customer, transaction,", "vendor, employee data"], BLUE, 40),
        (["Bridger (LexisNexis)", "screening engine"], BLUE, 262),
        (["Alerts sorted into", "review queues"], YELLOW, 484),
        (["Analyst compares", "name, DOB, address,", "nationality, occupation"], ORANGE, 706),
        (["Close as false positive", "or escalate"], GREEN, 984),
    ]
    for lines, color, x in steps:
        body += box_block(x, flow_y, box_w, box_h, lines, color, width_chars=26)

    for i in range(len(steps) - 1):
        x1 = steps[i][2] + box_w
        x2 = steps[i + 1][2]
        y = flow_y + box_h / 2
        body += arrow_svg(x1 + 4, y, x2 - 4, y)

    section_y = 250
    body += text_svg(40, section_y, "Where the analyst time actually goes", size=15.5, weight="bold")
    detail_items = [
        "External links, open web and news search",
        "Internal systems and account history",
        "Address, DOB, and identity discrepancy checks",
        "AML Insights review",
        "Confirming the hit is actually related to the customer",
        "Writing a similar closing note, case after case",
    ]
    dx, dy, dw, dh, gap = 40, section_y + 22, 370, 58, 12
    for i, item in enumerate(detail_items):
        yy = dy + i * (dh + gap)
        body += box_block(dx, yy, dw, dh, [item], WHITE, first_size=13, width_chars=44)

    vol_x = 440
    body += text_svg(vol_x, section_y, "Alert volume, 4 month average", size=15.5, weight="bold")
    volumes = [
        ("3,750 / month", "Name sanctions and PEP alerts"),
        ("1,500 / month", "Adverse media alerts"),
        ("320 / month", "Payment screening alerts"),
        ("90 / night", "Full customer base vs OFAC, sanctions, foreign PEP"),
        ("108 / week", "Transaction active customers vs domestic PEP"),
        ("48 / week", "Transaction active subset vs adverse media"),
    ]
    vw, vh, vgap = 370, 66, 12
    for i, (big, small) in enumerate(volumes):
        yy = dy + i * (vh + vgap)
        body += box_block(vol_x, yy, vw, vh, [big, small], YELLOW, width_chars=44)

    fp_x = 850
    body += text_svg(fp_x, section_y, "The reality behind the queue", size=15.5, weight="bold")
    facts = [
        ("99% false positive", "Name sanctions and PEP, 15 true matches in 63,000 alerts over 3 years"),
        ("97.7% false positive", "Adverse media, 337 true matches in 15,000 alerts over 12 months"),
        ("100% false positive", "Payment screening, and this is expected"),
        ("7 L1, 3 L2, 2 QA analysts", "11 offshore with Accenture, 1 Varo FTE"),
        ("2 to 20 minutes per alert", "Quick false positive about 2 min, harder cases 15 to 20 min"),
    ]
    fw, fh, fgap = 350, 72, 12
    for i, (big, small) in enumerate(facts):
        yy = dy + i * (fh + fgap)
        color = RED if "false positive" in big else (ORANGE if "analysts" in big else WHITE)
        body += box_block(fp_x, yy, fw, fh, [big, small], color, width_chars=46)

    render("board-1-the-problem", WIDTH, HEIGHT, body, title="Sanctions and PEP alert review, before this pilot")

    # ---- excalidraw scene ----
    elements = []
    for lines, color, xx in steps:
        elements.append(excal_rect(xx, flow_y, box_w, box_h, bg=color))
        elements.append(excal_text(xx + 10, flow_y + 10, "\n".join(lines), font_size=13, width=box_w - 20, height=box_h - 20))
    for i in range(len(steps) - 1):
        x1 = steps[i][2] + box_w
        x2 = steps[i + 1][2]
        y = flow_y + box_h / 2
        elements.append(excal_arrow(x1 + 4, y, x2 - 4, y))

    elements.append(excal_text(40, section_y - 14, "Where the analyst time actually goes", font_size=16, width=400))
    for i, item in enumerate(detail_items):
        yy = dy + i * (dh + gap)
        elements.append(excal_rect(dx, yy, dw, dh, bg=WHITE))
        elements.append(excal_text(dx + 10, yy + 12, item, font_size=12, width=dw - 20, height=dh - 20))

    elements.append(excal_text(vol_x, section_y - 14, "Alert volume, 4 month average", font_size=16, width=400))
    for i, (big, small) in enumerate(volumes):
        yy = dy + i * (vh + vgap)
        elements.append(excal_rect(vol_x, yy, vw, vh, bg=YELLOW))
        elements.append(excal_text(vol_x + 10, yy + 8, f"{big}\n{small}", font_size=12, width=vw - 20, height=vh - 12))

    elements.append(excal_text(fp_x, section_y - 14, "The reality behind the queue", font_size=16, width=400))
    for i, (big, small) in enumerate(facts):
        yy = dy + i * (fh + fgap)
        color = RED if "false positive" in big else (ORANGE if "analysts" in big else WHITE)
        elements.append(excal_rect(fp_x, yy, fw, fh, bg=color))
        elements.append(excal_text(fp_x + 10, yy + 8, f"{big}\n{small}", font_size=12, width=fw - 20, height=fh - 12))

    write_scene("board-1-the-problem", elements)


if __name__ == "__main__":
    build_problem_board()
