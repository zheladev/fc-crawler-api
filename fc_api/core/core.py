import transaction

from sqlalchemy import engine_from_config

from dependency_injector import containers, providers
from fc_api.models import get_tm_session, get_session_factory


class Core(containers.DeclarativeContainer):
    # Retrieves the settings of the application (*.ini).
    settings = providers.Configuration('config')


class Database(containers.DeclarativeContainer):
    """IoC container of database related providers."""

    # Retrieves a database session
    session = providers.ThreadLocalSingleton(
        get_tm_session,
        providers.Singleton(
            get_session_factory,
            providers.Factory(
                engine_from_config,
                Core.settings,
                prefix='sqlalchemy_'
            )
        ),
        transaction
    )


def includeme(config):
    """
    Injects the application config into the Core.settings container.
    :param config:
    :return:
    """
    settings = config.get_settings()
    setup_di(settings)


def setup_di(settings: dict):
    settings_ = dict()
    for key, value in settings.items():
        dotless_key = key.replace('.', '_')
        settings_[dotless_key] = value
    Core.settings.update(settings_)
