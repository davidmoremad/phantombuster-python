# -*- coding: utf-8 -*-
import json
import time

class Container(object):

    CONTAINERS = "containers/fetch-all?agentId={}"
    CONTAINER = "containers/fetch?id={}&withResultObject=2&withOutput=true&withRuntimeEvents=true&withNewerAndOlderContainerId=false"
    CONTAINER_OUTPUT = "containers/fetch-output?id={}&raw={}"
    CONTAINER_RESULTS = "containers/fetch-result-object?id={}"

    WAIT_TIME = 2  # seconds

    def __init__(self, req):
        """Initialize Container API client
        
        Args:
            req (RequestHandler): Request handler instance for making API requests
        """
        self.req = req
    
    
    def list(self, agent_id):
        """Fetch all containers for a specific agent
        
        Args:
            agent_id (str): Agent ID to fetch containers for
        
        Returns:
            (dict): A dictionary containing all containers for the specified agent.
        """
        return self.req.get(self.CONTAINERS.format(agent_id))['containers']

    def get(self, container_id):
        """Fetch a specific container by ID with results and output
        
        Args:
            container_id (str): Container ID to fetch
        
        Returns:
            (dict): A dictionary containing the container details.
        """
        return self.req.get(self.CONTAINER.format(container_id))
    
    def output(self, container_id, raw=False):
        """Fetch the output of a specific container by ID
        
        Args:
            container_id (str): Container ID to fetch output for
            raw (bool): If True, fetch raw output
        
        Returns:
            (dict): A dictionary containing the container's output.
        """
        return self.req.get(self.CONTAINER_OUTPUT.format(container_id, str(raw).lower()))['output']
    
    def results(self, container_id):
        """Fetch the results of a specific container by ID
        
        Args:
            container_id (str): Container ID to fetch results for
        
        Returns:
            (dict): A dictionary containing the container's results.
        """
        rsp = self.req.get(self.CONTAINER_RESULTS.format(container_id))
        try:
            if not rsp.get('resultObject'):
                return {}
            else:
                return json.loads(rsp.get('resultObject', {})).pop()
        except json.JSONDecodeError:
            return rsp

    def wait(self, container_id):
        """Wait for completion of a specific container by ID

        Args:
            container_id (str): Container ID to wait for

        Returns:
            (dict): A dictionary containing the container's output after it has finished executing.
        """
        container = self.get(container_id)
        exitCode = container.get('exitCode', None)
        status = container.get('status')

        # [!] Checking exitCode instead of status because
        #     it changes to 'finished' before the container is actually done.
        while exitCode is None or status == "running":
            container = self.get(container_id)
            exitCode = container.get('exitCode')
            status = container.get('status')
            time.sleep(self.WAIT_TIME)

        return container