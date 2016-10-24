import string;
import random;
import unittest;
import unittest.mock;

from core import *;

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

class CoreTest(unittest.TestCase):
  def test_nose(self):
    self.assertEqual(True, True);

  def test_cache(self):
    import os;
    r = id_generator() + '/';
    e = os.path.expanduser(CACHE_DIR);

    c = cache();
    self.assertEqual(c, e);

    c = cache(r);
    self.assertEqual(c, e+r);
    self.assertTrue(os.path.exists(c));
    os.rmdir(c);
