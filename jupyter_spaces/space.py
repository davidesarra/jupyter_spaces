import ast
import sys
from collections import ChainMap

from jupyter_spaces.errors import RegistryError


class SpaceRegister:
    __slots__ = ["_register"]

    def __init__(self):
        """Instantiate SpaceRegister."""
        self._register = {}

    @property
    def register(self):
        """Register.

        Returns:
            dict: Register of Space instances.
        """
        return self._register

    def get_space(self, name, outer_space):
        """Get existing Space if a Space has the same name, otherwise create
        and get new Space.

        Args:
            name (str): Name of the Space.
            outer_space (dict): User namespace.

        Returns:
            Space: Space.
        """
        if name not in self._register:
            self._register[name] = Space(name=name, outer_space=outer_space)
        return self._register[name]

    def remove_space(self, name):
        """Remove Space from register.

        Args:
            name (str): Name of the Space.

        Raises:
            RegistryError: If no registered Space has the name passed.
        """
        try:
            del self._register[name]
        except KeyError:
            raise RegistryError(
                "Cannot remove space {name} because "
                "it does not exist".format(name=name)
            )

    def remove_all_spaces(self):
        """Remove all Spaces from register."""
        self._register.clear()


class Space:
    __slots__ = ["_execution_namespace", "_name"]

    def __init__(self, name, outer_space):
        """Instantiate Space.

        Args:
            name (str): Name of the space.
            outer_space (dict): Outer namespace.
        """
        self._name = name
        self._execution_namespace = _ChainNamespace({}, outer_space)

    def __repr__(self):
        return "Space(name={name}, size={size:d})".format(
            name=self.name, size=len(self.namespace)
        )

    @property
    def name(self):
        """Name of the Space instance.

        Returns:
            str: Name.
        """
        return self._name

    @property
    def namespace(self):
        """Namespace of the Space instance.

        Note that modifying the namespace will modify the actual namespace
        of the Space instance.

        Returns:
            dict: Namespace.
        """
        return self._execution_namespace.maps[0]

    def execute(self, source):
        """Execute source code inside the space namespace and outer namespace.

        Args:
            source (str): Source code.
        """
        tree = ast.parse(source=source)
        self._execute(body=tree.body[:-1], mode="exec")
        self._execute(body=tree.body[-1:], mode="single")

    def _execute(self, body, mode):
        tree_types = {"exec": ast.Module, "single": ast.Interactive}
        tree = tree_types[mode](body=body)
        if sys.version_info > (3, 8):
            tree.type_ignores = []
        code = compile(source=tree, filename="<string>", mode=mode)
        exec(code, self._execution_namespace)


class _ChainNamespace(ChainMap, dict):
    pass
