import uuid
import messytables

DEBUG = False
TESTING = False
SECRET_KEY = str(uuid.uuid4())
USERNAME = str(uuid.uuid4())
PASSWORD = str(uuid.uuid4())

NAME = 'datapusher'

# database

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/job_store.db'

# webserver host and port

HOST = '0.0.0.0'
PORT = 8800
HOST = '127.0.0.1'
# logging

#FROM_EMAIL = 'server-error@example.com'
#ADMINS = ['yourname@example.com']  # where to send emails

#LOG_FILE = '/tmp/ckan_service.log'
STDERR = True


TYPES = [messytables.StringType, messytables.DecimalType,
         messytables.IntegerType]
