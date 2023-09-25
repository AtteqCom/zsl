import sys

from setuptools import find_packages, setup

requirements = [
    'flask>=1.1,<1.2',
    'future',
    'injector==0.12.1',
    'requests>=2.22',
    'SQLAlchemy>=1.3',
    'typing>=3.7',
    'Werkzeug>=0.15,<0.17',
    'markupsafe==2.0.1',
]

if sys.version_info < (3, 0):
    requirements.extend(['enum34',
                         'gearman==2.0.2',
                         ])
else:
    requirements.extend(['python3_gearman'])


setup(name='zsl',
      version='0.30.0',
      description='zsl application framework for web based services',
      long_description='Combines SQLAlchemy, flask swagger and others.',
      long_description_content_type='text/x-rst',
      author='Atteq s.r.o.',
      author_email='open.source@atteq.com',
      url='https://github.com/AtteqCom/zsl',
      license='MIT',
      package_dir={'': 'src'},
      install_requires=requirements,
      extras_require={
          'cli': ['bpython', 'click>=7.0'],
          'redis': ['redis>=3.2.0'],
          'celery': ['zsl_client'],
          'gearman': ['zsl_client'],
          'alembic': ['alembic'],
          'sentry': ['sentry-sdk[flask]'],
          'documentation': ['sphinx', 'recommonmark', 'sphinx_rtd_theme',
                            'alembic']
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Application Frameworks'
      ],
      packages=find_packages('src'))
