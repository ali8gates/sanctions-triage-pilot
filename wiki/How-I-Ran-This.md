# How I Ran This

Pages elsewhere in this wiki cover the problem, the buy versus build call, and what shipped. This page is about the sequence I actually followed to get there, and who owned which part of it.

## The pattern

1. Shadow the team doing the work today and write down what they actually do, not what the process document says they do.
2. Turn that into numbers: alert volume, time per case, false positive rate, headcount behind the queue.
3. Set a scope and a timeline before writing any code, and agree on what counts as done.
4. Build against real case patterns, not synthetic assumptions, and adjust the same day something does not hold up.
5. Report back what shipped and what it changed, and use that to point at the next highest value piece of work.

## Discovery

I sat with the L1 and L2 review team and went through live cases with them, not a sample deck. That is where the attribute list came from (name, date of birth, address, nationality, occupation, entity type), where the review time ranges came from, and where the false positive rates came from. None of that was estimated after the fact. It was written down during discovery and the pilot logic was built to match it.

That same discovery pass surfaced three other manual workflows the team wanted solved (IAT transaction separation, financial crime customer messaging, monthly TPRM screening, all covered on the [Problem page](Problem.md)). I did not build those. I scoped this pilot to the highest volume, most repetitive piece first, and left the other three written down as the next candidates.

## Scoping it before building it

Before any code got written, financial crime operations leadership and I agreed on two conditions. The pilot could only auto close an alert when the evidence was unambiguous, meaning the entity type did not match or two or more attributes actively contradicted the hit with nothing confirming it. Anything short of that stayed with L1, unchanged. And it had to be live within the quarter, not a multi quarter buildout. Everything else was a stretch goal, not a requirement. That scope is what made the buy versus build call straightforward, since a vendor implementation calendar could not hit either condition.

## Who owned what

- I owned the discovery synthesis, the scope and timeline commitment, the attribute comparison and decision logic, the written rationale behind every auto closed alert, and the readout back to leadership.
- Financial crime operations leadership owned the final call on what evidence counted as unambiguous enough to auto close, and owns the audit trail requirement this pilot had to satisfy.
- The L1 review team, L2 escalation reviewers, and QA analysts owned validating the logic against real case patterns and flagging anything that did not match how they actually worked a case.
- The offshore team continued carrying daily volume throughout, since this pilot never touched anything beyond the unambiguous false positive slice.

Because I owned this as an individual contributor, there was no steering committee between a case pattern not holding up and a fix going in. I adjusted the same day.

## Presenting it back

Once the pilot was running, the readout to financial crime operations leadership covered three things: the volume it was actually clearing, the cost avoided against the vendor path, and the audit trail behind every decision. That readout is what connected this pilot to the larger conversation about the broader agentic AI program across fraud, disputes, and financial crime described on the [Stakeholders page](Stakeholders.md), and it is what put the other three manual workflows from discovery on the table as the next pieces worth scoping.
