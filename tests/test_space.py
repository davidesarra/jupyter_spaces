import pytest

from jupyter_spaces.errors import RegistryError
from jupyter_spaces.space import Space, SpaceRegister


class TestSpace:

    def test_space_has_correct_name(self):
        space_name = 'tomato'
        space = Space(name=space_name, outer_space=locals())
        assert space.name == space_name

    def test_space_can_access_user_namespace_references(self):
        outer_reference = 100
        space = Space(name='tomato', outer_space=locals())
        space.execute(source='assert outer_reference == 100')

    def test_space_cannot_alter_user_namespace_references(self):
        reference = 100
        space = Space(name='tomato', outer_space=locals())
        space.execute(source='reference = 99')
        assert reference == 100

    def test_space_cannot_remove_user_namespace_references(self):
        reference = 100
        space = Space(name='tomato', outer_space=locals())
        with pytest.raises(NameError):
            space.execute(source='del reference')
        assert reference == 100

    def test_space_cannot_add_user_namespace_references(self):
        space = Space(name='tomato', outer_space=locals())
        space.execute(source='reference = 99')
        with pytest.raises(NameError):
            reference

    def test_space_references_prioritised_over_user_namespace_indirectly(self):
        reference = 100
        space = Space(name='tomato', outer_space=locals())
        space.execute(source='reference = 99')
        space.execute(source='assert reference == 99')
        assert space.namespace['reference'] == 99

    def test_space_references_prioritised_over_user_namespace_directly(self):
        reference = 100
        space = Space(name='tomato', outer_space=locals())
        space.execute(source='reference = 99')
        assert space.namespace['reference'] == 99

    def test_space_references_can_be_altered_indirectly(self):
        space = Space(name='tomato', outer_space=locals())
        space.execute(source='reference = 99')
        space.execute(source='reference = 101')
        space.execute(source='assert reference == 101')
        assert space.namespace['reference'] == 101

    def test_space_references_can_be_altered_directly(self):
        space = Space(name='tomato', outer_space=locals())
        space.execute(source='reference = 99')
        reference_value = 101
        space.namespace['reference'] = reference_value
        assert space.namespace['reference'] == reference_value

    def test_space_references_can_be_deleted_indirectly(self):
        space = Space(name='tomato', outer_space=locals())
        space.execute(source='reference = 99')
        space.execute(source='del reference')
        with pytest.raises(NameError):
            space.execute(source='reference')
        with pytest.raises(KeyError):
            space.namespace['reference']

    def test_space_references_can_be_deleted_directly(self):
        space = Space(name='tomato', outer_space=locals())
        space.execute(source='reference = 99')
        del space.namespace['reference']
        with pytest.raises(NameError):
            space.execute(source='reference')
        with pytest.raises(KeyError):
            space.namespace['reference']

    def test_space_references_can_be_added_directly(self):
        space = Space(name='tomato', outer_space=locals())
        reference_value = 101
        space.namespace['reference'] = reference_value
        space.execute(source='assert reference == 101')
        assert space.namespace['reference'] == reference_value


class TestSpaceRegister:

    def test_get_new_space(self):
        space_register = SpaceRegister()
        space_name = 'tomato'
        space = space_register.get_space(name=space_name, outer_space=locals())
        assert space.name == space_name

    def test_get_existing_space(self):
        space_register = SpaceRegister()
        space1 = space_register.get_space(name='tomato', outer_space=locals())
        space2 = space_register.get_space(name='tomato', outer_space=locals())
        assert space1 is space2

    def test_remove_existing_space(self):
        space_register = SpaceRegister()
        _ = space_register.get_space(name='tomato', outer_space=locals())
        space = space_register.get_space(name='potato', outer_space=locals())
        space_register.remove_space(name='tomato')
        expected_register = dict(potato=space)
        assert space_register.register == expected_register

    def test_remove_non_existing_space(self):
        space_register = SpaceRegister()
        with pytest.raises(RegistryError):
            space_register.remove_space(name='tomato')

    def test_remove_all_spaces_given_non_empty_register(self):
        space_register = SpaceRegister()
        _ = space_register.get_space(name='tomato', outer_space=locals())
        _ = space_register.get_space(name='potato', outer_space=locals())
        space_register.remove_all_spaces()
        expected_register = {}
        assert space_register.register == expected_register

    def test_remove_all_spaces_given_empty_register(self):
        space_register = SpaceRegister()
        space_register.remove_all_spaces()
        expected_register = {}
        assert space_register.register == expected_register
