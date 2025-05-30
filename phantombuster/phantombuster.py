# -*- coding: utf-8 -*-
import os
from .utils import RequestHandler
from phantombuster.org import Org
from phantombuster.script import Script
from phantombuster.agent import Agent
from phantombuster.container import Container

class PhantomBuster(object):
    
    BASE_URL = "https://api.phantombuster.com/api/v2/"

    def __init__(self, apikey, orgId=None):
        """Initialize PhantomBuster API client
        Args:
            apikey (str): PhantomBuster API key
            orgId (str): Organization ID to use for the API requests
        """
        self.apikey = apikey
        self.headers = {
            "X-Phantombuster-Key-1": self.apikey,
            "Content-Type": "application/json"
        }
        self.req = RequestHandler(endpoint=self.BASE_URL, headers=self.headers)
        self.org = Org(self.req)
        self.script = Script(self.req)
        self.agent = Agent(self.req)
        self.container = Container(self.req)
