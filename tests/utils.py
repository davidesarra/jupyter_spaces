from io import StringIO
import json

import nbformat


class NotebookBuilder:
    """Build a Jupyter notebook made of code cells by passing the notebook
    format version and the source code for each cell."""

    def __init__(self, nbformat_major, nbformat_minor):
        """Initialise NotebookBuilder instance.

        Args:
            nbformat_major (int): Major version of notebook format.
            nbformat_minor (int): Minor version of notebook format.
        """
        self._nbformat_major = nbformat_major
        self._nbformat_minor = nbformat_minor

    def build(self, cells):
        """Build notebook.

        Args:
            cells (list<list<str>>): List of source code cells. Each cell is a
                list of the its code lines.

        Returns:
            nbformat.NotebookNode: Jupyter notebook.
        """
        notebook_mapping = self._format_cells(cells=cells)
        notebook_json = json.dumps(obj=notebook_mapping, ensure_ascii=False)
        notebook_file = StringIO(initial_value=notebook_json)
        return nbformat.read(fp=notebook_file, as_version=self._nbformat_major)

    def _format_cells(self, cells):
        return dict(
            cells=[self._format_cell(cell=cell) for cell in cells],
            metadata={},
            nbformat=self._nbformat_major,
            nbformat_minor=self._nbformat_minor
        )

    def _format_cell(self, cell):
        return dict(
            cell_type='code',
            execution_count=None,
            metadata={},
            outputs=[],
            source=self._format_source(source=cell),
        )

    def _format_source(self, source):
        """Add a trailing new line to all source lines but the last one."""
        return ['{}\n'.format(line) for line in source[:-1]] + [source[-1]]
