# wca-sql-demo
## SQL optimization demo for WCA


For optimizing and resolving SQL issues, clients will need intelligence to inspect existing and new SQL for inefficiencies and stability issues. 

Examples of challenges:
- Blocking queries
- Full Table Scan
- Inefficient Index
- Top CPU consuming queries (will fetch plan details)
- Kill threshold 
- Fragmented tables

This is an automated code assistant to detect SQL for early violation of anti-patterns, both to improve SQL already in production and to harden before deployment to production (either for developers or the CICD pipeline). This should also reduce the tension to move relational data to NoSQL if queries can be easily and consistently improved.

Inspects/Optimizes for…

- Efficiency (cost): CPU, RAM, I/O
- Availability (outages)
    - resource availability (storage, limits, tunable resources)
    - time-outs
    - execution errors
    - noisy neighbors
- Performance (time to execute, identification of poorly written queries)
- Maintainability and Understanding: corporate standards and coding practices
- Portability (for migration between platforms)

Specifically, this intelligence can be used in various stages of the lifecycle:
- Development… New code: Give advice on SQL, etc. … a coding assistant to avoid mistakes
- As an inspector of existing queries… a code scanner and reporter
- Deployment (CICD): Hardening (e.g. AV)
- As Deployed (Github, etc.): Existing code: Static analysis of existing SQL, etc.
- Runtime (through automated or repeated testing): Against real data and configurations (e.g. Explains)
- Production (by inspecting and recommending fixes to poor performing queries showing up in the logs)/
- Maintenance / Fixes: …  a coding assistant, to accelerate fix time and reduce effort

Our code assistant technology excels at evaluating and improving existing code, not just helping people write new code.  Since it also benefits from synergies from having been trained on hundreds of languages and dialects, it can cover a range of pre-defined and unplanned anti-patterns, improving your SQL (various flavors) and related code, schemas, etc, for efficiency, quality, portability, maintainability, and more. 

## Demos

- [SQL Static Code Efficiency](/sql-execution-efficiency.md)
- [SQL Execution Efficiency](/sql-execution-efficiency.md)
- [Backup & Variations](/backup-variations.md)

### Contributors
Many thanks to the diligent work of Kevin Hall, Kyle Jurassic, Hung Tack Kwan, Audrey Velanovich and Michael Hepfer