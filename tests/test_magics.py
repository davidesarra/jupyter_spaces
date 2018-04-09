from nbconvert.preprocessors import ExecutePreprocessor

from tests.utils import NotebookBuilder


notebook_builder = NotebookBuilder(nbformat_major=4, nbformat_minor=2)
notebook_processor = ExecutePreprocessor(timeout=20)
notebook_resources = {}


def test_space_can_access_user_namespace_references():
    cells = [
        ['%load_ext jupyter_spaces'],
        ['reference = 100'],
        ['%%space tomato',
         'assert reference == 100']
    ]
    notebook = notebook_builder.build(cells=cells)
    notebook_processor.preprocess(nb=notebook, resources=notebook_resources)


def test_space_references_prioritised_over_user_namespace_references():
    cells = [
        ['%load_ext jupyter_spaces'],
        ['reference = 100'],
        ['%%space tomato',
         'reference = 99',
         'assert reference == 99']
    ]
    notebook = notebook_builder.build(cells=cells)
    notebook_processor.preprocess(nb=notebook, resources=notebook_resources)


def test_space_cannot_alter_user_namespace_references():
    cells = [
        ['%load_ext jupyter_spaces'],
        ['reference = 100'],
        ['%%space tomato',
         'reference = 99'],
        ['assert reference == 100']
    ]
    notebook = notebook_builder.build(cells=cells)
    notebook_processor.preprocess(nb=notebook, resources=notebook_resources)


def test_space_can_alter_user_namespace_references_using_global():
    cells = [
        ['%load_ext jupyter_spaces'],
        ['reference = 100'],
        ['%%space tomato',
         'global reference',
         'reference = 99'],
        ['assert reference == 99']
    ]
    notebook = notebook_builder.build(cells=cells)
    notebook_processor.preprocess(nb=notebook, resources=notebook_resources)


def test_space_cannot_remove_user_namespace_references():
    cells = [
        ['import pytest'],
        ['%load_ext jupyter_spaces'],
        ['reference = 100'],
        ['%%space tomato',
         'with pytest.raises(NameError):',
         '    del reference'],
        ['assert reference == 100']
    ]
    notebook = notebook_builder.build(cells=cells)
    notebook_processor.preprocess(nb=notebook, resources=notebook_resources)


def test_space_cannot_add_user_namespace_references():
    cells = [
        ['import pytest'],
        ['%load_ext jupyter_spaces'],
        ['%%space tomato',
         'reference = 99'],
        ['with pytest.raises(NameError):',
         '    reference']
    ]
    notebook = notebook_builder.build(cells=cells)
    notebook_processor.preprocess(nb=notebook, resources=notebook_resources)


def test_get_spaces_can_access_space_references():
    cells = [
        ['from jupyter_spaces import get_spaces'],
        ['%load_ext jupyter_spaces'],
        ['%%space tomato',
         'reference = 99'],
        ['spaces = get_spaces()'],
        ['assert spaces["tomato"].namespace["reference"] == 99']
    ]
    notebook = notebook_builder.build(cells=cells)
    notebook_processor.preprocess(nb=notebook, resources=notebook_resources)


def test_get_spaces_can_alter_space_references():
    cells = [
        ['from jupyter_spaces import get_spaces'],
        ['%load_ext jupyter_spaces'],
        ['%%space tomato',
         'reference = 99'],
        ['spaces = get_spaces()'],
        ['spaces["tomato"].namespace["reference"] = 101'],
        ['%%space tomato',
         'assert reference == 101']
    ]
    notebook = notebook_builder.build(cells=cells)
    notebook_processor.preprocess(nb=notebook, resources=notebook_resources)


def test_get_spaces_can_remove_space_references():
    cells = [
        ['import pytest'],
        ['from jupyter_spaces import get_spaces'],
        ['%load_ext jupyter_spaces'],
        ['%%space tomato', 'reference = 99'],
        ['spaces = get_spaces()'],
        ['del spaces["tomato"].namespace["reference"]'],
        ['%%space tomato',
         'with pytest.raises(NameError):',
         '    reference']
    ]
    notebook = notebook_builder.build(cells=cells)
    notebook_processor.preprocess(nb=notebook, resources=notebook_resources)


def test_get_spaces_reflects_space_references_changes():
    cells = [
        ['from jupyter_spaces import get_spaces'],
        ['%load_ext jupyter_spaces'],
        ['%%space tomato',
         'reference = 99'],
        ['spaces = get_spaces()'],
        ['assert spaces["tomato"].namespace["reference"] == 99'],
        ['%%space tomato',
         'reference = 101'],
        ['assert spaces["tomato"].namespace["reference"] == 101']
    ]
    notebook = notebook_builder.build(cells=cells)
    notebook_processor.preprocess(nb=notebook, resources=notebook_resources)


def test_get_spaces_reflects_space_removal():
    cells = [
        ['from jupyter_spaces import get_spaces'],
        ['%load_ext jupyter_spaces'],
        ['%%space tomato',
         'reference = 99'],
        ['spaces = get_spaces()'],
        ['%remove_space tomato'],
        ['assert "tomato" not in spaces']
    ]
    notebook = notebook_builder.build(cells=cells)
    notebook_processor.preprocess(nb=notebook, resources=notebook_resources)


def test_get_spaces_reflects_extension_reload():
    cells = [
        ['from jupyter_spaces import get_spaces'],
        ['%load_ext jupyter_spaces'],
        ['%%space tomato',
         'reference = 99'],
        ['spaces = get_spaces()'],
        ['%reload_ext jupyter_spaces'],
        ['assert not spaces']
    ]
    notebook = notebook_builder.build(cells=cells)
    notebook_processor.preprocess(nb=notebook, resources=notebook_resources)
