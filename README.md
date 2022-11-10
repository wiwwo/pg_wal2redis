# pg_wal2redis

---
Send Postgresql database changes to a redis instance, and keep it updated.
<br>
<br>Far from being "production ready", but not *that* far.
It just works.
<br><br>
Constraint: table must have a PK, and on a single field; composite PKs are (still) not supported


---
## Small HOWTO

Change config files.

### Terminal 1:

```
$ python3 pg_wal2redis.py
```

### Terminal 2:

```
$ pgbench -i -h 127.0.0.1 -Umyuser postgres -p5445
$ pgbench    -h 127.0.0.1 -Umyuser postgres -p5445 -s10
```
and/or
```
$ psql -h 127.0.0.1 -Umyuser postgres -p5445
=# UPDATE pgbench_accounts set abalance = 777 where aid=1;
```

### Terminal 3:

```
$ docker run --name some-redis -p 6379:6379 --rm  -d redis

$ docker exec -it some-redis redis-cli
127.0.0.1:6379> hgetall accounts_balance:1
```





---
## Requisites

* A running Postgresql, with logical replication enabled and wal2json plugin enabled
* A logical replication slot, as in `select pg_create_logical_replication_slot('pg_wal2redis', 'wal2json');`
* python 3.10
* psycopg2-binary==2.9.1
