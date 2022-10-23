from pytest import raises

from jupyter_spaces.errors import RegistryError
from jupyter_spaces.space import Space, SpaceRegister


class TestSpace:
    def test_space_has_correct_name(self):
        space_name = "tomato"
        space = Space(name=space_name, outer_space={})
        assert space.name == space_name

    def test_space_can_access_user_namespace_references(self):
        outer_space = dict(x=100)
        space = Space(name="tomato", outer_space=outer_space)
        space.execute(source="assert x == 100")

    def test_space_cannot_alter_user_namespace_immutable_references(self):
        outer_space = dict(x=100)
        space = Space(name="tomato", outer_space=outer_space)
        space.execute(source="x = 99")
        assert outer_space["x"] == 100

    def test_space_can_alter_user_namespace_mutable_references(self):
        outer_space = dict(x=[1, 2, 3])
        space = Space(name="tomato", outer_space=outer_space)
        space.execute(source="x[-1] = 10")
        assert outer_space["x"] == [1, 2, 10]

    def test_space_cannot_remove_user_namespace_references(self):
        outer_space = dict(x=100)
        space = Space(name="tomato", outer_space=outer_space)
        with raises(NameError):
            space.execute(source="del x")
        assert outer_space["x"] == 100

    def test_space_cannot_add_user_namespace_references(self):
        outer_space = {}
        space = Space(name="tomato", outer_space=outer_space)
        space.execute(source="reference = 99")
        assert "x" not in outer_space

    def test_space_references_prioritized_over_user_namespace_indirectly(self):
        outer_space = dict(x=100)
        space = Space(name="tomato", outer_space=outer_space)
        space.execute(source="x = 99")
        space.execute(source="assert x == 99")
        assert space.namespace["x"] == 99

    def test_space_references_prioritized_over_user_namespace_directly(self):
        outer_space = dict(x=100)
        space = Space(name="tomato", outer_space=outer_space)
        space.namespace["x"] = 99
        space.execute(source="assert x == 99")
        assert space.namespace["x"] == 99

    def test_space_references_can_be_altered_indirectly(self):
        space = Space(name="tomato", outer_space={})
        space.execute(source="x = 99")
        space.execute(source="x = 101")
        space.execute(source="assert x == 101")
        assert space.namespace["x"] == 101

    def test_space_references_can_be_altered_directly(self):
        space = Space(name="tomato", outer_space={})
        space.execute(source="x = 99")
        reference_value = 101
        space.namespace["x"] = reference_value
        assert space.namespace["x"] == reference_value

    def test_space_references_can_be_deleted_indirectly(self):
        space = Space(name="tomato", outer_space={})
        space.execute(source="x = 99")
        space.execute(source="del x")
        assert "x" not in space.namespace

    def test_space_references_can_be_deleted_directly(self):
        space = Space(name="tomato", outer_space={})
        space.execute(source="x = 99")
        del space.namespace["x"]
        with raises(NameError):
            space.execute(source="x")
        assert "x" not in space.namespace

    def test_space_references_can_be_added_directly(self):
        space = Space(name="tomato", outer_space={})
        reference_value = 101
        space.namespace["x"] = reference_value
        space.execute(source="assert x == 101")
        assert space.namespace["x"] == reference_value

    def test_space_representation(self):
        space = Space(name="tomato", outer_space={})
        space.namespace["x"] = 1
        space.namespace["y"] = 1
        assert repr(space) == "Space(name=tomato, size=2)"

    def test_last_output_is_sent_to_stdout(self, capsys):
        space = Space(name="tomato", outer_space={})
        space.execute(source="1")
        assert capsys.readouterr().out == "1\n"

    def test_only_last_output_is_sent_to_stdout(self, capsys):
        space = Space(name="tomato", outer_space={})
        space.execute(source="1\n2")
        assert capsys.readouterr().out == "2\n"

    def test_none_does_not_produce_any_stdout(self, capsys):
        space = Space(name="tomato", outer_space={})
        space.execute(source="None")
        assert capsys.readouterr().out == ""

    def test_statement_does_not_produce_any_stdout(self, capsys):
        space = Space(name="tomato", outer_space={})
        space.execute(source="x = 1")
        assert capsys.readouterr().out == ""

    def test_use_variable_defined_in_same_source(self):
        space = Space(name="tomato", outer_space={})
        space.execute(source="x = 1; y = x + 1")
        assert space.namespace == {"x": 1, "y": 2}


class TestSpaceRegister:
    def test_get_new_space(self):
        space_register = SpaceRegister()
        space_name = "tomato"
        space = space_register.get_space(name=space_name, outer_space={})
        assert space.name == space_name

    def test_get_existing_space(self):
        space_register = SpaceRegister()
        space1 = space_register.get_space(name="tomato", outer_space={})
        space2 = space_register.get_space(name="tomato", outer_space={})
        assert space1 is space2

    def test_remove_existing_space(self):
        space_register = SpaceRegister()
        space_register.get_space(name="tomato", outer_space={})
        space = space_register.get_space(name="potato", outer_space={})
        space_register.remove_space(name="tomato")
        expected_register = dict(potato=space)
        assert space_register.register == expected_register

    def test_remove_non_existing_space(self):
        space_register = SpaceRegister()
        with raises(RegistryError):
            space_register.remove_space(name="tomato")

    def test_remove_all_spaces_given_non_empty_register(self):
        space_register = SpaceRegister()
        space_register.get_space(name="tomato", outer_space={})
        space_register.get_space(name="potato", outer_space={})
        space_register.remove_all_spaces()
        expected_register = {}
        assert space_register.register == expected_register

    def test_remove_all_spaces_given_empty_register(self):
        space_register = SpaceRegister()
        space_register.remove_all_spaces()
        expected_register = {}
        assert space_register.register == expected_register
