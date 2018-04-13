from IPython.testing.globalipapp import start_ipython
import pytest


@pytest.fixture(scope='session')
def global_ip():
    return start_ipython()


@pytest.fixture(scope='function')
def ip(global_ip):
    global_ip.run_line_magic(magic_name='reset', line='-f')
    global_ip.run_line_magic(magic_name='load_ext', line='jupyter_spaces')
    yield global_ip
    global_ip.run_line_magic(magic_name='unload_ext', line='jupyter_spaces')
