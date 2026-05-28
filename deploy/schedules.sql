CREATE TABLE IF NOT EXISTS schedules (
    id BIGSERIAL PRIMARY KEY,
    calendar_name TEXT NOT NULL,
    schedule_description TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    weekdays SMALLINT[] NOT NULL CHECK (
        weekdays <@ ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[]
    ),
    arrange_type TEXT NOT NULL CHECK (arrange_type IN ('early', 'late', 'auto')),
    sort_order BIGINT NOT NULL,
    UNIQUE (calendar_name, schedule_description)
);

ALTER TABLE schedules
    ADD COLUMN IF NOT EXISTS sort_order BIGINT;

UPDATE schedules
SET sort_order = id
WHERE sort_order IS NULL;

ALTER TABLE schedules
    ALTER COLUMN sort_order SET NOT NULL;

CREATE INDEX IF NOT EXISTS idx_schedules_weekdays
    ON schedules USING GIN (weekdays);

CREATE INDEX IF NOT EXISTS idx_schedules_sort_order
    ON schedules (sort_order, id);

COMMENT ON COLUMN schedules.weekdays IS '0=Monday, 1=Tuesday, ..., 6=Sunday';
COMMENT ON COLUMN schedules.arrange_type IS 'early=as early as possible, late=as late as possible, auto=largest free slot first';
COMMENT ON COLUMN schedules.sort_order IS 'Display order used by the schedules API';

INSERT INTO schedules (
    calendar_name,
    schedule_description,
    duration_minutes,
    weekdays,
    arrange_type,
    sort_order
) VALUES
    ('Normal', '健身', 30, ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[], 'early', 1),
    ('IELTS', '复盘昨日四级单词', 20, ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[], 'early', 2),
    ('IELTS', '墨墨背单词', 20, ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[], 'early', 3),
    ('IELTS', '背四级单词', 90, ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[], 'auto', 4),
    ('IELTS', '单词抄写', 20, ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[], 'auto', 5),
    ('IELTS', '复盘四级单词', 60, ARRAY[4]::SMALLINT[], 'auto', 6),
    ('IELTS', '复盘今日四级单词', 20, ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[], 'late', 7)
ON CONFLICT (calendar_name, schedule_description) DO NOTHING;
