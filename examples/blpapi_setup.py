#!/usr/bin/env python3
# coding: utf-8

import sys
import subprocess


def blpapi_dependency():
    r"""
    If importing the blpapi library fails, download it using python3's pip module.
    
    Note the blpapi requires the Bloomberg C++ SDK. On Windows, the SDK is installed by default with the Bloomberg Desktop software.
    """

    try:
        import blpapi
    except:
        cmd_args = [sys.executable,'-m','pip','install','--user','--index-url=https://bcms.bloomberg.com/pip/simple','blpapi']
        subprocess.run(cmd_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def xbbg_dependency():
    r"""
    If importing the xbbg library fails, download it using python3's pip module.
    
    Note the xbbg requires both the blpapi and the Bloomberg C++ SDK. On Windows, the SDK is installed by default with the Bloomberg Desktop software.
    """

    try:
        from xbbg import blp
    except:
        cmd_args = [sys.executable,'-m','pip','install','--user','xbbg']
        subprocess.run(cmd_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def pandas_dependency():
    r"""
    If importing the pandas library fails, download it using python3's pip module.
    """

    try:
        import pandas as pd
    except:
        cmd_args = [sys.executable,'-m','pip','install','--user','pandas']
        subprocess.run(cmd_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def other_dependency(lib: str):
    r"""
    If importing a module or library fails, download it using by name using python3's pip module. Note this pattern may not work for every importable object.

    :param lib: The module or library that should be available to python3
    :type lib: str
    """

    try:
        import_cmd_args = [sys.executable,'-c','import {}'.format(lib)]
        subprocess.run([import_cmd_args], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        cmd_args = [sys.executable,'-m','pip','install','--user',lib]
        subprocess.run(cmd_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == "__main__":

    # Download the library dependencies for the other scripts in this project
    blpapi_dependency()
    xbbg_dependency()
    pandas_dependency()
