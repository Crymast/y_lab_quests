CREATE TABLE "menu"
(
    "id"            serial NOT NULL PRIMARY KEY,
    "title"         text   NOT NULL,
    "description"   text   NOT NULL
);

CREATE TABLE "subMenu"
(
    "id"            serial  NOT NULL PRIMARY KEY,
    "title"         text    NOT NULL,
    "description"   text   NOT NULL,
    "menu_id"       integer REFERENCES "menu" ("id") NOT NULL
);

CREATE TABLE "dish"
(
    "id"            serial  NOT NULL PRIMARY KEY,
    "title"         text    NOT NULL,
    "description"   text   NOT NULL,
    "price"         float   NOT NULL,
    "subMenu_id"    integer REFERENCES "subMenu" ("id") NOT NULL
);
