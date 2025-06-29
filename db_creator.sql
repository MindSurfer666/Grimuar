CREATE TABLE object_memory
(
    object_id        INTEGER NOT NULL  -- Убрано DEFAULT, так как для PRIMARY KEY это излишне
        CONSTRAINT object_memory_pk
            PRIMARY KEY,
    object_name      TEXT,
    object_href      TEXT,
    object_1         BOOLEAN,
    object_3         BOOLEAN,
    object_7         BOOLEAN,
    object_14        BOOLEAN,
    object_31        BOOLEAN,
    object_62        BOOLEAN,
    object_timestamp DATE
);

alter table object_memory
    owner to mindsurfer;