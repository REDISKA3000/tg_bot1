BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "musi" (
	"file"	INTEGER
);
INSERT INTO "musi" VALUES ('DEAD BLONDE - Мальчик на девятке.ogg');
INSERT INTO "musi" VALUES ('Дима Билан - Молния.ogg');
INSERT INTO "musi" VALUES ('Тарас Добровольский - Музыка лечит.ogg');
COMMIT;
