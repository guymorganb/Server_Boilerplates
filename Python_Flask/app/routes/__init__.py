# init.py is like index.js, we are importing all our routes here
# the init.py has power, just like index.js

from .home import bp as home
from .dashboard import bp as dashboard
from .api import bp as api  # register the blueprint from the api.py directory so the endpoint is established.
