import pytest
from IPython.testing.globalipapp import start_ipython


@pytest.fixture(scope="session")
def session_ip():
    return start_ipython()


@pytest.fixture(scope="function")
def ip(session_ip):
    session_ip.run_line_magic(magic_name="load_ext", line="jupyter_spaces")
    yield session_ip
    session_ip.run_line_magic(magic_name="unload_ext", line="jupyter_spaces")
    session_ip.run_line_magic(magic_name="reset", line="-f")
