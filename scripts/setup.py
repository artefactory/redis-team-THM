from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'thm_cli_arxiv',
    version = '1.0.0',
    author = 'Michel Hua',
    author_email = 'michel.hua@artefact.com',
    license = 'MIT',
    description = 'The ultimate CLI tool to help researchers and technical writers',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/artefactory-fr/redis-team-THM',
    py_modules = ['thm_cli', 'helpers', 'models'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        cooltool=thm_cli:start
    '''
)
