class BaseConfig:
    USER_DB='postgres'
    PASS_DB="Admin123"
    URL_DB='localhost'
    NAME_BD='nivelacion'
    FULL_URL_DB=f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_BD}'
    SQLALCHEMY_DATABASE_URI=FULL_URL_DB
    SECRET_KEY="llave_secreta"
    DEBUG = False
    BCRYPT_LOG_ROUNDS=13
    SQLALCHEMY_TRACK_ODIFICATIONS=False
    print(SQLALCHEMY_DATABASE_URI)