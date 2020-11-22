from pytest import raises


def test_space_can_access_user_namespace_references(ip):
    ip.run_cell(raw_cell="x = 100")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x")


def test_space_references_prioritized_over_user_namespace_references(ip):
    ip.run_cell(raw_cell="x = 100")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99; assert x == 99")


def test_space_cannot_alter_user_namespace_immutable_references(ip):
    ip.run_cell(raw_cell="x = 100")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99")
    assert ip.user_global_ns["x"] == 100


def test_space_can_alter_user_namespace_mutable_references(ip):
    ip.run_cell(raw_cell="x = [1, 2, 3]")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x[-1] = 10")
    assert ip.user_global_ns["x"] == [1, 2, 10]


def test_space_cannot_alter_user_namespace_references_using_global(ip):
    ip.run_cell(raw_cell="x = 100")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="global x; x = 99")
    assert ip.user_global_ns["x"] == 100


def test_space_cannot_remove_user_namespace_references(ip):
    ip.run_cell(raw_cell="x = 100")
    with raises(NameError):
        ip.run_cell_magic(magic_name="space", line="tomato", cell="del x")
    assert ip.user_global_ns["x"] == 100


def test_space_cannot_remove_user_namespace_references_using_global(ip):
    ip.run_cell(raw_cell="x = 100")
    with raises(NameError):
        ip.run_cell_magic(magic_name="space", line="tomato", cell="global x; del x")
    assert "x" in ip.user_global_ns


def test_space_cannot_add_user_namespace_references(ip):
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99")
    assert "x" not in ip.user_global_ns


def test_space_cannot_add_user_namespace_references_using_global(ip):
    ip.run_cell_magic(magic_name="space", line="tomato", cell="global x; x = 99")
    assert "x" not in ip.user_global_ns


def test_space_reference_assignments_persist_in_new_magic_call(ip):
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="assert x == 99")


def test_space_reference_deletions_persist_in_new_magic_call(ip):
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="del x")
    with raises(NameError):
        ip.run_cell_magic(magic_name="space", line="tomato", cell="x")


def test_space_references_assignments_are_confined_in_one_space_only(ip):
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99")
    ip.run_cell_magic(magic_name="space", line="potato", cell="x = 100")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="assert x == 99")


def test_space_references_deletions_are_confined_in_one_space_only(ip):
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99")
    with raises(NameError):
        ip.run_cell_magic(magic_name="space", line="potato", cell="del x")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="assert x == 99")


def test_space_can_execute_newly_defined_lambda_functions(ip):
    ip.run_cell_magic(
        magic_name="space",
        line="tomato",
        cell="f = lambda x: x + 1; y = f(x=2); assert y == 3",
    )


def test_space_can_execute_newly_defined_functions(ip):
    ip.run_cell_magic(
        magic_name="space",
        line="tomato",
        cell="def f(x): return x + 1; y = f(x=2); assert y == 3",
    )


def test_space_can_execute_top_level_non_closure_functions(ip):
    ip.run_cell_magic(
        magic_name="space",
        line="tomato",
        cell="def f(x): return x + 1\ndef g(x): return f(x=x) * 2\ny = g(x=3)",
    )
    ip.run_cell_magic(magic_name="space", line="tomato", cell="assert y == 8")


def test_get_spaces_can_access_space_references(ip):
    ip.run_cell(raw_cell="from jupyter_spaces import get_spaces")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99")
    ip.run_cell(raw_cell="spaces = get_spaces()")
    assert ip.user_global_ns["spaces"]["tomato"].namespace["x"] == 99


def test_get_spaces_can_alter_space_references(ip):
    ip.run_cell(raw_cell="from jupyter_spaces import get_spaces")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99")
    ip.run_cell(raw_cell="spaces = get_spaces()")
    ip.run_cell(raw_cell='spaces["tomato"].namespace["x"] = 101')
    assert ip.user_global_ns["spaces"]["tomato"].namespace["x"] == 101


def test_get_spaces_can_remove_space_references(ip):
    ip.run_cell(raw_cell="from jupyter_spaces import get_spaces")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99")
    ip.run_cell(raw_cell="spaces = get_spaces()")
    ip.run_cell(raw_cell='del spaces["tomato"].namespace["x"]')
    assert "x" not in ip.user_global_ns["spaces"]["tomato"].namespace


def test_get_spaces_reflects_space_references_changes(ip):
    ip.run_cell(raw_cell="from jupyter_spaces import get_spaces")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99")
    ip.run_cell(raw_cell="spaces = get_spaces()")
    ip.run_cell(raw_cell='spaces["tomato"].namespace["x"] = 101')
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 11")
    assert ip.user_global_ns["spaces"]["tomato"].namespace["x"] == 11


def test_get_spaces_reflects_space_removal(ip):
    ip.run_cell(raw_cell="from jupyter_spaces import get_spaces")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99")
    ip.run_cell(raw_cell="spaces = get_spaces()")
    ip.run_line_magic(magic_name="remove_space", line="tomato")
    assert "tomato" not in ip.user_global_ns["spaces"]


def test_get_spaces_reflects_extension_reload(ip):
    ip.run_cell(raw_cell="from jupyter_spaces import get_spaces")
    ip.run_cell_magic(magic_name="space", line="tomato", cell="x = 99")
    ip.run_cell(raw_cell="spaces = get_spaces()")
    ip.run_line_magic(magic_name="reload_ext", line="jupyter_spaces")
    assert not ip.user_global_ns["spaces"]


def test_space_outputs_to_console(ip, capsys):
    ip.run_cell_magic(magic_name="space", line="tomato", cell="100")
    assert capsys.readouterr().out == "100\n"


def test_space_can_print_to_console(ip, capsys):
    ip.run_cell_magic(magic_name="space", line="tomato", cell="print(100)")
    assert capsys.readouterr().out == "100\n"
