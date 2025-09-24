import oracledb

def get_oracle_connection():
    # Puedes usar variables de entorno o archivo .env para mayor seguridad
    user = "PYDATA"
    password = "PYDATA"
    dsn = oracledb.makedsn("oraprod9.tda", 1521, service_name="COMUN")

    connection = oracledb.connect(user=user, password=password, dsn=dsn)
    return connection
