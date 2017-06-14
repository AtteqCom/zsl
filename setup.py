import re
import ast
import sys
from setuptools import setup, find_packages

EXCLUDE_FROM_PACKAGES = ['tests', 'tests.*']

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('zsl/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

_is_py3 = sys.version_info > (3, 0)

requirements = [
    'future',
    'Flask-Injector>=0.8' if _is_py3 else 'Flask-Injector==0.8.0',
    'requests>=2.7',
    'SQLAlchemy>=1',
    'typing>=3.5',
    'Werkzeug>=0.12',
]

if sys.version_info < (3, 4):
    requirements.append('enum34')

setup(name='zsl',
      version=version,
      description='zsl application framework for web based services',
      author='Atteq s.r.o.',
      author_email='open.source@atteq.com',
      url='https://github.com/AtteqCom/zsl',
      license='MIT',
      install_requires=requirements,
      extras_require={
          'cli': ['bpython'],
          'redis': ['redis>=2.10'],
          'celery': ['zsl_client'],
          'gearman': ['zsl_client', 'gearman'],
          'alembic': ['alembic'],
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
      packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES))
