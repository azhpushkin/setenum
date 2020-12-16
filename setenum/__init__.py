from enum import Enum, EnumMeta


# classmethod trick is used to remove a need in SetEnum class (only metaclass is needed)
@classmethod
def _missing_(cls, value):
    # _missing_ is used for looking up the values during __call__
    # this is a small check that makes this lookup work across super/sub sets
    if isinstance(value, cls):
        return value

    return super()._missing_(value)


class SetEnumMeta(EnumMeta):

    def __new__(metacls, cls, bases, classdict):
        classdict['_missing_'] = _missing_
        return super().__new__(metacls, cls, bases, classdict)
    
    def __init__(self, name, bases, dict):
        self._subsets_ = []
        self._supersets_ = []

    def __repr__(cls):
        return "<SetEnum %r>" % cls.__name__

    def __instancecheck__(self, instance):
        if instance == self:
            return True
        
        for cls in self._subsets_:
            if isinstance(instance, cls):
                return True
        
        return False


class SetEnum(Enum, metaclass=SetEnumMeta):
    pass

    
def _copy_members_from_subset_to_superset(subset_cls, superset_cls):
    subset_cls._supersets_.append(superset_cls)
    superset_cls._subsets_.append(subset_cls)

    for name, obj in subset_cls._member_map_.items():
        setattr(superset_cls, name, obj)
        superset_cls._member_map_[name] = obj
        superset_cls._member_names_.append(name)
        superset_cls._value2member_map_[obj.value] = obj


def as_superset_of(subset_cls):
    def inner(superset_cls):
        _copy_members_from_subset_to_superset(subset_cls, superset_cls)
        return superset_cls
    return inner


def as_subset_of(superset_cls):
    def inner(subset_cls):
        _copy_members_from_subset_to_superset(subset_cls, superset_cls)
        return subset_cls
    return inner