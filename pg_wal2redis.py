#!/usr/bin/env python3

import sys
import redis
import configparser
import json

import psycopg2
from psycopg2.extras import LogicalReplicationConnection, StopReplication


def get_repl_cursor(postgres_config, cache_config):
  try:
    lconnection  = psycopg2.connect (
                    "host=%s user=%s password=%s dbname=%s port=%s" % \
                        (  postgres_config['host']
                          ,postgres_config['user']
                          ,postgres_config['password']
                          ,postgres_config['dbname']
                          ,postgres_config['port']
                        ),
                     connection_factory = LogicalReplicationConnection)
  except psycopg2.OperationalError as e:
    print(f"Unable to connect to postgresql!\n{format(e)}")
    exit(30)

  lcursor = lconnection.cursor()

  lcursor.start_replication (
    slot_name = postgres_config['slot_name']
    ,options = {  'pretty-print':0
                  ,'write-in-chunks':0
                  ,'include-lsn':0
                  ,'format-version':2
                  ,'include-transaction':0
                  ,'add-tables': cache_config['watch_schema']+'.'+cache_config['watch_table']
                  ,'actions': 'insert, update, delete'
              }
    ,decode=True
  )

  print(f"Connected to postgresql {postgres_config['host']} db {postgres_config['dbname']}")
  return lcursor



def connect_redis(redis_config):
  try:
    this_redis = redis.Redis(
      host = redis_config['host'],
      port = redis_config['port']
    )

  except redis.exceptions.ConnectionError as e:
    print(f"Unable to connect to redis!\n{format(e)}")
    exit(40)

  print(f"Connected to redis     {redis_config['host']}")
  return this_redis



def getData (key, values):
  return list(filter(lambda x: x['name']==key,  values))[0]['value']



def send_wal(wal_msg, redis_obj, cache_config):
  if wal_msg:

    ljson = json.loads(wal_msg.payload)
    #print(ljson)

    # Get the value of table's PK of table, which will be the ID in the hash namespace (eg. aid=123)
    # TODO: composite PKs
    lwatched_pk_val = getData(cache_config['watch_pk'], ljson['columns'])

    if ljson['action'] in {'I','U'}:

      # This is the value of the watched column (eg. abalance=123,4)
      lwatch_column_value = getData(cache_config['watch_column'], ljson['columns'])

      redis_obj.hset (  cache_config['hset_name']+':'+str(lwatched_pk_val)
                       ,cache_config['hset_field']
                       ,lwatch_column_value
                     )


    if ljson['action'] == 'D':
      # Just remove the key
      redis_obj.hdel (  cache_config['hset_name']+':'+str(lwatched_pk_val)
                       ,cache_config['hset_field']
                     )

    wal_msg.cursor.send_feedback(flush_lsn=wal_msg.data_start)






def main():
  config_filename = 'pg_wal2redis.conf'
  config = configparser.ConfigParser()
  if not config.read(config_filename):
    print("Unable to read config file %s" % config_filename)
    exit(20)

  lredis = connect_redis(config['redis'])
  repl_cursor = get_repl_cursor(config['postgresql'], config['cache'])


  while True:
    repl_slot_message = repl_cursor.read_message()
    send_wal(repl_slot_message, lredis, config['cache'])





if __name__=="__main__":
  main()
else:
  exit (10)
