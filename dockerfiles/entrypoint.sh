#!/bin/bash

su - postgres -c 'pg_ctl start -D /var/lib/postgres/data'
cd /srv/Order/api && python server.py
cd /srv/Order/order-ui && uvicorn main:app --reload
