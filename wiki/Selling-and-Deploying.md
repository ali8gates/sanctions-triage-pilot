# Selling and Deploying This

The other pages cover the problem, the discovery, and what shipped. This page is about the parts of the job that were not writing code: understanding what the customer of this pilot actually needed, weighing a vendor pitch the way a buyer does, and getting something new into a live, audited process without breaking anything.

## Who my customer was

Financial crime operations leadership and the review team were the customers of this pilot, even though nothing here ever touched an external client. What they needed was not "automation," it was something narrower and harder to fake: a tool that would not close a real or ambiguous match, that left a written reason behind every decision, and that would not need a headcount increase to maintain. Understanding that bar, and designing to it instead of to a generic automation pitch, was as much the job as the comparison logic itself.

## Evaluating vendors the way a customer does

Part of scoping this meant sitting through what UiPath and WorkFusion were actually offering, the same way any buyer sits through a vendor pitch: what does this actually solve versus what does the deck say it solves, what does it cost over three years and not just year one, how long until something is live, and who is still accountable when a case gets closed wrong. Both were rules based, both meant a multi month implementation and a license that renewed every year regardless of how much the workflow changed. Weighing that against building it myself was a sales evaluation from the buyer's seat, and it is the same evaluation described on the [Buy vs Build page](Buy-vs-Build.md).

## Selling the build-it-myself option internally

Before any code got written, I had to make the case to financial crime operations leadership that skipping the vendor path was the right call, not just the cheaper one. That pitch rested on three things: a number (more than two million dollars avoided over two years against either vendor), a timeline (live within the quarter, not a multi quarter vendor buildout), and a guardrail (auto close only where the evidence was unambiguous, everything else stays with L1 exactly as before). Without all three, it would have been a much harder sell, and probably the wrong call.

## Deployment strategy

This did not go live all at once, and it did not go live on trust either. The same shape holds every time a new automated decision is about to touch a live, audited process: agree on what "working" means before anything touches real alerts, run it against a bounded slice for a defined period, check the actual results against that bar instead of a gut feeling, then clear the compliance equivalent of procurement before it touches full volume.

Concretely, that looked like this. Before any code ran against a real alert, the bar was set in advance: no closing a real or ambiguous match, a written reason behind every decision, no headcount increase to maintain it. It started against the narrowest, lowest risk slice of the queue, the alerts where the entity type itself did not match or where two or more attributes actively contradicted the hit with nothing confirming it, for long enough that the L1, L2, and QA team could validate the logic against a real volume of case patterns rather than a handful of examples. Only after that validation held did it move to daily volume, and only after compliance and audit had reviewed the decision trail and signed off on it as an auditable process, not just a working one. Once it was running at volume, the readout back to leadership covered what it was actually clearing, what it cost to run, and the audit trail behind every decision, and that result is what put the [other manual workflows surfaced during discovery](Problem.md) on the table as the next candidates for the same approach.
