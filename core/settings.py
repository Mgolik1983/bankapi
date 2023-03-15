from passlib.context import CryptContext


PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = '9-8UN9nu(*uoihUGYh8oujnp88yU9n8o889PIun8gm799pij,p'
EXPIRE_JWT_TOKEN = 10
TOKEN_TYPE = 'Bearer'
ALGORITHM = 'HS256'