import getpass
from abc import *

class UserInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_menu(self):
        pass