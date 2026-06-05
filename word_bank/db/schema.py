SCHEMA = """
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
