BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "mus/author" (
	"ID"	TEXT,
	"field_id"	TEXT,
	"right_answer"	TEXT,
	"wrong_answer"	TEXT
);
INSERT INTO "mus/author" VALUES ('2','aaba','f','e,f,g,h');
INSERT INTO "mus/author" VALUES ('3','aabb','i','i,g,k,l');
INSERT INTO "mus/author" VALUES ('4','aaaa','x','h,f,s,x');
COMMIT;
