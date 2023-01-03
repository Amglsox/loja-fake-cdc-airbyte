class Config:
    def __init__(self) -> None:
        self.user = "postgres"
        self.password = None
        self.host = None
        self.port = "5432"
        self.database = "loja_fake"

    def _to_dict(self) -> dict:
        obj = {
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port,
            "database": self.database,
        }
        return obj
