ENABLE_PROXY_FIX = True
SECRET_KEY = "MyVerySecretKey"
PREVENT_UNSAFE_DB_CONNECTIONS = False
TALISMAN_ENABLED = False
SQLALCHEMY_DATABASE_URI = (
    "postgresql+psycopg2://superset:secretsecret@superset-postgres:5432/superset"
)
