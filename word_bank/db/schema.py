SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS verbs (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    base TEXT NOT NULL,
    infinitive TEXT,
    present_participle TEXT,
    past TEXT,
    past_participle TEXT,
    portuguese TEXT
);

CREATE TABLE IF NOT EXISTS be_forms (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    base TEXT NOT NULL,
    infinitive TEXT,
    present_participle TEXT,
    past TEXT,
    past_participle TEXT,
    portuguese TEXT
);

CREATE TABLE IF NOT EXISTS adjectives (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    english TEXT NOT NULL,
    portuguese TEXT
);

CREATE TABLE IF NOT EXISTS possessive_adjectives (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    person TEXT NOT NULL,
    form TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS nouns (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    singular TEXT NOT NULL,
    plural TEXT,
    portuguese TEXT
);

CREATE TABLE IF NOT EXISTS subject_pronouns (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    person TEXT NOT NULL,
    form TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS object_pronouns (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    person TEXT NOT NULL,
    form TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS possessive_pronouns (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    person TEXT NOT NULL,
    form TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tense_examples (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    number INTEGER,
    simple_present TEXT,
    present_continuous TEXT,
    simple_past TEXT,
    simple_future TEXT,
    present_perfect TEXT
);

CREATE TABLE IF NOT EXISTS yesno_examples (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    situation TEXT NOT NULL,
    yesno_question TEXT,
    response TEXT,
    wh_question TEXT,
    statement TEXT
);

CREATE INDEX IF NOT EXISTS idx_verbs_user ON verbs (user_id);
CREATE INDEX IF NOT EXISTS idx_be_forms_user ON be_forms (user_id);
CREATE INDEX IF NOT EXISTS idx_adjectives_user ON adjectives (user_id);
CREATE INDEX IF NOT EXISTS idx_possessive_adjectives_user ON possessive_adjectives (user_id);
CREATE INDEX IF NOT EXISTS idx_nouns_user ON nouns (user_id);
CREATE INDEX IF NOT EXISTS idx_subject_pronouns_user ON subject_pronouns (user_id);
CREATE INDEX IF NOT EXISTS idx_object_pronouns_user ON object_pronouns (user_id);
CREATE INDEX IF NOT EXISTS idx_possessive_pronouns_user ON possessive_pronouns (user_id);
CREATE INDEX IF NOT EXISTS idx_tense_examples_user ON tense_examples (user_id);
CREATE INDEX IF NOT EXISTS idx_yesno_examples_user ON yesno_examples (user_id);
"""

TABLES = [
    "verbs",
    "be_forms",
    "adjectives",
    "possessive_adjectives",
    "nouns",
    "subject_pronouns",
    "object_pronouns",
    "possessive_pronouns",
    "tense_examples",
    "yesno_examples",
]
