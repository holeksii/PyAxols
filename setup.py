from distutils.core import setup

setup(
    name="PyAxols",
    version="1.0",
    description="Python Axolotl, simple library for data manipulation and analysis",
    author="Oleksii Hytsiv",
    author_email="oleksii.hytsiv@gmail.com",
    url="https://github.com/holeksii/PyAxols/blob/master/README.md",
    packages=[
        "pyaxols",
        "pyaxols.aio",
        "pyaxols.aio.csv",
        "pyaxols.aio.json",
        "pyaxols.aio.xml",
        "pyaxols.atypes",
        "pyaxols.atypes.seq",
        "pyaxols.atypes.table",
    ],
)
