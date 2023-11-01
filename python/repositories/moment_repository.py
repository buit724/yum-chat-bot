from sqlalchemy.orm import Session

from python.models.moment import Moment


class MomentRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_moment(self, moment: Moment) -> Moment:
        self.session.add(moment)
        self.session.commit()
        return moment

    def update_moment(self, moment: Moment) -> None:
        self.session.merge(moment)
        self.session.commit()

    def delete_moment(self, moment: Moment) -> None:
        self.session.delete(moment)
        self.session.commit()
