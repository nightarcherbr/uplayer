'''
Retorna o proximo ID
'''
def increment():
  global _CURRENT_TIMESTAMP;
  global _CURRENT_INCREMENT;
  import time;
  if not '_CURRENT_TIMESTAMP' in globals() :
    _CURRENT_TIMESTAMP = time.time();
  if not '_CURRENT_INCREMENT' in globals() :
    _CURRENT_INCREMENT = 1;
  else:
    _CURRENT_INCREMENT += 1;
  return str(_CURRENT_TIMESTAMP).replace('.', '')+'.'+str(_CURRENT_INCREMENT);


def register():
  pass