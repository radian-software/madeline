from setuptools import setup

# https://python-packaging.readthedocs.io/en/latest/minimal.html
setup(
    author="Radian LLC",
    author_email="contact+madeline@radian.codes",
    description="Bidirectional sparse-tree directory mirroring.",
    license="MIT",
    install_requires=["paramiko", "sshpubkeys"],
    name="madeline",
    scripts=["madeline"],
    url="https://github.com/radian-software/madeline",
    version="1.0.2",
)
