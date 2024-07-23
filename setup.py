#!/usr/bin/env python

from setuptools import setup

REQUIRES = []


def read_requirements(file):
    with open(file) as f:
        for line in f:
            line, _, _ = line.partition('#')
            line = line.strip()
            if ';' in line:
                requirement, _, specifier = line.partition(';')
                for_specifier = EXTRAS.setdefault(':{}'.format(specifier), [])
                for_specifier.append(requirement)
            else:
                REQUIRES.append(line)


read_requirements('requirements.txt')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='fmo-tool',
      version='0.1',
      license='Apache-2.0',
      description='FMO-OS configuraiton and managment tool',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/tiiuae/fmo-tool',
      keywords=['fmo-os', 'fmo-tool', 'cli'],
      packages=['fmotool', 'apps', 'utils'],
      python_requires='>=3.7',
      install_requires=REQUIRES,
      entry_points={
          'console_scripts': [
              'fmo-tool=fmotool.__main__:main'
          ],
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Topic :: System :: Managment',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
      ],
      )
