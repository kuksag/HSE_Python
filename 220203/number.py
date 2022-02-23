from attrs import define
import numpy as np
import numbers


class Dumper:
    def dump(self, file):
        with open(file, 'w+') as fd:
            print(self.__str__(), file=fd)


class PrettyPrint:
    def __str__(self):
        return f'PrettyPrint: {self.value}!'


class Getter:
    def get(self):
        return self.value


class Setter:
    def set(self, other):
        self.value = other


@define(init=False, repr=False)
class ArrayLike(np.lib.mixins.NDArrayOperatorsMixin, Getter, Setter, PrettyPrint, Dumper):
    def __init__(self, value):
        self.value = np.asarray(value)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.value)

    # One might also consider adding the built-in list type to this
    # list, to support operations like np.add(array_like, list)
    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            # Only support operations with instances of _HANDLED_TYPES.
            # Use ArrayLike instead of type(self) for isinstance to
            # allow subclasses that don't override __array_ufunc__ to
            # handle ArrayLike objects.
            if not isinstance(x, self._HANDLED_TYPES + (ArrayLike,)):
                return NotImplemented

        # Defer to the implementation of the ufunc on unwrapped values.
        inputs = tuple(x.value if isinstance(x, ArrayLike) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, ArrayLike) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)