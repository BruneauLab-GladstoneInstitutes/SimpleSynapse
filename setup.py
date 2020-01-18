from setuptools import setup

setup(name='simpleSynapse',
      version='0.1',
      description='A simple Synapse organization and maintenance python client script',
      url='https://github.com/BruneauLab-GladstoneInstitutes/simpleSynapse',
      author='Andrew Blair',
      author_email='andrew.blair@gladstone.ucsf.edu',
      license='MIT',
      scripts=['simpleSynapse.py'],
      install_requires=[
          'synapseclient',
      ],
      zip_safe=False)