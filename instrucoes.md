
# FROM postgres

# ENV POSTGRES_PASSWORD postgres

# COPY imoveis.tar /var/lib/postgresql/backup/

# RUN set -ex \
# && psql -U postgres -c "CREATE DATABASE imoveis_financiados_db" \
# && psql -U postgres -c "CREATE USER imoveisfinanciados" WITH PASSOWRD "postgres" \
# && psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE imoveisfinanciados TO imoveisfinanciados" \
# && pg_restore -U postgres -d imoveisfinanciados /var/lib/postgresql/backup/imoveis.tar


# INSTRUCTIONS

sudo su - postgres                               
psql
psql (12.12 (Ubuntu 12.12-1.pgdg22.04+1))
Type "help" for help.

# remover o banco caso exista
postgres=# drop database imoveis_financiados_db ;
DROP DATABASE
postgres=# 

# Criar o banco vazio
postgres=# create database imoveis_financiados_db;

# criar o usuario imoveisfinanciados
postgres=# create user imoveisfinanciados with encrypted password 'postgres';


# permissões para o usuario imoveisfinaAnciados 
alter user imoveisfinanciados with SUPERUSER;

# permissoes para o banco para o usuario imoveisfinanciados
GRANT ALL PRIVILEGES ON DATABASE imoveis_financiados_db to imoveisfinanciados;

# senha do usuario é postgres 
create user imoveisfinanciados with encrypted password 'postgres';


# COMANDO UTEIS NO PROPT DO PSQL
\conninfo


\l - lista databases
                                       List of databases
        Name         |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges   
---------------------+----------+----------+-------------+-------------+-----------------------
 imoveis_financiados_db | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
 postgres            | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |  
 template0           | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
                     |          |          |             |             | postgres=CTc/postgres
 template1           | postgres | UTF8     | en_US.UTF-8 | en_US.UT:

postgres=# \c imoveis_financiados_db;
You are now connected to database "imoveis_financiados_db" as user "postgres".
imoveis_financiados_db=# 

pg_dump -U postgres -h mauriciol-1975.postgres.pythonanywhere-services.com -p 11975 -d imoveis_financiados_db --clean --no-privileges --no-owner --verbose --file teste.tar 

docker cp imoveis.tar imoveis_financiados:/tmp

dentro do container precisa executar o comando abaxio
chown root:root imoveis.tar

pg_restore -h localhost -p 5432 -d "imoveis_financiados" -U imoveisfinanciados -v "imoveis.tar" > log_dump.log

docker commit imoveis_financiados imoveis_docker

docker run -it imoveis_docker

