# -*- coding: utf-8 -*-
import os
from .utils import script_settings_loader

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
        """Fetch all agents
        Returns:
            dict: A dictionary containing all agents (Phantoms).
        """
        return self.req.get(self.AGENTS)

    def get(self, agent_id):
        """Fetch a specific agent by ID
        Args:
            agent_id (str): Agent ID to fetch
        Returns:
            dict: A dictionary containing the agent details.
        """
        return self.req.get(self.AGENT.format(agent_id))

    def output(self, agent_id):
        """Fetch the output of a specific agent by ID
        Args:
            agent_id (str): Agent ID to fetch output for
        Returns:
            dict: A dictionary containing the agent's output.
        """
        return self.req.get(self.AGENT_OUTPUT.format(agent_id))
    
    def run(self, agent_id, arguments=None):
        """Launch a specific agent (run a Phantom)
        Args:
            agent_id (str): Agent ID to launch
            arguments (dict): Optional arguments to send with the launch request.
        Returns:
            dict: A dictionary containing the response from the launch request.
        """
        payload = {
            'id': agent_id,
            'arguments': {}
        }

        # Load script settings for the agent
        script_id = self.get(agent_id).get('scriptId')
        script_settings = script_settings_loader(script_id)
        payload['arguments'].update(script_settings.get('arguments', {}))
        payload['arguments'].update(arguments or {})

        # Ensure sessionCookie is set, either from arguments or environment variable
        if 'sessionCookie' not in payload['arguments']:
            payload['arguments']['sessionCookie'] = os.getenv('PHANTOMBUSTER_COOKIE')

        # Raise exception if required_args are missing.
        if not set(script_settings.get('required', [])).issubset(payload['arguments'].keys()):
            raise ValueError(f"Missing required arguments: {script_settings['required']}")

        return self.req.post(self.AGENT_LAUNCH, payload=payload)

    def create(self, agent_id=None, organizationName="phantombuster", scriptName=None, agentName=None):
        """Save a specific agent (update a Phantom)
        Args:
            agent_id (str): Agent ID to save
            organizationName (str): Organization name to associate with the agent
            scriptName (str): Name of the script associated with the agent
            agentName (str): Name of the agent to save
        Returns:
            dict: A dictionary containing the response from the save request.
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
            agent_id (str): Agent ID to update
            organizationName (str): Organization name to associate with the agent
            scriptName (str): Name of the script associated with the agent
            agentName (str): Name of the agent to update
        Returns:
            dict: A dictionary containing the response from the update request.
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
        Returns:
            dict: A dictionary containing the response from the delete request.
        """
        return self.req.post(self.AGENT_DELETE, payload={'id': agent_id})