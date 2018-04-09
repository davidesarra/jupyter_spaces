from IPython.core.magic import cell_magic, line_magic, Magics, magics_class

from jupyter_spaces.space import SpaceRegister


space_register = SpaceRegister()


@magics_class
class SpaceMagic(Magics):

    @cell_magic
    def space(self, line, cell):
        """Execute cell contents using the space namespace as locals and the
        user namespace as globals.

        Args:
            line (str): Content following `%%space` magic call, expected to
                match the space name. If the provided space name has already
                been used and not been removed, the same space object is used.
            cell (str): Content following the first line.

        Examples:
            >>> %%space space_name
            ... alpha = 0.50
            ... print(alpha)
        """
        space = space_register.get_space(
            name=line, outer_space=self.shell.user_ns)
        space.execute(source=cell)

    @line_magic
    def remove_space(self, line):
        """Remove a space.

        Args:
            line (str): Content following `%%remove_space` magic call, expected
                to match the space name to remove.

        Examples:
            >>> %remove_space space_name
        """
        space_register.remove_space(name=line)
