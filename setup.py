from setuptools import setup

setup(name='simpleSynapse',
      version='0.4',
      description='A simple Synapse organization and maintenance python client program',
      url='https://github.com/BruneauLab-GladstoneInstitutes/simpleSynapse',
      author='Andrew Blair',
      author_email='andrew.blair@gladstone.ucsf.edu',
      license='MIT',
      packages=['simpleSynapse'],
      install_requires=['synapseclient'],
      entry_points={'console_scripts':
      ['simpleSynapsePull=simpleSynapse.pull:main', 'simpleSynapsePush=simpleSynapse.push:main']
      },
      zip_safe=False)