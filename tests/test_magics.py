from IPython.utils.io import capture_output
import pytest

from tests.fixtures import ip, global_ip


def test_space_can_access_user_namespace_references(ip):
    ip.run_cell(raw_cell='reference = 100')
    ip.run_cell_magic(magic_name='space', line='tomato', cell='reference')


def test_space_references_prioritised_over_user_namespace_references(ip):
    ip.run_cell(raw_cell='reference = 100')
    ip.run_cell_magic(magic_name='space', line='tomato',
                      cell='reference = 99; assert reference == 99')


def test_space_cannot_alter_user_namespace_references(ip):
    ip.run_cell(raw_cell='reference = 100')
    ip.run_cell_magic(magic_name='space', line='tomato', cell='reference = 99')
    assert ip.user_global_ns['reference'] == 100


def test_space_can_alter_user_namespace_references_using_global(ip):
    ip.run_cell(raw_cell='reference = 100')
    ip.run_cell_magic(magic_name='space', line='tomato',
                      cell='global reference; reference = 99')
    assert ip.user_global_ns['reference'] == 99


def test_space_cannot_remove_user_namespace_references(ip):
    ip.run_cell(raw_cell='reference = 100')
    with pytest.raises(NameError):
        ip.run_cell_magic(magic_name='space', line='tomato',
                          cell='del reference')
    assert ip.user_global_ns['reference'] == 100


def test_space_can_remove_user_namespace_references_using_global(ip):
    ip.run_cell(raw_cell='reference = 100')
    ip.run_cell_magic(magic_name='space', line='tomato',
                        cell='global reference; del reference')
    assert 'reference' not in ip.user_global_ns


def test_space_cannot_add_user_namespace_references(ip):
    ip.run_cell_magic(magic_name='space', line='tomato', cell='reference = 99')
    assert 'reference' not in ip.user_global_ns


def test_space_can_add_user_namespace_references_using_global(ip):
    ip.run_cell_magic(magic_name='space', line='tomato',
                      cell='global reference; reference = 99')
    assert ip.user_global_ns['reference'] == 99


def test_get_spaces_can_access_space_references(ip):
    ip.run_cell(raw_cell='from jupyter_spaces import get_spaces')
    ip.run_cell_magic(magic_name='space', line='tomato', cell='reference = 99')
    ip.run_cell(raw_cell='spaces = get_spaces()')
    assert ip.user_global_ns['spaces']['tomato'].namespace['reference'] == 99


def test_get_spaces_can_alter_space_references(ip):
    ip.run_cell(raw_cell='from jupyter_spaces import get_spaces')
    ip.run_cell_magic(magic_name='space', line='tomato', cell='reference = 99')
    ip.run_cell(raw_cell='spaces = get_spaces()')
    ip.run_cell(raw_cell='spaces["tomato"].namespace["reference"] = 101')
    assert ip.user_global_ns['spaces']['tomato'].namespace['reference'] == 101


def test_get_spaces_can_remove_space_references(ip):
    ip.run_cell(raw_cell='from jupyter_spaces import get_spaces')
    ip.run_cell_magic(magic_name='space', line='tomato', cell='reference = 99')
    ip.run_cell(raw_cell='spaces = get_spaces()')
    ip.run_cell(raw_cell='del spaces["tomato"].namespace["reference"]')
    assert 'reference' not in ip.user_global_ns['spaces']['tomato'].namespace


def test_get_spaces_reflects_space_references_changes(ip):
    ip.run_cell(raw_cell='from jupyter_spaces import get_spaces')
    ip.run_cell_magic(magic_name='space', line='tomato', cell='reference = 99')
    ip.run_cell(raw_cell='spaces = get_spaces()')
    ip.run_cell(raw_cell='spaces["tomato"].namespace["reference"] = 101')
    ip.run_cell_magic(magic_name='space', line='tomato', cell='reference = 11')
    assert ip.user_global_ns['spaces']['tomato'].namespace['reference'] == 11


def test_get_spaces_reflects_space_removal(ip):
    ip.run_cell(raw_cell='from jupyter_spaces import get_spaces')
    ip.run_cell_magic(magic_name='space', line='tomato', cell='reference = 99')
    ip.run_cell(raw_cell='spaces = get_spaces()')
    ip.run_line_magic(magic_name='remove_space', line='tomato')
    assert 'tomato' not in ip.user_global_ns['spaces']


def test_get_spaces_reflects_extension_reload(ip):
    ip.run_cell(raw_cell='from jupyter_spaces import get_spaces')
    ip.run_cell_magic(magic_name='space', line='tomato', cell='reference = 99')
    ip.run_cell(raw_cell='spaces = get_spaces()')
    ip.run_line_magic(magic_name='reload_ext', line='jupyter_spaces')
    assert not ip.user_global_ns['spaces']


def test_space_can_print_to_console(ip):
    with capture_output() as captured:
        ip.run_cell_magic(magic_name='space', line='tomato', cell='print(100)')
    assert captured.stdout == '100\n'
