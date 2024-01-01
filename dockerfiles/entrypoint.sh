#!/bin/bash

su - postgres -c 'pg_ctl start -D /var/lib/postgres/data'
cd /srv/Order/api && uvicorn main:app --reload
cd /srv/Order/order-ui && npm run dev
