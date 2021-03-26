from abc import ABC, abstractmethod

class Object(ABC):
    def __init__(self, id, pos):
        self.__id = id
        self.__x, self.__y = pos
        super(Object, self).__init__()

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_pos(self):
        pos = (self.__x, self.__y)
        return pos

    def set_pos(self, pos):
        self.__x, self.__y = pos

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass
