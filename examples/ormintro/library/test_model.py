'''test_model.py shows how to write a standalone script to test various django subroutines.
'''

'''Over here is some boiler plat django to make sure the script executes properly. Don't worry
about it too much. Pretty much pattern match when you need to do this.;
'''
import sys, os, logging
sys.path.append('../ormintro')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ormintro.settings'

import django
django.setup()

#sets up logging, all logs go to the console
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)


'''Now we will import our code
'''
from library.models import *


addBook('9781497438095','Romeo and Juliet','William Shakespeare', 1597)
addBook('9780446310789','To Kill a Mockingbird','Harper Lee', 1962)

addInventory('9781497438095',5)
addInventory('9780446310789',3)

checkout('9780446310789')
checkout('9780446310789')
checkout('9781497438095')