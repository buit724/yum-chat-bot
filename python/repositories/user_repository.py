from typing import Union

from sqlalchemy.orm import Session

from python.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def find_user(self, id: int, display_name) -> User:
        # Get user if this user already tracked by our app
        db_user: Union[User, None] = self.session.query(User).filter_by(id=id).first()

        # This user is already tracked, update
        if db_user is not None:
            # Check if we need to update display name
            if db_user.display_name is not display_name:
                db_user.display_name = display_name
                self.session.commit()
            return db_user

        # This user is not track, add to database
        new_user = User(id, display_name)
        self.session.add(new_user)
        self.session.commit()
        return new_user
