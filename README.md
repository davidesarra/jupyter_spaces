# Jupyter Spaces

[![Build Status](https://travis-ci.org/davidesarra/jupyter_spaces.svg?branch=master)](https://travis-ci.org/davidesarra/jupyter_spaces)
[![codecov](https://codecov.io/gh/davidesarra/jupyter_spaces/branch/master/graph/badge.svg)](https://codecov.io/gh/davidesarra/jupyter_spaces)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/jupyter_spaces.svg)](https://pypi.org/project/jupyter_spaces/)

Jupyter Spaces is an IPython extension for creating parallel namespaces
available within the user namespace. It is designed to be used via IPython
magics in Jupyter notebooks.

## Installation

```bash
pip install jupyter_spaces
```

`jupyter_spaces` supports Python versions `3.4`, `3.5` and `3.6`.

## Usage

### Load `jupyter_spaces` extension

```python
%load_ext jupyter_spaces
```

### Reload `jupyter_spaces` extension

```python
%reload_ext jupyter_spaces
```

Reloading the extension will remove all spaces.

### Run a cell within a space

```python
%%space <space-name>
alpha = 0.50
print(alpha)
```

When you execute a cell within a space, all references are firstly searched in
the space namespace and secondly in the user namespace. All assignments are
made in the space namespace.

Trying to delete a user namespace reference will raise an error. Trying to
affect a user namespace reference using the keyword `global` will produce an
execution equivalent to not using such keyword.

Mutable objects in the user namespace can be altered (e.g. appending an item
to a list).

#### Console output

Conversely to the standard usage of the python console, the `print` function is
required to get a output in the console or in the Jupyter cell output.

- No output to console
    ```python
    %%space <space-name>
    100
    ```
- Output to console
    ```python
    %%space <space-name>
    print(100)
    ```

### Remove a space

```python
%remove_space <space-name>
```

### Access all spaces at once

You can access all the spaces' namespaces at once without using any magic.
This might be useful to jointly post-process or compare the spaces' contents.

```python
from jupyter_spaces import get_spaces

spaces = get_spaces()
space = spaces[<space-name>]
reference = space.namespace[<reference-name>]
```

`Space` objects have two properties:

- `name` the name of the space
- `namespace` a dictionary with the namespace of the space

Modifying the spaces via `get_spaces` will actually modify the underlying
spaces.

## Acknowledgements

Many thanks to [Yeray Diaz Diaz](https://github.com/yeraydiazdiaz) and
[Karol Duleba](https://github.com/mrfuxi)!
