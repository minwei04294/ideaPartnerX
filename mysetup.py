from cx_Freeze import setup, Executable
import os
import py2exe

setup(
    name = "SmokeTest",
    version = "1",
    description = "SmokeTest",
    executables = [Executable("runSmoke.py")])
