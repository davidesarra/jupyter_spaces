"""Jupyter Spaces is an IPython extension for creating parallel namespaces
availabe within the user namespace. It is designed to be used via IPython
magics in Jupyter notebooks.

Copyright (c) 2018 Davide Sarra.
MIT License, see LICENSE.txt for more details.
"""
from types import MappingProxyType

from jupyter_spaces.magics import SpaceMagic as _SpaceMagic
from jupyter_spaces.magics import space_register as _space_register


def get_spaces():
    """Get a proxy mapping of the spaces.

    Returns:
        dict: Mapping of spaces with keys being space names and values being
            space namespaces.
    """
    return MappingProxyType(_space_register.register)


def load_ipython_extension(ipython):
    """Load IPython extension."""
    ipython.register_magics(_SpaceMagic)


def unload_ipython_extension(ipython):
    """Unload IPython extension. All existing spaces will be removed."""
    _space_register.remove_all_spaces()
