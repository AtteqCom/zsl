import sys

from setuptools import find_packages, setup

_is_py3 = sys.version_info > (3, 0)

requirements = [
    'flask',
    'future',
    'injector==0.12.1',
    'requests>=2.7',
    'SQLAlchemy>=1',
    'typing>=3.5',
    'Werkzeug>=0.12',
]

if sys.version_info < (3, 0):
    requirements.append('enum34')

setup(name='zsl',
      version='0.19.0',
      description='zsl application framework for web based services',
      author='Atteq s.r.o.',
      author_email='open.source@atteq.com',
      url='https://github.com/AtteqCom/zsl',
      license='MIT',
      package_dir={'': 'src'},
      install_requires=requirements,
      extras_require={
          'cli': ['bpython'],
          'redis': ['redis>=2.10'],
          'celery': ['zsl_client'],
          'gearman': ['zsl_client', 'gearman'],
          'alembic': ['alembic'],
          'sentry': ['raven'],
          'documentation': ['sphinx', 'recommonmark', 'sphinx_rtd_theme',
                            'alembic']
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Application Frameworks'
      ],
      packages=find_packages('src'))
