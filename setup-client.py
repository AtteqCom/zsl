from setuptools import setup, find_packages

EXCLUDE_FROM_PACKAGES = ['client', 'client.*']

setup(name='asl-client',
      version='1.0',
      description='Atteq service layer',
      author='Atteq, s.r.o.',
      author_email='opensource@atteq.com',
      url='https://github.com/atteq/zsl',
      packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES))

