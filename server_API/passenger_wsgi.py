# or whatever file has `app = Flask(__name__)`
from main import app as application
import sys
import os

# Make sure your app folder is in the import path
sys.path.insert(0, os.path.dirname(__file__))

# Activate virtual environment (adjust path to match yours)
activate_this = os.path.expanduser(
    "source /home/mfkgunhs/virtualenv/repositories/FullstackMMA_DataHub/server_API/3.10/bin/activate && cd /home/mfkgunhs/repositories/FullstackMMA_DataHub/server_API")
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Import your Flask app (adjust import path to your actual app)
