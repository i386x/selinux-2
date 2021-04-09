# -*- coding: utf-8 -*-

"""That is shim pure-python module that detects and loads the original rpm
package from outside the current virtualenv, avoiding a very common error
inside virtualenvs: ModuleNotFoundError: No module named 'rpm'
"""

__author__ = """Sorin Sbarnea"""
__email__ = "sorin.sbarnea@gmail.com"
__version__ = "0.1.4"

import importlib
import json
import os
import platform
import subprocess
import sys


class add_path(object):
    """Context manager for adding path to sys.path"""

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            sys.path.remove(self.path)
        except ValueError:
            pass


def add_location(location):
    """Try to add a possible location for the rpm module"""
    if os.path.isdir(os.path.join(location, "rpm")):
        with add_path(location):
            # And now we replace outselves with the original rpm module
            importlib.reload(sys.modules["rpm"])
            return True
    return False


def get_system_sitepackages():
    """Get sitepackage locations from system python"""
    # Do not ever use sys.executable here
    # See https://github.com/pycontribs/selinux/issues/17 for details
    system_python = "/usr/bin/python%s" % platform.python_version_tuple()[0]

    system_sitepackages = json.loads(
        subprocess.check_output(
            [
                system_python,
                "-c",
                "import json, site; print(json.dumps(site.getsitepackages()))",
            ]
        ).decode("utf-8")
    )
    return system_sitepackages


def check_system_sitepackages():
    """Try add rpm module from any of the python site-packages"""

    success = False
    system_sitepackages = get_system_sitepackages()
    for candidate in system_sitepackages:
        success = add_location(candidate)
        if success:
            break

    if not success:
        raise Exception(
            "Failed to detect rpm python bindings at %s" % system_sitepackages
        )

check_system_sitepackages()
