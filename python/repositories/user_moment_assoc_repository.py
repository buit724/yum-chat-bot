from datetime import datetime
from typing import Tuple, List

from sqlalchemy import select, func, and_, Select
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

    def user_moment_counts(self) -> List[Tuple[str, int]]:
        query: Select = (select(User.display_name, func.count(UserMomentAssoc.user_id).label("moment_count"))
                         .join(User).where(and_(User.id == UserMomentAssoc.user_id))
                         .order_by("moment_count")
                         .group_by(UserMomentAssoc.user_id))

        return [(row[0], row[1]) for row in self.session.execute(query)]
