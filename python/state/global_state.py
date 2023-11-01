"""
Class keeping global states of the applications that can be shared between commands
"""
from typing import Union, List

from python.models.moment import Moment
from python.models.user import User


class GlobalState:
    def __init__(self):
        # Moment related flags
        self.current_moment: Union[Moment | None] = None
        self.claimed_users: List[User] = []

    def add_claimed_user(self, user: User) -> bool:
        """
        Add user to list of claimed user. If the user has already been added, this will return false.
        Before calling this method, should check if there is a moment currently going on.
        :return:  Whether the user was added
        """
        # User already claimed the moment
        if user.id in [x.id for x in self.claimed_users]:
            return False

        self.claimed_users.append(user)
        return True

    def start_moment(self, moment: Moment) -> None:
        """
        Start a moment
        :param moment:  The moment
        :return: None
        """
        self.current_moment = moment
        self.claimed_users = []

    def end_moment(self) -> None:
        """
        End the moment by setting all the moment flags back to their original states
        :return: None
        """
        self.current_moment = None
        self.claimed_users = []
