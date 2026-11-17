"""
IntelliSoft Innovations Django Package

Compatibility Patch:
Python 3.14 changes `copy(super())` behavior, which breaks Django's `BaseContext.__copy__`
with: AttributeError: 'super' object has no attribute 'dicts' and no __dict__ for setting new attributes.
We patch `BaseContext.__copy__` to safely instantiate and copy the context state.
"""
try:
    from django.template.context import BaseContext

    def _base_context_copy(self):
        duplicate = self.__class__.__new__(self.__class__)
        duplicate.__dict__.update(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

    BaseContext.__copy__ = _base_context_copy
except Exception:
    pass
