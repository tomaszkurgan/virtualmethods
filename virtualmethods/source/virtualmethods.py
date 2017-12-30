"""Bring non-virtual attributes into Python environment.

In Python world, all attributes are indeed virtual, but there are
some cases, where this behaviour is undesired and C++ish behaviour
is more suitable.
In such cases, this module will save the day.
"""

import types
import gc
import inspect
from functools import wraps
from types import FunctionType

# semi-enum values used with virtual_methods metaclass factory
VIRTUAL = 1
NON_VIRTUAL = 2


def _is_dunder(name):
    """Test, if name is dunder name."""
    return name[:2] == name[-2:] == '__'


def _is_method_implemented(cls, method_name):
    # NOTE: getattr(cls, method_name) for some attributes returns default
    # implementation, like, `slot wrapper` for __getattrbiute__,
    # that's why we must test it's type against MethodType
    return isinstance(getattr(cls, method_name), types.MethodType)


def _guess_caller(caller_type_filter=FunctionType):
    """Try to return caller function object.

    It is different than getting caller using just `inspect.stack()` in such a way,
    it returns an actual function object, not a code object.

    Be careful, this is a Wonderland with a bunch of rabbit wholes.

    Returns:
        caller function object or None, if object can't be retrieved.
    """
    # Wonderland, rabbit whole no.1
    frame = inspect.stack()[2][0]
    try:
        # Wonderland, rabbit whole no.2
        # From docs.python.org: 'Avoid using get_referrers() for any purpose other than debugging.'
        # Evil is around us...
        referrers = gc.get_referrers(frame.f_code)
        if not referrers:
            return None

        # Wonderland, rabbit whole no.3
        fn = [ref for ref in referrers if isinstance(ref, caller_type_filter)]
        if not fn:
            return None
        return fn[0]
    finally:
        del frame


def _guess_owner_class(obj):
    try:
        return obj._owner_cls
    except AttributeError:
        # if obj doesn't have owner_cls attribute, let's check obj's outer scope
        pass
    try:
        return obj._wrapper._owner_cls
    except AttributeError:
        # there's nothing we can do more
        return None


def _implement_getattribute(cls):
    def __getattribute__(self, attr_name):
        caller = _guess_caller()
        caller_class = _guess_owner_class(caller)

        if not caller_class:
            return super(cls, self).__getattribute__(attr_name)

        try:
            attr = getattr(caller_class, attr_name)
            if isinstance(attr, property) and getattr(attr.fget, '_non_virtual_method', False):
                return attr.__get__(self)
            # https://docs.python.org/2/reference/datamodel.html#index-38
            # Methods also support accessing (but not setting) the arbitrary
            # function attributes on the underlying function object.
            elif isinstance(attr, types.MethodType) and getattr(attr, '_non_virtual_method', False):
                return types.MethodType(attr, self)
            elif isinstance(attr, types.FunctionType) and getattr(attr, '_non_virtual_method', False):
                return attr
        except AttributeError:
            pass
        return super(cls, self).__getattribute__(attr_name)

    cls.__getattribute__ = __getattribute__


def _implement_setattr(cls):
    def __setattr__(self, key, value):
        caller = _guess_caller()
        caller_class = _guess_owner_class(caller)

        if not caller_class:
            return super(cls, self).__setattr__(key, value)

        try:
            attr = getattr(caller_class, key)
            if isinstance(attr, property) and getattr(attr.fset, '_non_virtual_method', False):
                return attr.__set__(self, value)
        except AttributeError:
            pass
        return super(cls, self).__setattr__(key, value)

    cls.__setattr__ = __setattr__


def _implement_magic_function(magic_function):
    @wraps(magic_function)
    def wrapper(self, *args, **kwargs):
        caller = _guess_caller()
        caller_class = _guess_owner_class(caller)

        if not caller_class:
            return magic_function(self, *args, **kwargs)

        if caller.__name__ == magic_function.__name__:
            return magic_function(self, *args, **kwargs)

        try:
            attr = getattr(caller_class, magic_function.__name__)
            if isinstance(attr, types.MethodType) and getattr(attr, '_non_virtual_method', False):
                if caller_class is getattr(wrapper, '_owner_cls', None):
                    return magic_function(self, *args, **kwargs)
                return attr._magic_function(self, *args, **kwargs)
        except AttributeError:
            pass
        return magic_function(self, *args, **kwargs)

    magic_function._wrapper = wrapper
    wrapper._magic_function = magic_function

    return wrapper


def virtual_methods(default=VIRTUAL):
    """Metaclass factory."""

    class VirtualizationMeta(type):
        def __new__(mcs, name, bases, namespace):
            # reimplement user-defined magic methods
            for attr_name, attr_value in namespace.iteritems():
                if not _is_dunder(attr_name):
                    continue
                if attr_name in ('__init__', '__new__'):
                    continue
                if not isinstance(attr_value, types.FunctionType):
                    continue
                namespace[attr_name] = _implement_magic_function(attr_value)

            # build class - we will need it later, for __getattribute__ and __setattr__ implementation
            cls = super(VirtualizationMeta, mcs).__new__(mcs, name, bases, namespace)

            # do not reimplement __getattribute__ if it is already defined somewhere
            # in the top of the inheritance hierarchy, especially, it the existing
            # implementation is our own
            if not _is_method_implemented(cls, '__getattribute__'):
                _implement_getattribute(cls)
            # the same for __setattr__ as for __getattribute__
            if not _is_method_implemented(cls, '__setattr__'):
                _implement_setattr(cls)

            # setup additional attributes for class methods and properties
            def setup_attrs(obj):
                setattr(obj, '_owner_cls', cls)
                setattr(obj, '_non_virtual_method', getattr(obj, '_non_virtual_method', bool(default == NON_VIRTUAL)))

            # setup class attributes, but only these ones defined by a user
            for attr_name in namespace.iterkeys():
                attr_value = getattr(cls, attr_name)
                if isinstance(attr_value, types.MethodType):
                    setup_attrs(attr_value.__func__)
                elif isinstance(attr_value, property):
                    map(setup_attrs,
                        (f for f in (getattr(attr_value, f_name) for f_name in ('fget', 'fset', 'fdel')) if f))
                elif isinstance(attr_value, types.FunctionType):
                    setup_attrs(attr_value)

            return cls

    return VirtualizationMeta


def virtual_method(fn):
    fn._non_virtual_method = False
    return fn


def non_virtual_method(fn):
    fn._non_virtual_method = True
    return fn
