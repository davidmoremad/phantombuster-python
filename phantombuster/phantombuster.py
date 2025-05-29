# -*- coding: utf-8 -*-
import os
import json
import requests
from phantombuster.utils import RequestHandler

class PhantomBuster(object):
    
    BASE_URL = "https://api.phantombuster.com/api/v2/"

    ORG = "orgs/fetch"
    ORG_RESOURCES = "orgs/fetch-resources"

    # Scripts - Called Phantoms
    SCRIPTS = "scripts/fetch-all"
    SCRIPT = "script/fetch?id={}"
    # Agents - Run Phantoms
    AGENTS = "agents/fetch-all"
    AGENT = "agents/fetch?id={}"
    AGENT_OUTPUT = "agents/fetch-output?id={}"
    AGENT_LAUNCH = "agents/launch"
    AGENT_SAVE = "agents/save"
    # Containers - Execution results
    CONTAINERS = "containers/fetch-all?agentId={}"
    CONTAINER = "containers/fetch?id={}"
    CONTAINER_OUTPUT = "containers/fetch-output?id={}&raw={}"
    CONTAINER_RESULTS = "containers/fetch-result-object?id={}"


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

    # ------------------   Orgs   ------------------
    # --------------------------------------------------

    def fetch_org(self):
        """Fetch all organizations"""
        return self.req.get(self.ORG)
    
    def fetch_org_usage(self):
        """Fetch resources for the organization"""
        return self.req.get(self.ORG_RESOURCES)
    

    # ------------------   Scripts   ------------------
    # --------------------------------------------------
    def fetch_scripts(self, organizationName="phantombuster"):
        """Fetch all scripts (Phantoms)"""
        return self.req.get(f'{self.SCRIPTS}?org={organizationName}')
    
    def fetch_script(self, scriptId):
        """Fetch a specific script (Phantom) by ID
        Args:
            scriptId (str): Script ID to fetch
        """
        return self.req.get(self.SCRIPT.format(scriptId))
    

    # ------------------   Agents   ------------------
    # --------------------------------------------------
    def fetch_agents(self):
        """Fetch all agents"""
        return self.req.get(self.AGENTS)
    
    def fetch_agent(self, agentId):
        """Fetch a specific agent by ID
        Args:
            agentId (str): Agent ID to fetch
        """
        return self.req.get(self.AGENT.format(agentId))
    
    def fetch_agent_output(self, agentId):
        """Fetch the output of a specific agent by ID
        Args:
            agentId (str): Agent ID to fetch output for
        """
        return self.req.get(self.AGENT_OUTPUT.format(agentId))
    
    def launch_agent(self, agentId, arguments=None):
        """Launch a specific agent (run a Phantom)
        Args:
            agentId (str): Agent ID to launch
            arguments (dict): Optional arguments to send with the launch request.
        """
        if not arguments:
            arguments = {}

        if 'sessionCookie' not in arguments:
            # If sessionCookie is not provided, use the default one from the environment variable
            arguments['sessionCookie'] = os.getenv('PHANTOMBUSTER_COOKIE')

        payload = {
            'id': agentId,
            'arguments': arguments
        }

        return self.req.post(self.AGENT_LAUNCH, payload=payload)

    def save_agent(self, agentId, payload=None): 
        """Save a specific agent (update a Phantom)
        Args:
            agentId (str): Agent ID to save
            payload (dict): Optional payload to send with the save request
        """
        if not payload:
            payload = {}
        payload['id'] = agentId
        return self.req.post(self.AGENT_SAVE, payload=payload)

    # ------------------   Containers   ------------------
    # --------------------------------------------------
    
    def fetch_containers(self, agentId):
        """Fetch all containers for a specific agent
        Args:
            agentId (str): Agent ID to fetch containers for
        """
        return self.req.get(self.CONTAINERS.format(agentId))

    def fetch_container(self, containerId):
        """Fetch a specific container by ID
        Args:
            containerId (str): Container ID to fetch
        """
        return self.req.get(self.CONTAINER.format(containerId))
    
    def fetch_container_output(self, containerId, raw=False):
        """Fetch the output of a specific container by ID
        Args:
            containerId (str): Container ID to fetch output for
            raw (bool): If True, fetch raw output
        """
        return self.req.get(self.CONTAINER_OUTPUT.format(containerId, str(raw).lower()))
    
    def fetch_container_results(self, containerId):
        """Fetch the results of a specific container by ID
        Args:
            containerId (str): Container ID to fetch results for
        """
        return self.req.get(self.CONTAINER_RESULTS.format(containerId))