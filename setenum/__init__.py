from enum import Enum, EnumMeta


# classmethod trick is used to remove a need in SetEnum class (only metaclass is needed)
@classmethod
def _missing_(cls, value):
    # _missing_ is used for looking up the values during __call__
    # this is a small check that makes this lookup work across super/sub sets
    if isinstance(value, cls):
        return value

    return super()._missing_(value)


def _copy_members_from_subset_to_superset(subset_cls, superset_cls):

    for name, obj in subset_cls._member_map_.items():
        setattr(superset_cls, name, obj)
        superset_cls._member_map_[name] = obj
        superset_cls._member_names_.append(name)
        superset_cls._value2member_map_[obj.value] = obj


class SetEnumMeta(EnumMeta):

    def __new__(metacls, cls, bases, classdict):
        classdict.setdefault('__subsets__', [])
        classdict.setdefault('__supersets__', [])

        classdict['_missing_'] = _missing_
        new_cls = super().__new__(metacls, cls, bases, classdict)

        for subset in classdict.get('__subsets__'):
            subset.__supersets__.append(new_cls)
            _copy_members_from_subset_to_superset(subset, new_cls)
        
        for superset in classdict.get('__supersets__'):
            superset.__subsets__.append(new_cls)
            _copy_members_from_subset_to_superset(new_cls, superset)
        
        return new_cls

    def __repr__(cls):
        return "<SetEnum %r>" % cls.__name__

    def __instancecheck__(self, instance):
        if instance == self:
            return True
        
        for cls in self.__subsets__:
            if isinstance(instance, cls):
                return True
        
        return False


class SetEnum(Enum, metaclass=SetEnumMeta):
    pass
