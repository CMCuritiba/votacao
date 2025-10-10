# Use a base Python image
FROM python:3.5-stretch

COPY ./devops/sources.list /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    nginx \
    memcached \
    libfreetype6-dev \
    libncurses5-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libffi-dev \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    libjpeg62-turbo-dev \
    libreoffice-core \
    libreoffice-writer \
    enchant \
    && rm -rf /var/lib/apt/lists/*

ENV NODE_VERSION=8.17.0
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | /bin/bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" \
    && nvm install $NODE_VERSION \
    && nvm use $NODE_VERSION

ENV PATH="/root/.nvm/versions/node/v$NODE_VERSION/bin/:${PATH}"

RUN npm install -g bower

# Set the working directory inside the container
WORKDIR /app

COPY ./ ./

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

# Copia configuração do nginx
COPY --chmod=644 ./deploy/production/nginx.conf /etc/nginx/sites-available/default

# # Habilita serviços nginx
# RUN systemctl enable nginx \
#     && systemctl restart nginx

# Activate the virtual environment
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --no-cache-dir -r /app/requirements/production.txt

# Placeholders para variáveis de ambiente
ENV MSCMC_SERVER=""
ENV LDAP_AUTH_URL=""
ENV DATABASE_URL=""
ENV SECRET_KEY="changeme"
ENV SECRET_KEY_PROD="changeme"

# USER www-data

# Instala pacotes bower, coleta arquivos estáticos e adiciona tarefas do cron
# Evita erros ao rodar o manage.py sem as variáveis de ambiente
RUN python3 manage.py bower_install --settings=config.settings.production --allow-root \
    # && mkdir -p /app/components/bower_components \
    && python3 manage.py collectstatic --noinput --settings=config.settings.production \
    && python3 manage.py crontab add --settings=config.settings.production
    # && mkdir -p /app/var/run

COPY --chmod=755 ./deploy/production/run.sh ./

RUN chown -R www-data:www-data ./

EXPOSE 80

ENTRYPOINT [ "/app/run.sh" ]

# # CMD ["python3", "manage.py", "runserver", "0.0.0.0:80", "--settings=config.settings.production"]

# CMD ["nginx", "-g", "daemon off;"]
