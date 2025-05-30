# -*- coding: utf-8 -*-
from .utils import RequestHandler
from phantombuster.org import Org
from phantombuster.script import Script
from phantombuster.agent import Agent
from phantombuster.container import Container

class PhantomBuster(object):
    """
    PhantomBuster API client for interacting with PhantomBuster services.
    This class provides methods to manage scripts, agents, and organizations
    using the PhantomBuster API.
    Attributes:
        apikey (str): PhantomBuster API key
        headers (dict): Headers for API requests
        org (Org): Organization management interface
        script (Script): Script management interface
        agent (Agent): Agent management interface
        container (Container): Container management interface
    """

    BASE_URL = "https://api.phantombuster.com/api/v2/"

    def __init__(self, api_key: str):
        """Initialize PhantomBuster API client
        Args:
            api_key (str): PhantomBuster API key
        """
        if not api_key:
            raise ValueError("API key is required")
        
        self._api_key = api_key
        self._headers = {
            "X-Phantombuster-Key-1": self._api_key,
            "Content-Type": "application/json"
        }
        self._req = RequestHandler(endpoint=self.BASE_URL, headers=self._headers)

        self.org = Org(self._req)
        self.script = Script(self._req)
        self.agent = Agent(self._req)
        self.container = Container(self._req)