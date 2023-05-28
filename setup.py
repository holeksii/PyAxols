from distutils.core import setup

setup(
    name="PyAxols",
    version="1.0",
    description="Python Axolotl, simple library for data manipulation and analysis",
    author="Oleksii Hytsiv",
    author_email="oleksii.hytsiv@gmail.com",
    url="https://github.com/holeksii/PyAxols/blob/master/README.md",
    packages=[
        "aio",
        "aio.csv",
        "aio.json",
        "aio.xml",
        "atypes",
        "atypes.seq",
        "atypes.table",
    ],
)
