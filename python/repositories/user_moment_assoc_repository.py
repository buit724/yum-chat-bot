from datetime import datetime

from sqlalchemy.orm import Session

from python.models.moment import Moment
from python.models.user import User
from python.models.user_moment_assoc import UserMomentAssoc


class UserMomentAssocRepository:
    def __init__(self, session: Session):
        self.session = session

    def assoc_user_moment(self, user: User, moment: Moment) -> UserMomentAssoc:
        user_moment_assoc: UserMomentAssoc = UserMomentAssoc(user.id, moment.id, datetime.now())
        self.session.add(user_moment_assoc)
        self.session.commit()
        return user_moment_assoc
