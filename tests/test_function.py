import unittest
import inspect
import types

import wrapt

from compat import exec_, getfullargspec

DECORATORS_CODE = """
import wrapt

@wrapt.decorator
def passthru_decorator(wrapped, instance, args, kwargs):
    return wrapped(*args, **kwargs)
"""

decorators = types.ModuleType('decorators')
exec_(DECORATORS_CODE, decorators.__dict__, decorators.__dict__)

def function1(arg):
    '''documentation'''
    return arg

function1o = function1
function1d = decorators.passthru_decorator(function1)
assert(function1d is not function1o)

class TestNamingFunction(unittest.TestCase):

    def test_object_name(self):
        # Test preservation of function __name__ attribute.

        self.assertEqual(function1d.__name__, function1o.__name__)

    def test_object_qualname(self):
        # Test preservation of function __qualname__ attribute.

        try:
            __qualname__ = function1o.__qualname__
        except AttributeError:
            pass
        else:
            self.assertEqual(function1d.__qualname__, __qualname__)

    def test_module_name(self):
        # Test preservation of function __module__ attribute.

        self.assertEqual(function1d.__module__, __name__)

    def test_doc_string(self):
        # Test preservation of function __doc__ attribute.

        self.assertEqual(function1d.__doc__, function1o.__doc__)

    def test_argspec(self):
        # Test preservation of function argument specification.

        function1o_argspec = getfullargspec(function1o)
        function1d_argspec = getfullargspec(function1d)
        self.assertEqual(function1o_argspec, function1d_argspec)

    def test_getmembers(self):
        function1o_members = inspect.getmembers(function1o)
        function1d_members = inspect.getmembers(function1d)

    def test_isinstance(self):
        # Test preservation of isinstance() checks.

        self.assertTrue(isinstance(function1d, type(function1o)))

class TestCallingFunction(unittest.TestCase):

    def test_call_function(self):
        _args = (1, 2)
        _kwargs = {'one': 1, 'two': 2}

        @wrapt.decorator
        def _decorator(wrapped, instance, args, kwargs):
            self.assertEqual(instance, None)
            self.assertEqual(args, _args)
            self.assertEqual(kwargs, _kwargs)
            return wrapped(*args, **kwargs)

        @_decorator
        def _function(*args, **kwargs):
            return args, kwargs

        result = _function(*_args, **_kwargs)

        self.assertEqual(result, (_args, _kwargs))

if __name__ == '__main__':
    unittest.main()
