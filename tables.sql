CREATE TABLE DATASET_1
(
    CODE         TEXT NOT NULL,
    VALUE        INT  NOT NULL,
    TIME_CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT DATASET_1_CH CHECK (DATASET_1.VALUE >= 0)
);

CREATE TABLE DATASET_2
(
    CODE         TEXT NOT NULL,
    VALUE        INT  NOT NULL,
    TIME_CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT DATASET_1_CH CHECK (DATASET_2.VALUE >= 0)
);

CREATE TABLE DATASET_3
(
    CODE         TEXT NOT NULL,
    VALUE        INT  NOT NULL,
    TIME_CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT DATASET_1_CH CHECK (DATASET_3.VALUE >= 0)
);

CREATE TABLE DATASET_4
(
    CODE         TEXT NOT NULL,
    VALUE        INT  NOT NULL,
    TIME_CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT DATASET_1_CH CHECK (DATASET_4.VALUE >= 0)
);