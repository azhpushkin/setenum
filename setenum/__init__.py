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
    
    # TODO: https://docs.python.org/3/reference/datamodel.html#customizing-instance-and-subclass-checks
    # This is a somewhat ugly trick to make repr and print show on which 
    
    def __get__(self, obj, objtype=None):
        self.__called_from = objtype
        return self

    def __repr__(self):
        return "<%s.%s: %r>" % (
                self.__called_from.__name__, self._name_, self._value_)

    def __str__(self):
        return "%s.%s" % (self.__called_from.__name__, self._name_)

    



def includes(cls_to_include):
    def inner(cls):
        for name, obj in cls_to_include._member_map_.items():
            setattr(cls, name, obj)
            cls._member_map_[name] = obj
            cls._member_names_.append(name)
        return cls
    return inner
