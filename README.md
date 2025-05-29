# PhantomBuster Python SDK

This is a Python package that provides functionality to process LinkedIn and email inputs.



# Installation

```bash
cd /path/to/phantombuster-python
pip install .
```
**📚 Documentation**: Will be available at readthedocs.io


# Usage

There are two ways to authenticate:

By passing you API key directly in the code:
```python
from phantombuster import PhantomBuster

pb = PhantomBuster(apikey=API_KEY, orgId=ORG_ID)
pb.fetch_agents()
```

Or by setting the environment variables `PHANTOMBUSTER_ORG_ID` and `PHANTOMBUSTER_API_KEY`:

```python
pb = PhantomBuster()
pb.fetch_agents()
```

---

# Explaining PhantomBuster API

PhantomBuster provides a powerful API to interact with its services. The SDK allows you to easily fetch agents, process LinkedIn profiles, and handle email inputs.

### Organization

> When you sign up for an account on Phantombuster, an <ins>org</ins> is automatically created for you. It contains the agents you'll use and the scripts you'll code. Your org contains your catalog of Phantoms

> A <ins>Phantom</ins> is a term intended for non-technical users which designates both a script (which is listed in an org's catalog) and an agent (which is an "instance of a script" listed in an org's dashboard). When developing on the Phantombuster platform, we recommend not using this term as it conflates both concepts.
> Phantoms handle all your scraping and automation. They are actually made of:
>   - a <ins>script</ins>: to define the navigation scenario and the data to retrieve
>   - an <ins>agent</ins>: it is a configured "instance" of its associated script
>   - a <ins>setup</ins>: to configure your agent schedule execution, notifications, etc.


### Scripts

Scripts are the source code that defines the behavior of a Phantom. They are executed by NodeJs and define the navigation scenario and the data to retrieve.

### Agents

An agent is an "instance of a script". It can be configured through its setup. An org's agents are listed in its dashboard. Every agent has its own page, where you can see details about the previous launches, debug your script live and so on... 

### Container

A container is a virtual environment asociated to a specific agent where the script is executed. It provides the necessary resources and isolation for the script to run.

---

# Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

# License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.