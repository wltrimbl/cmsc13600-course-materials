t1:
col1    col2
A       5
B       3
C       1
D       5

t2:
col3    col4
A       foo
A       bar
C       baz
E       foo

CREATE TABLE t1(
col1 varchar(10),
col2 int );
CREATE TABLE t2(
col3 varchar(10),
col4 varchar(10));

INSERT INTO t1 VALUES ('A', 5);
INSERT INTO t1 VALUES ('B', 3);
INSERT INTO t1 VALUES ('C', 1);
INSERT INTO t1 VALUES  ('D', 5);

INSERT INTO t2  VALUES ('A', 'foo');
INSERT INTO t2  VALUES ('A', 'bar');
INSERT INTO t2  VALUES ('C', 'baz');
INSERT INTO t2  VALUES ('E', 'foo');

SELECT COUNT(*) from t1 JOIN t2;

SELECT COUNT(*) from t1 JOIN t2 on col1=col3;

SELECT * FROM t1 JOIN t2 on col1=col3;    -- inner join is commmutative because equality is commutative.

SELECT * FROM t2 JOIN t1 on col1=col3;    -- column order is different, but column order doesn't matter.:

SELECT * FROM t1 FULL OUTER JOIN t2 on t1.col1=t2.col3; 

SELECT count(*) FROM t1 LEFT JOIN t2 on t1.col1=t2.col3; 

SELECT * FROM t1 FULL OUTER JOIN t2 on t1.col1=t2.col3 WHERE col1 IS NULL;   -- this is the right disjoint set
SELECT * FROM t1 FULL OUTER JOIN t2 on t1.col1=t2.col3 WHERE col3 IS NULL;   -- and the left disjoint set

