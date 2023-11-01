from sqlalchemy.orm import Session

from python.repositories.game_repository import GameRepository
from python.repositories.moment_repository import MomentRepository
from python.repositories.user_moment_assoc_repository import UserMomentAssocRepository
from python.repositories.user_repository import UserRepository


class RepositoryProvider:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)
        self.moment_repository = MomentRepository(session)
        self.game_repository = GameRepository(session)
        self.user_moment_assoc_repository = UserMomentAssocRepository(session)
