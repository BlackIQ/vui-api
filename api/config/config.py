from dotenv import load_dotenv
import sys
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
env = os.environ
path = sys.path[0]
