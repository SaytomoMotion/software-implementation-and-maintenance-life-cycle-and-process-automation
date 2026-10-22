ALTER TABLE projects ADD COLUMN revision_limit INTEGER NOT NULL DEFAULT 2
    CHECK (revision_limit >= 0);
ALTER TABLE projects ADD COLUMN revision_count INTEGER NOT NULL DEFAULT 0
    CHECK (revision_count >= 0);
ALTER TABLE projects ADD COLUMN delivery_formats TEXT NOT NULL DEFAULT '["mp4"]';
CREATE INDEX projects_deadline_idx ON projects(deadline);
