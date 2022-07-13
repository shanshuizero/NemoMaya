# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _NemoMaya
else:
    import _NemoMaya

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


import weakref

class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _NemoMaya.delete_SwigPyIterator

    def value(self):
        return _NemoMaya.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _NemoMaya.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _NemoMaya.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _NemoMaya.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _NemoMaya.SwigPyIterator_equal(self, x)

    def copy(self):
        return _NemoMaya.SwigPyIterator_copy(self)

    def next(self):
        return _NemoMaya.SwigPyIterator_next(self)

    def __next__(self):
        return _NemoMaya.SwigPyIterator___next__(self)

    def previous(self):
        return _NemoMaya.SwigPyIterator_previous(self)

    def advance(self, n):
        return _NemoMaya.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _NemoMaya.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _NemoMaya.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _NemoMaya.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _NemoMaya.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _NemoMaya.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _NemoMaya.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _NemoMaya:
_NemoMaya.SwigPyIterator_swigregister(SwigPyIterator)

class StrVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _NemoMaya.StrVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _NemoMaya.StrVector___nonzero__(self)

    def __bool__(self):
        return _NemoMaya.StrVector___bool__(self)

    def __len__(self):
        return _NemoMaya.StrVector___len__(self)

    def __getslice__(self, i, j):
        return _NemoMaya.StrVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _NemoMaya.StrVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _NemoMaya.StrVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _NemoMaya.StrVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _NemoMaya.StrVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _NemoMaya.StrVector___setitem__(self, *args)

    def pop(self):
        return _NemoMaya.StrVector_pop(self)

    def append(self, x):
        return _NemoMaya.StrVector_append(self, x)

    def empty(self):
        return _NemoMaya.StrVector_empty(self)

    def size(self):
        return _NemoMaya.StrVector_size(self)

    def swap(self, v):
        return _NemoMaya.StrVector_swap(self, v)

    def begin(self):
        return _NemoMaya.StrVector_begin(self)

    def end(self):
        return _NemoMaya.StrVector_end(self)

    def rbegin(self):
        return _NemoMaya.StrVector_rbegin(self)

    def rend(self):
        return _NemoMaya.StrVector_rend(self)

    def clear(self):
        return _NemoMaya.StrVector_clear(self)

    def get_allocator(self):
        return _NemoMaya.StrVector_get_allocator(self)

    def pop_back(self):
        return _NemoMaya.StrVector_pop_back(self)

    def erase(self, *args):
        return _NemoMaya.StrVector_erase(self, *args)

    def __init__(self, *args):
        _NemoMaya.StrVector_swiginit(self, _NemoMaya.new_StrVector(*args))

    def push_back(self, x):
        return _NemoMaya.StrVector_push_back(self, x)

    def front(self):
        return _NemoMaya.StrVector_front(self)

    def back(self):
        return _NemoMaya.StrVector_back(self)

    def assign(self, n, x):
        return _NemoMaya.StrVector_assign(self, n, x)

    def resize(self, *args):
        return _NemoMaya.StrVector_resize(self, *args)

    def insert(self, *args):
        return _NemoMaya.StrVector_insert(self, *args)

    def reserve(self, n):
        return _NemoMaya.StrVector_reserve(self, n)

    def capacity(self):
        return _NemoMaya.StrVector_capacity(self)
    __swig_destroy__ = _NemoMaya.delete_StrVector

# Register StrVector in _NemoMaya:
_NemoMaya.StrVector_swigregister(StrVector)

class vec3(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, x, y, z):
        _NemoMaya.vec3_swiginit(self, _NemoMaya.new_vec3(x, y, z))
    __swig_destroy__ = _NemoMaya.delete_vec3

# Register vec3 in _NemoMaya:
_NemoMaya.vec3_swigregister(vec3)


def get_timestamp():
    return _NemoMaya.get_timestamp()
