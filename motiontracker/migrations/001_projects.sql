CREATE TABLE projects (
    id TEXT PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    client TEXT NOT NULL,
    brief TEXT NOT NULL DEFAULT '',
    deadline TEXT,
    status TEXT NOT NULL DEFAULT 'briefing'
        CHECK (status IN ('briefing', 'in_progress', 'review', 'delivered', 'on_hold'))
);
