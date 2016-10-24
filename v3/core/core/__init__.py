import sys
import os
import os.path

from core.settings import *;



'''
Normaliza o caminho de um diretorio, criando a pasta se necessario
'''
def normalize_path(directory=HOME_DIR):
  assert( directory is not None );
  import re;

  # Remove os backslashes duplicados
  while( "//" in directory ):
    directory = re.sub(r'//', '/', directory);

  directory = os.path.expanduser(directory);
  directory = os.path.expandvars(directory);

  # Verifica se o arquivo possui um trailing slash
  orig = directory;
  if( not directory.endswith('/') ):
    directory = os.path.dirname(directory);

  # Cria os diretorios se preciso
  if ( not os.path.exists(directory) ):
    os.makedirs(directory, exist_ok=False);
  return orig;


'''
Retorna um caminho relativo no cache da maquina
'''
def cache(directory=CACHE_DIR):
  if( directory != CACHE_DIR ):
    directory = CACHE_DIR + '/' + directory;
  return normalize_path( directory );

'''
Retorna a identificacao principal da maquina
'''
def player_id():
  import uuid;
  return '-'.join('%02X' % ((uuid.getnode() >> 8*i) & 0xff) for i in reversed(range(6)))