class Parser(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def append_module_path(self, path):
        return _NemoMaya.Parser_append_module_path(self, path)

    def init(self, dir, debug):
        return _NemoMaya.Parser_init(self, dir, debug)

    def set_inputs(self, inputs):
        return _NemoMaya.Parser_set_inputs(self, inputs)

    def parse(self, output):
        return _NemoMaya.Parser_parse(self, output)

    def clean(self):
        return _NemoMaya.Parser_clean(self)

    def dump_graph(self, path):
        return _NemoMaya.Parser_dump_graph(self, path)

    def dump_resource(self, path):
        return _NemoMaya.Parser_dump_resource(self, path)

    def dump_debug(self, path):
        return _NemoMaya.Parser_dump_debug(self, path)
    State_Dynamic = _NemoMaya.Parser_State_Dynamic
    State_Static = _NemoMaya.Parser_State_Static
    State_Default = _NemoMaya.Parser_State_Default

    def add_custom_parameter(self, parameter):
        return _NemoMaya.Parser_add_custom_parameter(self, parameter)

    def __init__(self):
        _NemoMaya.Parser_swiginit(self, _NemoMaya.new_Parser())
    __swig_destroy__ = _NemoMaya.delete_Parser

# Register Parser in _NemoMaya:
_NemoMaya.Parser_swigregister(Parser)

class CustomParameter(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _NemoMaya.delete_CustomParameter
    index_mask = property(_NemoMaya.CustomParameter_index_mask_get, _NemoMaya.CustomParameter_index_mask_set)
    is_stack = property(_NemoMaya.CustomParameter_is_stack_get, _NemoMaya.CustomParameter_is_stack_set)
    typeH = property(_NemoMaya.CustomParameter_typeH_get, _NemoMaya.CustomParameter_typeH_set)
    method_name = property(_NemoMaya.CustomParameter_method_name_get, _NemoMaya.CustomParameter_method_name_set)

    def process(self, plug, graph, resource, port, clientData):
        return _NemoMaya.CustomParameter_process(self, plug, graph, resource, port, clientData)

# Register CustomParameter in _NemoMaya:
_NemoMaya.CustomParameter_swigregister(CustomParameter)

class IntCustomParameter(CustomParameter):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        if self.__class__ == IntCustomParameter:
            _self = None
        else:
            _self = self
        _NemoMaya.IntCustomParameter_swiginit(self, _NemoMaya.new_IntCustomParameter(_self, ))
    __swig_destroy__ = _NemoMaya.delete_IntCustomParameter

    def get(self, arg0, arg1):
        return _NemoMaya.IntCustomParameter_get(self, arg0, arg1)
    def __disown__(self):
        self.this.disown()
        _NemoMaya.disown_IntCustomParameter(self)
        return weakref.proxy(self)

# Register IntCustomParameter in _NemoMaya:
_NemoMaya.IntCustomParameter_swigregister(IntCustomParameter)

class Vec3CustomParameter(CustomParameter):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self):
        if self.__class__ == Vec3CustomParameter:
            _self = None
        else:
            _self = self
        _NemoMaya.Vec3CustomParameter_swiginit(self, _NemoMaya.new_Vec3CustomParameter(_self, ))
    __swig_destroy__ = _NemoMaya.delete_Vec3CustomParameter

    def get(self, arg0, arg1):
        return _NemoMaya.Vec3CustomParameter_get(self, arg0, arg1)
    def __disown__(self):
        self.this.disown()
        _NemoMaya.disown_Vec3CustomParameter(self)
        return weakref.proxy(self)

# Register Vec3CustomParameter in _NemoMaya:
_NemoMaya.Vec3CustomParameter_swigregister(Vec3CustomParameter)

class BinaryCustomParameter(CustomParameter):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _NemoMaya.delete_BinaryCustomParameter

    def get(self, arg2, arg3, arg4):
        return _NemoMaya.BinaryCustomParameter_get(self, arg2, arg3, arg4)

    def process(self, plug, graph, resource, port, clientData):
        return _NemoMaya.BinaryCustomParameter_process(self, plug, graph, resource, port, clientData)

# Register BinaryCustomParameter in _NemoMaya:
_NemoMaya.BinaryCustomParameter_swigregister(BinaryCustomParameter)

class BinaryListCustomParameter(CustomParameter):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _NemoMaya.delete_BinaryListCustomParameter

    def get(self, arg2, arg3, arg4):
        return _NemoMaya.BinaryListCustomParameter_get(self, arg2, arg3, arg4)

    def process(self, plug, graph, resource, port, clientData):
        return _NemoMaya.BinaryListCustomParameter_process(self, plug, graph, resource, port, clientData)

# Register BinaryListCustomParameter in _NemoMaya:
_NemoMaya.BinaryListCustomParameter_swigregister(BinaryListCustomParameter)


def add_custom_parameters_for_builtin(arg1, arg2):
    return _NemoMaya.add_custom_parameters_for_builtin(arg1, arg2)

