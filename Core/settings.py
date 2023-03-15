from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = 'bnn-oi;nbopaop(mvmvmvmd123zxcvnbfnfgb,4'
EXPIRE_JWT_TOKEN = 10
TOKEN_TYPE = 'Bearer'