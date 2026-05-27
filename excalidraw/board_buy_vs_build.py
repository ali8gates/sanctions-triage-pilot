"""Board 2: buy vs build.

Compares the vendor RPA path against the Accenture-proposed agentic program
against the path I actually took: build the sanctions triage slice myself,
in the open, with Claude Code, using the same team's real cases.
"""

from build_boards import (
    ORANGE, RED, BLUE, GREEN, YELLOW, WHITE, VIOLET, MUTED,
    arrow_svg, render, rough_rect_svg, text_svg,
    excal_rect, excal_text, excal_arrow, write_scene,
)

WIDTH, HEIGHT = 1240, 760

COLUMNS = [
    {
        "title": "UiPath",
        "sub": "vendor RPA license",
        "color": WHITE,
        "rows": [
            "Per-bot licensing plus implementation services",
            "Rules based automation, not attribute reasoning",
            "Multi month vendor implementation cycle",
            "Ongoing license renewal every year",
        ],
    },
    {
        "title": "WorkFusion",
        "sub": "vendor RPA license",
        "color": WHITE,
        "rows": [
            "Similar licensing model to UiPath",
            "Pre-built AML connectors, still rules based",
            "Vendor controls the roadmap and pace of change",
            "Ongoing license renewal every year",
        ],
    },
    {
        "title": "Accenture program",
        "sub": "agentic AI, UiPath bots plus Claude Code",
        "color": VIOLET,
        "rows": [
            "13 workflows across fraud, disputes, financial crime",
            "35 to 50% efficiency target across the program",
            "Phased delivery, 3 to 5 months",
            "Right scope for the full YAMS and DBC surface",
        ],
    },
    {
        "title": "Build it myself",
        "sub": "what I actually did",
        "color": GREEN,
        "rows": [
            "Claude Code, working directly with L1 and L2",
            "Attribute level reasoning on real case patterns",
            "Deployed in 90 days, one individual contributor",
            "Under $10k a year to run and maintain",
        ],
    },
]


def col_block(x, y, w, title, sub, rows, color, row_h=54, gap=10):
    out = ""
    header_h = 70
    out += rough_rect_svg(x, y, w, header_h, color)
    out += text_svg(x + 12, y + 24, title, size=16, weight="bold", width_chars=26)
    out += text_svg(x + 12, y + 42, sub, size=11.5, color=MUTED, width_chars=30)
    cursor = y + header_h + 14
    for row in rows:
        out += rough_rect_svg(x, cursor, w, row_h, WHITE)
        out += text_svg(x + 12, cursor + 22, row, size=12, width_chars=30)
        cursor += row_h + gap
    return out, cursor


def build_buy_vs_build_board():
    body = ""
    col_w, col_gap = 275, 25
    top_y = 90

    x = 40
    bottoms = []
    for col in COLUMNS:
        block, bottom = col_block(x, top_y, col_w, col["title"], col["sub"], col["rows"], col["color"])
        body += block
        bottoms.append(bottom)
        x += col_w + col_gap

    decision_y = max(bottoms) + 40
    body += text_svg(40, decision_y, "What I picked and why", size=15.5, weight="bold")
    body += rough_rect_svg(40, decision_y + 16, 1160, 90, GREEN)
    body += text_svg(
        58, decision_y + 42,
        "I built the L1 sanctions and PEP triage slice myself with Claude Code inside the 90 days, "
        "sitting next to the same broader Accenture-proposed program rather than separate from it. "
        "The vendor platforms needed a multi month buildout and a recurring license for a workflow "
        "this well defined. Owning it myself meant the fix shipped before the vendor conversation "
        "even finished, and it kept running for a fraction of the cost.",
        size=13, width_chars=132, color="#1e1e1e",
    )

    render("board-2-buy-vs-build", WIDTH, HEIGHT, body, title="Buy vs build, sanctions triage")

    # ---- excalidraw scene ----
    elements = []
    x = 40
    for col in COLUMNS:
        header_h = 56
        elements.append(excal_rect(x, top_y, col_w, header_h, bg=col["color"]))
        elements.append(excal_text(x + 10, top_y + 8, f"{col['title']}\n{col['sub']}", font_size=13, width=col_w - 20, height=header_h - 12))
        cursor = top_y + header_h + 14
        for row in col["rows"]:
            elements.append(excal_rect(x, cursor, col_w, 54, bg=WHITE))
            elements.append(excal_text(x + 10, cursor + 8, row, font_size=12, width=col_w - 20, height=40))
            cursor += 54 + 10
        x += col_w + col_gap

    elements.append(excal_text(40, decision_y - 14, "What I picked and why", font_size=16, width=400))
    elements.append(excal_rect(40, decision_y + 2, 1160, 90, bg=GREEN))
    elements.append(excal_text(
        58, decision_y + 14,
        "I built the L1 sanctions and PEP triage slice myself with Claude Code inside the 90 days, "
        "sitting next to the same broader Accenture-proposed program rather than separate from it.",
        font_size=13, width=1120, height=70,
    ))

    write_scene("board-2-buy-vs-build", elements)


if __name__ == "__main__":
    build_buy_vs_build_board()
