CREATE TABLE IF NOT EXISTS schedules (
    id BIGSERIAL PRIMARY KEY,
    calendar_name TEXT NOT NULL,
    schedule_description TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    weekdays SMALLINT[] NOT NULL CHECK (
        weekdays <@ ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[]
    ),
    arrange_type TEXT NOT NULL CHECK (arrange_type IN ('early', 'late', 'auto')),
    UNIQUE (calendar_name, schedule_description)
);

CREATE INDEX IF NOT EXISTS idx_schedules_weekdays
    ON schedules USING GIN (weekdays);

COMMENT ON COLUMN schedules.weekdays IS '0=Monday, 1=Tuesday, ..., 6=Sunday';
COMMENT ON COLUMN schedules.arrange_type IS 'early=as early as possible, late=as late as possible, auto=largest free slot first';

INSERT INTO schedules (
    calendar_name,
    schedule_description,
    duration_minutes,
    weekdays,
    arrange_type
) VALUES
    ('Normal', '健身', 30, ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[], 'early'),
    ('IELTS', '复盘昨日四级单词', 20, ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[], 'early'),
    ('IELTS', '墨墨背单词', 20, ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[], 'early'),
    ('IELTS', '背四级单词', 90, ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[], 'auto'),
    ('IELTS', '单词抄写', 20, ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[], 'auto'),
    ('IELTS', '复盘四级单词', 60, ARRAY[4]::SMALLINT[], 'auto'),
    ('IELTS', '复盘今日四级单词', 20, ARRAY[0, 1, 2, 3, 4, 5, 6]::SMALLINT[], 'late')
ON CONFLICT (calendar_name, schedule_description) DO NOTHING;
