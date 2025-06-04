# PhantomBuster Python SDK

[![Documentation](https://img.shields.io/badge/docs-readthedocs-blue.svg)](https://phantombuster-python.readthedocs.io/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

---

# Installation

```bash
pip install pbuster
```
**📚 Documentation**: Will be available at readthedocs.io

---

# Usage

Authenticate by setting the environment variables `PHANTOMBUSTER_ORG_ID` and `PHANTOMBUSTER_API_KEY`:

```python
pb = PhantomBuster()
pb.agents.list()
```

Or by passing you API key directly in the code:
```python
from phantombuster import PhantomBuster

pb = PhantomBuster(apikey=API_KEY, orgId=ORG_ID)
pb.agents.list()
```

---

# Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

---

# License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.