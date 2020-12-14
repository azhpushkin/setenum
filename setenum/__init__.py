from enum import Enum, EnumMeta


class SetEnumMeta(EnumMeta):
    def __contains__(cls, member):
        if not isinstance(member, Enum):
            raise TypeError(
                "unsupported operand type(s) for 'in': '%s' and '%s'" % (
                    type(member).__qualname__, cls.__class__.__qualname__))
        # TODO: class check is required
        return member._name_ in cls._member_map_

class SetEnum(Enum, metaclass=SetEnumMeta):
    pass


def includes(cls_to_include):
    def inner(cls):
        for name, obj in cls_to_include._member_map_.items():
            cls._member_map_[name] = obj
            cls._member_names_.append(name)
        return cls
    return inner
