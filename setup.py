import os

from setuptools import setup


setup(name='pyhearts',
       author_email='acomfygeek@gmail.com',
      version='0.1.0',
      packages=['pyhearts'],
      package_data={'pyhearts' : ['conf/*.cfg']},
#      scripts=['bin/runHearts.sh'],
#      install_requires=[
#                        ]
      )
