#!/bin/bash

su - postgres -c 'pg_ctl start -D /var/lib/postgres/data' && \
cd /srv/Order/api && uvicorn server:app --reload & \
cd /srv/Order/order-ui && npm run dev
