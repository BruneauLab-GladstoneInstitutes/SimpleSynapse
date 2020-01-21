# simpleSynapse

[Synapse](https://www.synapse.org/) is an open source software platform for researchers to coordinate projects and freely store their data. simpleSynapse is a Python API and CLI that allows data scientists to simply organize, version control, and share data.

# Requirements
* [Be a registered Synapse user](https://www.synapse.org/#!RegisterAccount:0), however, only [certified users](https://docs.synapse.org/articles/accounts_certified_users_and_profile_validation.html) can upload files/tables and add provenance tracking
* Create a [Synapse project](https://docs.synapse.org/articles/making_a_project.html)
* Python 3

# Installation

```bash
pip install simpleSynapse
```

# Usage

simpleSynapse either **pulls** data from Synapse or **pushes** data to Synapse. 

### Pull
A simpleSynapse data **pull** downloads the most recently uploaded files without overwriting local updates. A first time project **pull** will create a local folder, with the name of the project, to store the data. Users can either use simpleSynapse or the Synapse GUI to create new folders.

### Push
A simpleSynapse data **push** will only upload new files/folders or files that have had their content changed. The latter case will create a new file version on Synapse that by default will be the most recent upload ready for a **pull**. 

## Python
```python
import simpleSynapse

simpleSynapse.push(<username>, <password>, <project>)
simpleSynapse.pull(<username>, <password>, <project>)
```

## Command Line Interface
```bash
simpleSynapsePush --username <username> --password <password> --project <project>
simpleSynapsePull --username <username> --password <password> --project <project>
```

# Tutorial

Acknowledgements and thanks extend to Sage Bionetworks for developing the Synapse Python client, for which without SimpleSynapse would be much less simple.
