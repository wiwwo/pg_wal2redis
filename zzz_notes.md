$ <wherever>/funwith__pg_recvlogical
$ dkc up -d


$ docker run --name some-redis -p 6379:6379 --rm  -d redis



$ workon pg_wal2redis

$ psql  -h 127.0.0.1 -Umyuser postgres -p5445 -c "SELECT 'init' FROM pg_create_logical_replication_slot('pg_wal2redis', 'wal2json');"


$ pgbench -i  -h 127.0.0.1 -Umyuser postgres -p5445
$ pgbench   -h 127.0.0.1 -Umyuser postgres -p5445 -s10


$ docker exec -it some-redis redis-cli
127.0.0.1:6379> hgetall accounts_balance:1
1) "abalance"
2) "0"

127.0.0.1:6379> hget accounts_balance:1 abalance
"0"



{
    "action": "I",
    "lsn": "0/2457358",
    "schema": "public",
    "table": "pgbench_accounts",
    "columns": [
        {
            "name": "aid",
            "type": "integer",
            "value": 18182
        },
        {
            "name": "bid",
            "type": "integer",
            "value": 1
        },
        {
            "name": "abalance",
            "type": "integer",
            "value": 0
        },
        {
            "name": "filler",
            "type": "character(84)",
            "value": "                                                                                    "
        }
    ]
}



 {'action': 'U'
 , 'lsn': '0/2F7B020'
 , 'schema': 'public'
 , 'table': 'pgbench_accounts'
 , 'columns': [ {'name': 'aid', 'type': 'integer', 'value': 30986},
                {'name': 'bid', 'type': 'integer', 'value': 1},
                {'name': 'abalance', 'type': 'integer', 'value': 2642},
                {'name': 'filler', 'type': 'character(84)', 'value': '                                                                                    '}]
 , 'identity': [{'name': 'aid', 'type': 'integer', 'value': 30986}]}









{
    "change": [
        {
            "kind": "update",
            "schema": "public",
            "table": "table2_with_pk",
            "columnnames": [
                "a",
                "b",
                "c"
            ],
            "columntypes": [
                "integer",
                "character varying(30)",
                "timestamp without time zone"
            ],
            "columnvalues": [
                3,
                "MEH1",
                "2022-11-10 10:46:50.848364"
            ],
            "oldkeys": {
                "keynames": [
                    "a",
                    "c"
                ],
                "keytypes": [
                    "integer",
                    "timestamp without time zone"
                ],
                "keyvalues": [
                    3,
                    "2022-11-10 10:46:50.848364"
                ]
            }
        }
    ]
}




 {
    "action": "U",
    "schema": "public",
    "table": "table2_with_pk",
    "columns": [
        {
            "name": "a",
            "type": "integer",
            "value": 3
        },
        {
            "name": "b",
            "type": "character varying(30)",
            "value": "MEH"
        },
        {
            "name": "c",
            "type": "timestamp without time zone",
            "value": "2022-11-10 10:46:50.848364"
        }
    ],
    "identity": [
        {
            "name": "a",
            "type": "integer",
            "value": 3
        },
        {
            "name": "c",
            "type": "timestamp without time zone",
            "value": "2022-11-10 10:46:50.848364"
        }
    ]
}
