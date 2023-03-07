# Configuração do banco de dados PostgreSQL
Este é um arquivo de configuração do banco de dados PostgreSQL. O arquivo inclui comandos para criar um novo banco de dados e um novo usuário, conceder privilégios e restaurar um backup.
Dockerfile
O Dockerfile deve incluir as seguintes linhas:
```Dockerfile

FROM postgres

ENV POSTGRES_PASSWORD postgres

COPY imoveis.tar /var/lib/postgresql/backup/

RUN set -ex \
 && psql -U postgres -c "CREATE DATABASE imoveis_financiados_db" \
 && psql -U postgres -c "CREATE USER imoveisfinanciados WITH PASSWORD 'postgres'" \
 && psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE imoveis_financiados_db TO imoveisfinanciados" \
 && pg_restore -U postgres -d imoveis_financiados_db /var/lib/postgresql/backup/imoveis.tar
```
### Instruções
Para executar as instruções abaixo, é necessário entrar no prompt do PostgreSQL. Isso pode ser feito com o seguinte comando:
```bash
sudo su - postgres
psql
```
Remover o banco de dados existente
```sql
drop database imoveis_financiados;
```
Criar um novo banco de dados vazio
```sql
create database imoveis_financiados;
```
Criar um novo usuário
```sql
create user imoveisfinanciados with encrypted password 'postgres';
```
Conceder privilégios ao usuário
```sql
alter user imoveisfinanciados with SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE imoveis_financiados_db to imoveisfinanciados;
```
Ver informações de conexão
```sql
\conninfo
```
Listar bancos de dados
```sql
\l
```
Conectar a um banco de dados
```sql
\c imoveis_financiados_db;
```
Fazer backup do banco de dados
```bash
pg_dump -U postgres -h mauriciol-1975.postgres.pythonanywhere-services.com -p 11975 -d imoveis_financiados_db --clean --no-privileges --no-owner --verbose --file teste.tar
```
Copiar backup para dentro do container Docker
```bash
docker cp imoveis.tar imoveis_financiados:/tmp
```
Mudar proprietário do arquivo de backup
```bash
chown root:root imoveis.tar
```
Restaurar o backup
```bash
pg_restore -h localhost -p 5432 -d "imoveis_financiados" -U imoveisfinanciados -v "imoveis.tar" > log_dump.log
```
Criar imagem Docker
```bash
docker commit imoveis_financiados
```
Executar imagem Docker
```bash
docker run -it imoveis_financiados
```