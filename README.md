# Votação

## Aplicação com containers

Para subir a aplicação em um container:

1. Instale os pacotes do docker:

   ```shell
   apt install docker.io docker-compose-v2 docker-buildx
   ```

2. Configure as variáveis de ambiente de acordo com o
   [docker compose](./docker-compose.yml);
3. Suba o cluster (isto também irá fazer o build da imagem):

   ```shell
   docker compose up
   ```

4. Para fazer o build da imagem sem utilizar o compose:

   ```shell
   docker build -t votacao:latest .
   ```

5. Para desfazer o cluster:

   ```shell
   # o -v é para apagar os volumes
   docker compose down -v
   ```

> [!WARNING]  
> As migrations não são realizadas no script de entrypoint.

As migrations podem ser executadas manualmente sob demanda dentro do container:

```shell
# Acesse o container:
docker container exec -it votacao-votacao-1 bash
# Rode as migrations dentro do container:
python3 manage.py makemigrations --settings=config.settings.production
python3 manage.py makemigrations autentica votacao --settings=config.settings.production
python3 manage.py migrate --settings=config.settings.production
```
