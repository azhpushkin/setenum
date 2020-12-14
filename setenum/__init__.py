from enum import Enum

class SetEnum(Enum):
    pass


def includes(cls_to_include):
    def inner(cls):
        return cls
    return inner
