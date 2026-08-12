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

## Mapping the process, not just the numbers

The volume and the false positive rate told me this was worth doing. They did not tell me what to build. Getting to that took mapping out the actual process in detail, in the same sessions as the discovery work above.

- **Current state pain points.** The decision on a case was usually fast. What ate the time was the research behind it: pulling external links, checking open web and news sources, cross referencing internal systems, resolving a date of birth or address that almost matched but not quite, reviewing AML Insights, and then writing a closing note that looked a lot like the last twenty. None of that research was optional or skippable, and none of it was the same case to case, which is exactly why it could not be solved with a simple rule.
- **Stakeholder needs.** L1 analysts wanted the repetitive research off their plate without losing the judgment calls that actually needed a person. L2 wanted confidence that whatever got auto closed would never land back on their desk as an escalation that should not have been closed. QA wanted closing notes and decision logic consistent enough to actually audit, not just fast. Financial crime operations leadership wanted the false positive rate down without adding headcount and without losing the audit trail. The offshore team needed daily volume covered without disruption while any of this was being tested. Four different groups, four different bars to clear, all with the same pilot.
- **Decision flow.** How an alert actually moved: Bridger screened customer, transaction, vendor, and employee data against OFAC, sanctions, PEP, enforcement, and adverse media lists, sorted results into a review queue, and from there an analyst compared name, date of birth, address, nationality, occupation, and entity type against the hit before closing it as a false positive or escalating it, with confirmed referrals moving into Verafin for case management. The pilot logic had to sit inside that exact flow, not replace it, since Verafin and the review queue were not going anywhere.
- **Data and technical constraints.** What Bridger actually returned per alert, which attributes were reliable enough to compare programmatically and which still needed a human read, and where the pilot could and could not safely make a call without a person in the loop.
- **Target state.** Auto close only where the evidence was unambiguous, entity type mismatch or two or more contradicting attributes with nothing confirming the hit. Everything else stayed with L1 exactly as it worked before this pilot existed. No new tool for analysts to learn, no new system for QA to audit outside the existing process.
- **The wish list.** The three other manual workflows named above were the team's wish list beyond this pilot's scope, written down during the same discovery pass so they were not lost, and used later to justify the next piece of work instead of starting the next conversation from zero.

## Scoping it before building it

Before any code got written, financial crime operations leadership and I agreed on two conditions. The pilot could only auto close an alert when the evidence was unambiguous, meaning the entity type did not match or two or more attributes actively contradicted the hit with nothing confirming it. Anything short of that stayed with L1, unchanged. And it had to be live within the quarter, not a multi quarter buildout. Everything else was a stretch goal, not a requirement. That scope is what made the buy versus build call straightforward, since a vendor implementation calendar could not hit either condition.

## Who owned what

- I owned the discovery synthesis, the scope and timeline commitment, the attribute comparison and decision logic, the written rationale behind every auto closed alert, and the readout back to leadership.
- Financial crime operations leadership owned the final call on what evidence counted as unambiguous enough to auto close, and owns the audit trail requirement this pilot had to satisfy.
- The L1 review team, L2 escalation reviewers, and QA analysts owned validating the logic against real case patterns and flagging anything that did not match how they actually worked a case.
- The offshore team continued carrying daily volume throughout, since this pilot never touched anything beyond the unambiguous false positive slice.

Because I owned this as an individual contributor, there was no steering committee between a case pattern not holding up and a fix going in. I adjusted the same day.

## Bringing the team along, not just the code

None of this worked if the L1, L2, and QA team did not trust it. I walked them through why a case got auto closed, not just that it did, using their own case patterns as the examples, so the logic was something they had seen validated with their own eyes rather than something handed to them finished. That mattered more for QA and L2 than for anyone else, since they were the ones who had to be comfortable defending the logic in an audit, not just using it day to day.

The same underlying approach, shadow the work first, quantify it, agree on a guardrail and a timeline before building anything, validate against real cases with the people who do the work, then read the result back and use it to point at what is next, is not something I only used once. The [related IT ticket triage work](../related-work/it-ticket-triage-agent/) linked from the README applies that same sequence to a completely different queue and a completely different team. Writing the approach down instead of carrying it only in my head is what let someone else pick it up for their own queue.

## Presenting it back

Once the pilot was running, the readout to financial crime operations leadership covered three things: the volume it was actually clearing, the cost avoided against the vendor path, and the audit trail behind every decision. That readout is what connected this pilot to the larger conversation about the broader agentic AI program across fraud, disputes, and financial crime described on the [Stakeholders page](Stakeholders.md), and it is what put the other three manual workflows from discovery on the table as the next pieces worth scoping.
