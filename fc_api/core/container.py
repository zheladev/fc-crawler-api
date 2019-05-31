import dependency_injector.containers as containers
import dependency_injector.providers as providers

from fc_api.core.core import Database
from fc_api.repositories.post import PostRepository
from fc_api.repositories.thread import ThreadRepository
from fc_api.repositories.user import UserRepository


class Repositories(containers.DeclarativeContainer):
    """
    Repository providers
    """

    # base = providers.Factory(
    #     BaseRepository,
    #     session=Database.session,
    #     foo=bar
    # )
    user = providers.Factory(
        UserRepository,
        session=Database.session,
    )

    thread = providers.Factory(
        ThreadRepository,
        session=Database.session,
    )

    post = providers.Factory(
        PostRepository,
        session=Database.session,
    )
