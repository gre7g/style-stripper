from aiounittest import AsyncTestCase
from asyncio import Future
from inspect import iscoroutinefunction
import os
import sys
from unittest.mock import Mock

# Make sure this directory is above wherever wx is actually located
DIR = os.path.abspath(os.path.dirname(__file__))
if sys.path[0] != DIR:
    sys.path.insert(0, DIR)

from wx import GetApp


def completed(result=None) -> Future:
    """Return a completed future"""
    future = Future()
    future.set_result(result)
    return future


def failed(result=Exception()) -> Future:
    """Return a failed future"""
    future = Future()
    future.set_exception(result)
    return future


class wxTestCase(AsyncTestCase):
    def wrap_ctrls(self, *attrs):
        """Capture more history by replacing simple controls with simple mocks"""

        def apply():
            for attr in attrs:
                the_mock = GetApp()._the_mock
                if attr.startswith("app."):
                    attr = attr[4:]
                    setattr(self.app, attr, getattr(the_mock.app, attr))
                else:
                    setattr(self.window, attr, getattr(the_mock, attr))

        class WrappedObj:
            @staticmethod
            def __enter__():
                for attr in attrs:
                    if attr.startswith("app."):
                        attr = attr[4:]
                        setattr(self.app, attr, Mock())

            @staticmethod
            def __exit__(exc_type, exc_val, exc_tb):
                apply()

        if hasattr(self, "window"):
            apply()
        return WrappedObj()


def note_function_wrapper(self, name, func_to_wrap, *args, **kwargs):
    the_mock = GetApp()._the_mock
    getattr(the_mock, name)(*args, **kwargs)
    try:
        value = func_to_wrap(*args, **kwargs)
        if value is not None:
            getattr(the_mock, "%s_return_value" % name)(value)
        return value
    except Exception as msg:
        getattr(the_mock, "%s_raised" % name)(repr(msg))
        if getattr(self.window, "_reraise", False) is True:
            raise


async def async_note_function_wrapper(self, name, func_to_wrap, *args, **kwargs):
    the_mock = GetApp()._the_mock
    getattr(the_mock, name)(*args, **kwargs)
    try:
        value = await func_to_wrap(*args, **kwargs)
        if value is not None:
            getattr(the_mock, "%s_return_value" % name)(value)
        return value
    except Exception as msg:
        getattr(the_mock, "%s_raised" % name)(repr(msg))
        if getattr(self.window, "_reraise", False) is True:
            raise


def note_func(name):
    """Note when a function is called in the mock history"""

    def wrapped1(func):
        def wrapped2(self, *args2, **kwargs2):
            func_to_wrap = getattr(self.window, name)
            wrapper = (
                async_note_function_wrapper
                if iscoroutinefunction(func_to_wrap)
                else note_function_wrapper
            )
            setattr(
                self.window,
                name,
                lambda *args, **kwargs: wrapper(
                    self, name, func_to_wrap, *args, **kwargs
                ),
            )
            return func(self, *args2, **kwargs2)

        async def wrapped2a(self, *args2, **kwargs2):
            func_to_wrap = getattr(self.window, name)
            wrapper = (
                async_note_function_wrapper
                if iscoroutinefunction(func_to_wrap)
                else note_function_wrapper
            )
            setattr(
                self.window,
                name,
                lambda *args, **kwargs: wrapper(
                    self, name, func_to_wrap, *args, **kwargs
                ),
            )
            return await func(self, *args2, **kwargs2)

        return wrapped2a if iscoroutinefunction(func) else wrapped2

    return wrapped1
