#activate_this = '/home/ubuntu/flaskproject/venv/bin/activate_this.py'
#with open(activate_this) as f:
#	exec(f.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/fastbooks3/")

sys.path.append('/home/ubuntu/fastbooks3/venv/lib/python3.6/site-packages')

from app import app as application
