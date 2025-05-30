import os

class Agent(object):

    AGENTS = "agents/fetch-all"
    AGENT = "agents/fetch?id={}"
    AGENT_OUTPUT = "agents/fetch-output?id={}"
    AGENT_LAUNCH = "agents/launch"
    AGENT_SAVE = "agents/save"
    AGENT_DELETE = "agents/delete"

    def __init__(self, req):
      self.req = req


    def list(self):
        """Fetch all agents"""
        return self.req.get(self.AGENTS)

    def get(self, agent_id):
        """Fetch a specific agent by ID"""
        return self.req.get(self.AGENT.format(agent_id))

    def output(self, agent_id):
        """Fetch the output of a specific agent by ID
        Args:
            agent_id (str): Agent ID to fetch output for
        """
        return self.req.get(self.AGENT_OUTPUT.format(agent_id))
    
    def run(self, agent_id, arguments=None):
        """Launch a specific agent (run a Phantom)
        Args:
            agent_id (str): Agent ID to launch
            arguments (dict): Optional arguments to send with the launch request.
        """
        if not arguments:
            arguments = {}

        if 'sessionCookie' not in arguments:
            # If sessionCookie is not provided, use the default one from the environment variable
            arguments['sessionCookie'] = os.getenv('PHANTOMBUSTER_COOKIE')

        payload = {
            'id': agent_id,
            'arguments': arguments
        }

        return self.req.post(self.AGENT_LAUNCH, payload=payload)

    def create(self, agent_id=None, organizationName="phantombuster", scriptName=None, agentName=None):
        """Save a specific agent (update a Phantom)
        Args:
            agent_id (str): Agent ID to save
            payload (dict): Optional payload to send with the save request
        """
        payload = {}
        if agent_id:
            payload['id'] = agent_id
        if organizationName:
            payload['org'] = organizationName
        if scriptName:
            payload['script'] = scriptName
        if agentName:
            payload['name'] = agentName

        return self.req.post(self.AGENT_SAVE, payload=payload)

    def update(self, agent_id=None, organizationName="phantombuster", scriptName=None, agentName=None):
        """Save a specific agent (update a Phantom)
        Args:
            agent_id (str): Agent ID to save
            payload (dict): Optional payload to send with the save request
        """
        payload = {}
        if agent_id:
            payload['id'] = agent_id
        if organizationName:
            payload['org'] = organizationName
        if scriptName:
            payload['script'] = scriptName
        if agentName:
            payload['name'] = agentName

        return self.req.post(self.AGENT_SAVE, payload=payload)
    
    def delete(self, agent_id):
        """Delete a specific agent by ID
        Args:
            agent_id (str): Agent ID to delete
        """
        return self.req.post(self.AGENT_DELETE, payload={'id': agent_id})