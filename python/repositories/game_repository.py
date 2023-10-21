from typing import Union

from sqlalchemy.orm import Session

from python.models.game import Game


class GameRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_game(self, id: int, name: str) -> Game:
        # Get user if this user already tracked by our app
        db_game: Union[Game, None] = self.session.query(Game).filter_by(id=id).first()

        # This user is already tracked, update
        if db_game is not None:
            # Check if we need to update display name
            if db_game.name is not name:
                db_game.name = name
                self.session.commit()
            return db_game

        # This user is not track, add to database
        new_game = Game(id, name)
        self.session.add(new_game)
        self.session.commit()
        return new_game
