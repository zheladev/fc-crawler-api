# from datetime import date
# from typing import List
# from uuid import UUID
#
# from sqlalchemy import func
from fc_api.models.post import Post
from fc_api.repositories.base import BaseRepository


class PostRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session=session, model=Post)

