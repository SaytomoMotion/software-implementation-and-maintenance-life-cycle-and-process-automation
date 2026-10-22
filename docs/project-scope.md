# Motion design project requirements

This local app helps a freelancer keep client briefs, deadlines, revision rounds and delivery
requirements together across animation projects.

- Create projects with a title and client, with an optional brief and deadline.
- Select formats and an agreed revision limit.
- Track briefing, production, review, delivery and hold.
- List by deadline and filter by client, status or overdue work.
- Record revisions, requiring an explicit override beyond the agreed budget.
- Show full project details and a workload summary.
- Keep records across commands in SQLite.
- Upgrade schema 1 to 2 with a backup and preserved records.
- Import old task JSON without changing the source or duplicating IDs.
- Build and test a runnable Python artifact automatically.

This version is a command-line application. It does not control After Effects, render videos,
store media assets, send messages, invoice clients or provide a shared web interface.
Examples use synthetic clients. The Git practical remains on its original separate branch.
