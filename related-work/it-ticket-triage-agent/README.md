# IT Ticket Triage Agent

This is a separate piece of work from the sanctions triage pilot above it in this repo, kept here because it uses the same underlying agent pattern: a policy layer that makes a decision and writes down why, an orchestrator that turns that into an auditable outcome, and a human review queue for anything the policy is not confident about.

The real version of this covered internal IT support tickets end to end, from intake through routing and escalation, for a support team handling a steady stream of password resets, software install requests, and access requests. I built the prioritization framework behind it, quantified the cost and volume of the highest frequency ticket types, and presented the business case and next-phase options to leadership.

Everything in this folder is synthetic. The tickets below are invented examples that walk through every decision path the policy supports, not real requests or real people.

## The three ticket types and their decision paths

- Password resets always auto-approve and are always logged. There is no version of this where a human needs to look at a routine reset.
- Software installs auto-approve cleanly if the software is on the approved catalog. Off catalog, the agent checks whether the justification ties the request to a specific work task before approving it, otherwise it escalates.
- Access requests are the one category where role and system sensitivity genuinely gate the decision. A standard allowlist match for the requester's role auto-approves. A high-sensitivity system escalates every time, regardless of justification. Anything off the allowlist with a weak or unclear justification also escalates.

## What's here

- [`agent/policy.py`](agent/policy.py), the rules layer, returns a decision and a written reason for every ticket
- [`agent/orchestrator.py`](agent/orchestrator.py), runs a ticket through policy, logs it, and routes escalations to the human review queue
- [`demo.py`](demo.py), seven synthetic tickets chosen to hit every decision path described above
- [`tests/`](tests/), covers each decision path plus the queue behavior

## Run the demo

```
cd related-work/it-ticket-triage-agent
python demo.py
```

This processes seven synthetic tickets and prints a decision, a written rationale, and a summary for each one, followed by a count of how many landed in the human review queue versus resolved automatically.

Run the tests with:

```
cd related-work/it-ticket-triage-agent
python -m pytest tests
```
