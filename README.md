# simpleSynapse

[Synapse](https://www.synapse.org/) is an open source software platform for researchers to coordinate projects and freely store their data. simpleSynapse is a Python API and CLI that allows data scientists to simply organize and sync data.

# Requirements
* [Be a registered Synapse user](https://www.synapse.org/#!RegisterAccount:0), however, only [certified users](https://docs.synapse.org/articles/accounts_certified_users_and_profile_validation.html) can upload files/tables and add provenance tracking
* Create a [Synapse project](https://docs.synapse.org/articles/making_a_project.html)
* Python 3

# Installation

```bash
pip install simpleSynapse
```

# Usage

## Python
```python
import simpleSynapse

simpleSynapse.push(<username>, <password>, <project>)
simpleSynapse.pull(<username>, <password>, <project>)
```

## Command line interface
```bash
simpleSynapsePush --username <username> --password <password> --project <project>
simpleSynapsePull --username <username> --password <password> --project <project>
```

Acknowledgements and thanks extend to Sage Bionetworks for developing the Synapse Python client, for which without SimpleSynapse would be much less simple.



