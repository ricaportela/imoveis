# Configuração do banco de dados PostgreSQL
Este é um arquivo de configuração do banco de dados PostgreSQL. O arquivo inclui comandos para criar um novo banco de dados e um novo usuário, conceder privilégios e restaurar um backup.
Dockerfile
O Dockerfile deve incluir as seguintes linhas:
```Dockerfile
Dockerfile
Copy code
FROM postgres

ENV POSTGRES_PASSWORD postgres

COPY imoveis.tar /var/lib/postgresql/backup/

RUN set -ex \
 && psql -U postgres -c "CREATE DATABASE imoveis_financiados_db" \
 && psql -U postgres -c "CREATE USER imoveisfinanciados WITH PASSWORD 'postgres'" \
 && psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE imoveis_financiados_db TO imoveisfinanciados" \
 && pg_restore -U postgres -d imoveis_financiados_db /var/lib/postgresql/backup/imoveis.tar
```
Instruções
Para executar as instruções abaixo, é necessário entrar no prompt do PostgreSQL. Isso pode ser feito com o seguinte comando:
```bash
bash
Copy code
sudo su - postgres
psql
```
Remover o banco de dados existente
```sql
sql
Copy code
drop database imoveis_financiados_db;
```
Criar um novo banco de dados vazio
```sql
sql
Copy code
create database imoveis_financiados_db;
```
Criar um novo usuário
```sql
sql
Copy code
create user imoveisfinanciados with encrypted password 'postgres';
```
Conceder privilégios ao usuário
```sql
sql
Copy code
alter user imoveisfinanciados with SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE imoveis_financiados_db to imoveisfinanciados;
```
Ver informações de conexão
```sql
sql
Copy code
\conninfo
```
Listar bancos de dados
```sql
sql
Copy code
\l
```
Conectar a um banco de dados
```sql
sql
Copy code
\c imoveis_financiados_db;
```
Fazer backup do banco de dados
```bash
bash
Copy code
pg_dump -U postgres -h mauriciol-1975.postgres.pythonanywhere-services.com -p 11975 -d imoveis_financiados_db --clean --no-privileges --no-owner --verbose --file teste.tar
```
Copiar backup para dentro do container Docker
```bash
bash
Copy code
docker cp imoveis.tar imoveis_financiados:/tmp
```
Mudar proprietário do arquivo de backup
```bash
bash
Copy code
chown root:root imoveis.tar
```
Restaurar o backup
```bash
bash
Copy code
pg_restore -h localhost -p 5432 -d "imoveis_financiados" -U imoveisfinanciados -v "imoveis.tar" > log_dump.log
```
Criar imagem Docker
```bash
bash
Copy code
docker commit imoveis_financiados imoveis_docker
```
Executar imagem Docker
```bash
bash
Copy code
docker run -it imoveis_docker
```

---

**User:**
e como eu faço para copiar mantendo a formatação 

Please write in Portuguese language.

---

**ChatGPT:**
Para copiar e manter a formatação do texto em LaTeX, você pode seguir as seguintes etapas:
<li>Selecione o texto que deseja copiar;</li><li>Clique com o botão direito do mouse e escolha a opção "Copiar" ou use o atalho "Ctrl+C" no Windows ou "Command+C" no Mac;</li><li>Abra um editor de texto em LaTeX, como o TeXstudio ou o Overleaf;</li><li>Cole o texto copiado no editor usando a opção "Colar" ou o atalho "Ctrl+V" no Windows ou "Command+V" no Mac.</li>
O texto copiado deve manter a formatação original em LaTeX, incluindo os comandos de formatação e as fórmulas matemáticas, se houver. Se você tiver problemas com a formatação, verifique se o seu editor de texto está configurado corretamente para compilar o código LaTeX.