FROM archlinux:base-devel

RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm git python python-psycopg python-psycopg-pool python-yaml python-fastapi postgresql

RUN systemctl enable postgresql.service && \
    mkdir /var/run/postgresql && \
    chown -R postgres:postgres /var/run/postgresql

RUN su - postgres -c 'initdb --locale=C.UTF-8 --encoding=UTF8 -D /var/lib/postgres/data --data-checksums && \
    pg_ctl start -D /var/lib/postgres/data' && \
    psql -U postgres -c "CREATE USER order_chat WITH PASSWORD 'SuperSecret';" -c "CREATE DATABASE order_chat OWNER order_chat;" && \
    su - postgres -c 'pg_ctl stop -D /var/lib/postgres/data'

RUN cd /srv && \
    git clone https://github.com/TheMargarineMan/Order

ENTRYPOINT [/srv/Order/dockerfiles/entrypoint.sh]
