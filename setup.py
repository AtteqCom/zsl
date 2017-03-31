from setuptools import setup, find_packages

EXCLUDE_FROM_PACKAGES = ['tests', 'tests.*']

setup(name='zsl',
      version='0.11.0',
      description='zsl application framework for web based services',
      author='Atteq s.r.o.',
      author_email='open.source@atteq.com',
      url='https://github.com/AtteqCom/zsl',
      license='MIT',
      install_requires=[
        'injector',
        'flask',
        'flask_injector',
        'future'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 2.7',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Application Frameworks'
      ],
      packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES))
