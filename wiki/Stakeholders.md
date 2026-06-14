# Stakeholders

Real names never appear in this repo. People here are described by role.

## Who was in the room

- Financial crime operations leadership, who owned the sanctions and PEP program and cared most about the false positive rate and audit trail
- The sanctions and PEP review team (7 L1 analysts), who worked the queue every day and knew exactly which cases were a waste of their time before I ever opened a spreadsheet
- L2 escalation reviewers (3 analysts), who saw the harder cases and the patterns that repeated across them
- QA analysts (2), who checked closure quality and were the first to flag when a closing note pattern was safe to standardize
- The offshore review team, staffed through Accenture, who carried the majority of daily volume

## How I worked with them

I did not start from a spec. I started by sitting with the discovery notes from the L1 and L2 team directly: what attributes they actually compared, how long a case really took, which alerts were obviously a false positive within seconds versus which ones needed real digging. That discovery work became the ground truth the pilot logic was built against.

Because I owned this piece as an individual contributor, decisions moved fast. I did not need a steering committee to change a threshold or add a rationale field, I tested it against real case patterns with the team that would use it and adjusted the same day.

## Where this connects to the bigger picture

This sanctions and PEP slice sits inside the same broader agentic AI program proposed for Varo across fraud (YAMS and its related queues), disputes (DBC and its related queues), and financial crime more broadly, 13 workflows in total, targeting 35 to 50 percent efficiency gains delivered in phases over 3 to 5 months. Financial crime operations leadership sponsored that broader conversation. My pilot was the concrete, already-working piece of it I could point to.
