from setuptools import setup

# https://python-packaging.readthedocs.io/en/latest/minimal.html
setup(
    author="Radon Rosborough",
    author_email="radon.neon@gmail.com",
    description="Bidirectional sparse-tree directory mirroring.",
    license="MIT",
    install_requires=["paramiko", "sshpubkeys"],
    name="madeline",
    scripts=["madeline"],
    url="https://github.com/raxod502/madeline",
    version="1.0.2",
)
