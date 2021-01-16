from enum import Enum, EnumMeta
from typing import Any, Iterable, List


# classmethod trick is used to remove a need in SetEnum class (only metaclass is needed)
def _missing_(cls, value):
    # _missing_ is used for looking up the values during __call__
    # this is a small check that makes this lookup work across super/sub sets
    if isinstance(value, cls):
        return value

    return super()._missing_(value)


def _find_cycle(root_cls, visited=None) -> bool:
    if not visited:
        visited = set()
    
    if root_cls in visited:
        return True

    visited.add(root_cls)
    is_cycle_detected = any(_find_cycle(subset, visited) for subset in root_cls.__subsets__)
    visited.remove(root_cls)
    return is_cycle_detected


def _is_enums_hierarchy_valid(cls) -> bool:
    if _find_cycle(cls):
        return False

    return all(_is_enums_hierarchy_valid(superset) for superset in cls.__supersets__)


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

        classdict['_missing_'] = classmethod(_missing_)
        new_cls = super().__new__(metacls, cls, bases, classdict)

        for subset in classdict.get('__subsets__'):
            subset.__supersets__.append(new_cls)
        
        for superset in classdict.get('__supersets__'):
            superset.__subsets__.append(new_cls)

        if not _is_enums_hierarchy_valid(new_cls):
            for subset in classdict.get('__subsets__'):
                subset.__supersets__.remove(new_cls)
            
            for superset in classdict.get('__supersets__'):
                superset.__subsets__.remove(new_cls)
            
            raise RuntimeError(f"Definition of {new_cls.__name__} introduces cycle in a sets!")

        for subset in classdict.get('__subsets__'):
            _copy_members_from_subset_to_superset(subset, new_cls)
        
        for superset in classdict.get('__supersets__'):
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

    def mro(cls, *args, **kwargs):
        subsets = getattr(cls, '__subsets__', [])
        if not subsets:
            return super().mro()
        
        print('MRO() called for ', cls)
        
        return super().mro()


class SetEnum(Enum, metaclass=SetEnumMeta):
    __subsets__: Iterable[Any] = []
    __supersets__: Iterable[Any] = []
    pass
        
