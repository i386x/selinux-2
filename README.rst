.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black
   :alt: Python Black Code Style

rpm
===

Pure-python rpm **shim** module for use in virtualenvs in order to avoid
failure to load rpm python bindings.

You still need to have rpm python bindings package installed on your
system for it to work but you no longer have the problem of not being able
to import it from inside isolated (default) virtualenvs.

