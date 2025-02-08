import builtins
from .api import Server, API


__all__ = ("Server", "API")
__excluded_modules__ = ("http", "api", "methods")


original_import = builtins.__import__


def custom_import(name, *args, **kwargs):
    if name in __excluded_modules__:
        raise ImportError(f"Module {name} is for internal use only.")
    return original_import(name, *args, **kwargs)


builtins.__import__ = custom_import
