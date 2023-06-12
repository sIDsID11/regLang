import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='regLang',
    version='0.1',
    author='Simon Dorer',
    description='Python implementation for FAs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sIDsID11/regLang',
    project_urls={
        "Bug Tracker": "https://github.com/sIDsID11/regLang/Issues"
    },
    license='MIT',
    packages=['regLang'],
    install_requires=[],
)