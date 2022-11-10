import sqlite3
from dependency_injector import containers, providers
from . import services
# from logger import MyLogger


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[".auth", ".utils.error_handler"])
    config = providers.Configuration(ini_files=['config.ini'])
    # logging = providers.Singleton(
    #     logging.config.fileConfig, fname="logging.ini")

    # logger = providers.Singleton(MyLogger, log_file="app.log")

    # Database
    database_client = providers.Singleton(sqlite3.connect, config.database.dsn)

    # Services
    user_service = providers.Factory(
        services.UserService, db=database_client)
    auth_service = providers.Factory(
        services.AuthService, db=database_client, token_ttl=config.auth.token_ttl.as_int())
