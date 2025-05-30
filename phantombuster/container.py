class Container(object):

    CONTAINERS = "containers/fetch-all?agentId={}"
    CONTAINER = "containers/fetch?id={}"
    CONTAINER_OUTPUT = "containers/fetch-output?id={}&raw={}"
    CONTAINER_RESULTS = "containers/fetch-result-object?id={}"

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
        """
        return self.req.get(self.CONTAINERS.format(agent_id))

    def get(self, container_id):
        """Fetch a specific container by ID
        Args:
            container_id (str): Container ID to fetch
        """
        return self.req.get(self.CONTAINER.format(container_id))
    
    def output(self, container_id, raw=False):
        """Fetch the output of a specific container by ID
        Args:
            container_id (str): Container ID to fetch output for
            raw (bool): If True, fetch raw output
        """
        return self.req.get(self.CONTAINER_OUTPUT.format(container_id, str(raw).lower()))
    
    def results(self, container_id):
        """Fetch the results of a specific container by ID
        Args:
            container_id (str): Container ID to fetch results for
        """
        return self.req.get(self.CONTAINER_RESULTS.format(container_id))