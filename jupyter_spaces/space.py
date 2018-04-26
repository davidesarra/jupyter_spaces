from jupyter_spaces.errors import RegistryError


class SpaceRegister:
    __slots__ = ['_register']

    def __init__(self):
        """Initialise SpaceRegister instance."""
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
            raise RegistryError('Failed to forget space {name} because '
                                'it does not exist'.format(name=name))

    def remove_all_spaces(self):
        """Remove all Spaces from register."""
        self._register.clear()


class Space:
    __slots__ = ['_execution_namespace', '_name']

    def __init__(self, name, outer_space):
        """Initialise Space instance.

        Args:
            name (str): Name of the space.
            outer_space (dict): Outer namespace.
        """
        self._name = name
        self._execution_namespace = ExecutionNamespace(
            global_references=outer_space, local_references={})

    def __repr__(self):
        return "Space(name='{name}', namespace={namespace})".format(
            name=self.name, namespace=self.namespace)

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
        return self._execution_namespace.local_references

    def execute(self, source):
        """Execute source code inside the space namespace and outer namespace.

        Args:
            source (str): Source code.
        """
        exec(source, self._execution_namespace)


class ExecutionNamespace(dict):

    def __init__(self, global_references, local_references):
        self.global_references = global_references
        self.local_references = local_references

    def __getitem__(self, key):
        try:
            return self.local_references[key]
        except KeyError:
            return self.global_references[key]

    def __setitem__(self, key, value):
        self.local_references[key] = value

    def __delitem__(self, key):
        del self.local_references[key]
