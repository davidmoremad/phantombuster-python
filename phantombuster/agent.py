# -*- coding: utf-8 -*-
import os
import json
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

    def _json_to_dict(self, txt):
        """JSON to DICT."""
        if isinstance(txt, dict):
            return txt
        try:
            return json.loads(txt)
        except json.JSONDecodeError:
            return {}

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
        agent = self.req.get(self.AGENT.format(agent_id))
        agent['argument'] = self._json_to_dict(agent.get('argument', ''))
        return agent

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

    def create(self, script_name, agent_name=None, org_name="phantombuster", arguments={}):
        """Create a new agent
        Args:
            scriptName (str): Name of the script to associate with the agent.
            agentName (str): Name of the agent to create.
            organizationName (str): Name of the organization that owns the script. Default is "phantombuster".
        Returns:
            dict: A dictionary containing the response from the save request.
        """
        payload = {
            'script': script_name,
            'name': agent_name or script_name,
            'org': org_name
        }

        return self.req.post(self.AGENT_SAVE, payload=payload)

    def delete(self, agent_id):
        """Delete a specific agent by ID
        Args:
            agent_id (str): Agent ID to delete
        Returns:
            dict: A dictionary containing the response from the delete request.
        """
        return self.req.post(self.AGENT_DELETE, payload={'id': agent_id})