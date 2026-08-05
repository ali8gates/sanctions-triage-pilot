# Sanctions Triage Pilot

A fun way to walk through a real pilot: I took the most repetitive slice of Varo's sanctions and PEP alert review, watched exactly where the analyst minutes went, and built a working triage pass with Claude Code in 90 days. One individual contributor, real case patterns, no vendor license.

This sits inside the same broader agentic AI program Accenture proposed for Varo across fraud, disputes, and financial crime. My piece was the sanctions and PEP alert review slice, and I owned it end to end, from the discovery notes to the code that runs today.

Everything in this repo uses synthetic, invented data. Real customer records, real watchlist hits, and real stakeholder names never appear here. Where I use exact figures (alert volumes, false positive rates, staffing, vendor names), those come from the discovery notes I wrote up during the pilot, and they are the real numbers behind why this was worth building.

## What's here

- [The problem](wiki/Problem.md), what the alert queue actually looked like before this pilot
- [Stakeholders](wiki/Stakeholders.md), who was in the room and why
- [How I ran this](wiki/How-I-Ran-This.md), the discovery to readout sequence and who owned each part of it
- [Selling and deploying this](wiki/Selling-and-Deploying.md), evaluating the vendor pitches, selling the build-it-myself call internally, and how it actually rolled out
- [Buy vs build](wiki/Buy-vs-Build.md), UiPath, WorkFusion, the Accenture program, and why I built this piece myself
- [The pilot and the outcome](wiki/Pilot-and-Outcomes.md), what shipped in 90 days and what it saved
- [The code](src/sanctions_triage/), a runnable version of the triage logic, synthetic data only

## Run the demo

```
cd src
python -m sanctions_triage.cli
```

This runs the triage pipeline over six synthetic sample alerts and prints a decision, a written rationale, and a batch summary for each one. Nothing here reaches out to a real system, everything is invented data checked into this repo.

Run the tests with:

```
python -m pytest tests
```

## The whiteboards

The three boards under [excalidraw/](excalidraw/) were built as real Excalidraw scenes:

- `board-1-the-problem.excalidraw`, the as-is alert review flow and the numbers behind it
- `board-2-buy-vs-build.excalidraw`, UiPath and WorkFusion against the Accenture program against building it myself
- `board-3-pilot-and-outcomes.excalidraw`, what the pilot actually does and what it returned

Each `.excalidraw` file opens directly in [Excalidraw](https://excalidraw.com), drag it onto the canvas or use File, Open. The matching `.png` next to each one is a static preview so the boards show up on GitHub without opening the app.

## A note on scope

This repo covers the front end alert review step, the highest volume and most manual part of the workflow. Downstream investigation of a true match, actual SAR filing, and the rest of the financial crime program are out of scope here, and any figures I mention (the true match counts, the false positive rates) describe the review step, not the outcome of an investigation.

## Related work: a different queue, the same pattern

[`related-work/it-ticket-triage-agent/`](related-work/it-ticket-triage-agent/) is a separate project, an IT ticket triage agent built for a different team and a different queue entirely (password resets, software installs, access requests). It is not part of the sanctions pilot and uses none of the same code. It is here because it is built on the same underlying pattern: a policy layer that returns a decision and a written reason, and an orchestrator that turns that into an auditable outcome with a human review queue for anything the policy is not confident about. Worth a look if you want to see the same approach applied somewhere else.
