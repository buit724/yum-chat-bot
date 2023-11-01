from typing import List, Type

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from python.models.game import Game
from python.models.moment import Moment
from python.models.user import User
from python.models.user_moment_assoc import UserMomentAssoc

if __name__ == "__main__":
    engine: Engine = create_engine("sqlite:///C:\\Users\\thoai\\databases\\yumbot.db", echo=True)

    # Create session
    session: Session = sessionmaker(bind=engine)()
    games: List[Type[Game]] = session.query(Game).all()
    print(games)

    users: List[Type[User]] = session.query(User).all()
    print(users)

    moments: List[Type[Moment]] = session.query(Moment).all()
    print(moments)

    user_moment_assocs: List[Type[UserMomentAssoc]] = session.query(UserMomentAssoc).all()
    print(user_moment_assocs)
