# simpleSynapse

[Synapse](https://www.synapse.org/) is an open source software platform for researchers to coordinate projects and freely store their data. simpleSynapse is a Python API that allows data scientists to organize and sync data.

# Requirements


# Installation

```bash
pip install simpleSynapse
```

# Usage

```python
import simpleSynapse

simpleSynapse.push(<username>, <password>, <project>)
simpleSynapse.pull(<username>, <password>, <project>)
```

Acknowledgements and thanks extend to Sage Bionetworks for developing the Synapse Python client, for which without SimpleSynapse would be much less simple.



