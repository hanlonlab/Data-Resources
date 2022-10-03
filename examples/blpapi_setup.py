#!/usr/bin/env python3
# coding: utf-8

import subprocess


def blpapi_dependency():
    r"""
    If importing the blpapi library fails, download it using python3's pip module.
    
    Note the blpapi requires the Bloomberg C++ SDK. On Windows, the SDK is installed by default with the Bloomberg Desktop software.
    """

    try:
        import blpapi
    except:
        blpapi_cmd = 'python3 -m pip install --user --index-url=https://bcms.bloomberg.com/pip/simple blpapi'
        subprocess.run([blpapi_cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def xbbg_dependency():
    r"""
    If importing the xbbg library fails, download it using python3's pip module.
    
    Note the xbbg requires both the blpapi and the Bloomberg C++ SDK. On Windows, the SDK is installed by default with the Bloomberg Desktop software.
    """

    try:
        from xbbg import blp
    except:
        xbbg_cmd = 'python3 -m pip install --user xbbg'
        subprocess.run([xbbg_cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def pandas_dependency():
    r"""
    If importing the pandas library fails, download it using python3's pip module.
    """

    try:
        import pandas as pd
    except:
        pandas_cmd = 'python3 -m pip install --user pandas'
        subprocess.run([pandas_cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def plotly_dependency():
    r"""
    If importing the plotly library fails, download it using python3's pip module.
    """

    try:
        import plotly
    except:
        plotly_cmd = 'python3 -m pip install --user pandas'
        subprocess.run([plotly_cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def other_dependency(lib: str):
    r"""
    If importing a module or library fails, download it using by name using python3's pip module. Note this pattern may not work for every importable object.

    :param lib: The module or library that should be available to python3
    :type lib: str
    """

    try:
        import_cmd = 'python3 -c "import {}"'.format(lib)
        subprocess.run([import_cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        pip_cmd = 'python3 -m pip install --user {}'.format(lib)
        subprocess.run([pip_cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == "__main__":

    # Download the library dependencies for the other scripts in this project
    blpapi_dependency()
    xbbg_dependency()
    pandas_dependency()
    plotly_dependency()
