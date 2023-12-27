from psycopg_pool import ConnectionPool
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "../config/postgres.yml"

ARGS = yaml.load(open(CONFIG_PATH, 'r'))

CONNINFO = f'host={ARGS['host']};'
           + f'port={ARGS['port']};'
           + f'dbname={ARGS['database']};'
           + f'user{ARGS['user']};'
           + f'password={ARGS['password']}'

CONNPOOL = ConnectionPool(CONNINFO)

def exec_file(path):
    with CONNPOOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(open(path, 'r').read())
            conn.commit()

def exec_get_one(query, args={}):
    with CONNPOOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, args)
            return cur.fetchone()
        
def exec_get_all(query, args={}):
    with CONNPOOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, args={})
            return cur.fetchall()

def exec_commit(query, args={}):
    with CONNPOOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, args)
            conn.commit()

def exec_commit_return(query, args={}):
    with CONNPOOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, args)
            conn.commit()
            return cur.fetchone()
    
    
