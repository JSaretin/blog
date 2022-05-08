from deta import Deta 
from os import environ

deta = Deta(environ['DETA_API_KEY'])

def get_connection(db_name: str):
    return deta.Base(f'blog_{db_name}')