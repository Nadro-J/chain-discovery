#!/bin/bash
# Enviroment: Ubuntu 18.04

usr='blockstat'
db='chain-discovery'

cowsay "Chain-Discovery PostgreSQL setup"
read -p "Enter PostgreSQL server password: " -s passwd; printf "\n"

postgre_handler(){
  case $1 in
    *"already exists"*)
      echo "    - Already exists! - case test"
    ;;
    *"CREATE DATABASE"*)
      echo "    - successfully created!"
    ;;
    *"CREATE TABLE"*)
      echo "    - successfully created!"
    ;;
    *"authentication failed"*)
      echo "    - [AUTHENTICATION FAILED]"
    ;;
  esac
}

## Create DB to store all tables in
echo "+ Creating database: $db"
create_db="$(psql "postgresql://$usr:$passwd@localhost/postgres" -c "CREATE DATABASE $db" 2>&1)"
postgre_handler "$create_db"

getblockstats="$(psql "postgresql://$usr:$passwd@localhost/$db" -c " CREATE TABLE public.getblockstats
  (
     avgfee              BIGINT NOT NULL,
     avgfeerate          BIGINT NOT NULL,
     avgtxsize           BIGINT NOT NULL,
     blockhash           VARCHAR(250) UNIQUE,
     feerate_percentiles VARCHAR(200),
     height              BIGINT NOT NULL UNIQUE,
     ins                 BIGINT NOT NULL,
     maxfee              BIGINT NOT NULL,
     maxfeerate          BIGINT NOT NULL,
     maxtxsize           BIGINT NOT NULL,
     medianfee           BIGINT NOT NULL,
     mediantime          BIGINT NOT NULL,
     mediantxsize        BIGINT NOT NULL,
     minfee              BIGINT NOT NULL,
     minfeerate          BIGINT NOT NULL,
     mintxsize           BIGINT NOT NULL,
     outs                BIGINT NOT NULL,
     subsidy             BIGINT NOT NULL,
     swtotal_size        BIGINT NOT NULL,
     swtotal_weight      BIGINT NOT NULL,
     swtxs               BIGINT NOT NULL,
     'time'              BIGINT NOT NULL,
     total_out           BIGINT NOT NULL,
     total_size          BIGINT NOT NULL,
     total_weight        BIGINT NOT NULL,
     totalfee            BIGINT NOT NULL,
     txs                 BIGINT NOT NULL,
     utxo_increase       BIGINT NOT NULL,
     utxo_size_inc       BIGINT NOT NULL
  )" 2>&1)"

## Create the relevant sql tables required to scrape data from BitGreen's blockchain
echo "+ Creating table(s): '$getblockstats"
postgre_handler "$getblockstats"

