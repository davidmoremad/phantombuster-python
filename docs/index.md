# Getting started

[![PhantomBuster API Documentation](https://img.shields.io/badge/API%20Reference-PhantomBuster-blue.svg)](https://hub.phantombuster.com/reference/get_orgs-export-agent-usage-1)  

---

## Installation

```bash
pip install pbuster
```

---


## Usage

```python
from pbuster import PhantomBuster
pb = PhantomBuster("YOUR_API_KEY")

# Get your agents
agents = pb.agents.list()

# Print the names and IDs of your agents
for agent in agents:
    print(f'Agent {agent.get("name")} has ID {agent.get("id")}')
```

---

## Documentation

* [Organizations](organizations.md)
* [Agents](agents.md)
* [Scripts](scripts.md)
* [Containers](containers.md)
