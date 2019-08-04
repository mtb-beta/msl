from setuptools import setup

entry_points = {
    'console_scripts': ['msl = msl.console:main']
}

setup(
    name='msl',
    version='0.3.0',
    description='My Standard Library',
    author='Tatsuya Matoba',
    author_email='tatsuya.matoa.wk.jp@gmail.com',
    packages = ['msl'],
    include_package_data=True,
    entry_points=entry_points,
    install_requires=['colorama', 'GitPython', 'markdown', 'jinja2'],
)
