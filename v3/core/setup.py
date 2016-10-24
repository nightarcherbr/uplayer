from setuptools import setup, find_packages;

setup(
  name="uplayer_core",
  version=0.1,
  url="https://github.com/nightarcherbr/uplayer/",
  author="Fabio Prodoccini",
  author_email="prodoccini@gmail.com",
  packages=find_packages(),
  install_require=["promise"],
  test_suite='tests',
  tests_require=['nose']
);