
#!/usr/bin/env python2
import sys

sys.path.insert(0, '/var/www/html/Item_Catalog/')


from Item_Catalog.app import app as application
from Item_Catalog import *

application.secret_key = 'super_secret_key'
