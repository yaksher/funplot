import matplotlib.pyplot as _plt
import numpy as _np
import sympy as _sp

from typing import Callable, Union

class Space:
    def __init__(self, objects = None, **kwargs):
        self._kwargs = kwargs
        self._objects = PhsyicalCollection() if objects is None else objects
    
    def __add__(self, obj):
        space = self.copy()
        space._objects += obj
        return space

    def copy(self):
        space = Space(self._objects)
        space._kwargs = self._kwargs
        return space

    def plot(self):
        self._objects.plot()
        for key, value in self._kwargs.items():
            getattr(_plt, key)(value)

    def show(self):
        self.plot()
        _plt.show()

    def plus(self, obj):
        return self + obj
    
    def save(self, filename, **kwargs):
        self.plot()
        _plt.savefig(filename, **kwargs)
        _plt.close()

class Physical:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def plot(self):
        _plt.plot(*self._args, **self._kwargs)

    def show(self):
        self.plot()
        _plt.show()

    def __add__(self, other: "Physical"):
        if isinstance(other, PhsyicalCollection):
            return PhsyicalCollection([self] + other.objects)
        elif isinstance(other, Physical):
            return PhsyicalCollection([self, other])
        else:
            raise TypeError("Can only add Physical objects to Physical objects")

        

class PhsyicalCollection(Physical):
    def __init__(self, objects: list[Physical] = None):
        self._objects = objects if objects else []

    @property
    def objects(self):
        return self._objects

    def __add__(self, obj):
        if isinstance(obj, PhsyicalCollection):
            return PhsyicalCollection(self._objects + obj.objects)
        elif isinstance(obj, Physical):
            return PhsyicalCollection(self._objects + [obj])
        else:
            raise TypeError("Can only add Physical objects to Physical objects")

    def plot(self):
        for obj in self._objects:
            obj.plot()


class Func(Physical):
    def __init__(self, func, domain = None, vectorize = False, **kwargs):
        if isinstance(func, str):
            expr = _sp.sympify(func)
            expr.subs(_sp.Symbol("e"), _np.e)
            expr.subs(_sp.Symbol("pi"), _np.pi)
            expr.subs(_sp.Symbol("π"), _np.pi)
            if len(expr.free_symbols) == 1:
                var = expr.free_symbols.pop()
            else:
                raise ValueError("Function must have exactly one variable.")

            try:
                f = _sp.lambdify(var, expr, modules=_np)
            except:
                f = _np.vectorize(lambda x: expr.subs(var, x))
            self._func = f
        elif callable(func):
            if vectorize:
                func = _np.vectorize(func)
            self._func = func
        else:
            raise TypeError("Function must be a string or a callable object.")

        if isinstance(domain, tuple):
            self._domain = _np.linspace(*domain)
        elif isinstance(domain, _np.ndarray):
            self._domain = domain
        elif domain is None:
            self._domain = _np.linespace(-10, 10, 100)
        else:
            raise TypeError("Domain must be a tuple or a numpy array.")

        self._kwargs = kwargs

    def plot(self):
        _plt.plot(self._domain, self._func(self._domain), **self._kwargs)

class Curve(Physical):
    def __init__(self, x, y, **kwargs):
        self._x = x
        self._y = y
        self._kwargs = kwargs

    def plot(self):
        _plt.plot(self._x, self._y, **self._kwargs)

class Points(Physical):
    def __init__(self, x, y, **kwargs):
        self._x = x
        self._y = y
        self._kwargs = kwargs

    def plot(self):
        _plt.scatter(self._x, self._y, **self._kwargs)