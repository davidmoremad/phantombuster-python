# -*- coding: utf-8 -*-
import os
import json
from .utils import script_settings_loader
from pbuster.container import Container

class Agent(object):

    AGENTS = "agents/fetch-all"
    AGENT = "agents/fetch?id={}"
    AGENT_OUTPUT = "agents/fetch-output?id={}"
    AGENT_LAUNCH = "agents/launch"
    AGENT_SAVE = "agents/save"
    AGENT_DELETE = "agents/delete"

    WAIT_TIME = 2  # seconds

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
        """Fetch all agents (Phantoms)
        
        Returns:
            (dict): A dictionary containing all agents (Phantoms).
        """
        return self.req.get(self.AGENTS)

    def get(self, agent_id):
        """Fetch a specific agent by ID

        Args:
            agent_id (str): Agent ID to fetch

        Returns:
            (dict): A dictionary containing the agent details.
        """
        agent = self.req.get(self.AGENT.format(agent_id))
        agent['argument'] = self._json_to_dict(agent.get('argument', ''))
        return agent
    
    def status(self, agent_id):
        """Fetch the status of the last execution of a specific agent by ID

        Args:
            agent_id (str): Agent ID to fetch status for
        
        Returns:
            (str): Status of the last agent execution. [`finished` `killed` `global timeout` `org timeout` `agent timeout` `unknown` `no log timeout`]
        """
        return self.req.get(self.AGENT.format(agent_id)).get('lastEndType', "")


    def output(self, agent_id):
        """Fetch the output of a specific agent by ID
        
        Args:
            agent_id (str): Agent ID to fetch output for
        
        Returns:
            (dict): A dictionary containing the agent's output.
        """
        return self.req.get(self.AGENT_OUTPUT.format(agent_id))
    
    def launch(self, agent_id, arguments=None):
        """Run a specific agent.
        
        Args:
            agent_id (str): Agent ID to launch
            arguments (dict): Arguments to send with the launch request. Some are required, depending on the script.
        
        Returns:
            (dict): A dictionary containing the response with the container ID of the launched agent.
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

    def launch_and_wait(self, agent_id, arguments=None):
        """Run a specific agent and wait for it to finish and get results
        
        Args:
            agent_id (str): Agent ID to launch
            arguments (dict): Arguments to send with the launch request. Some are required, depending on the script.
        
        Returns:
            (tuple): A tuple containing the container ID and the results of the agent execution.
        """
        # 1. Run the agent
        pb_container = Container(self.req)
        response = self.launch(agent_id, arguments)
        container_id = response.get('containerId')
        
        if not container_id:
            raise ValueError("Failed to launch agent: No container ID returned.")
        
        # 2. Wait for completion
        container = pb_container.wait(container_id)

        # 3. Error handling
        if container.get('exitCode') != 0:
            raise ValueError(f"Agent failed. Container {container_id} got exit code {container.get('exitCode')}.")
        if container.get('exitCode') == 0 and not container.get('resultObject'):
            raise ValueError(f"Agent {agent_id} did not return any output.\nRuntime events: {', '.join([event.get('text') for event in container.get('runtimeEvents', [])])}\n")
        
        return container

    def create(self, script_name, agent_name=None, org_name="phantombuster", arguments={}):
        """Create a new agent
        
        Args:
            script_name (str): Name of the script to associate with the agent.
            agent_name (str): Name of the agent to create.
            org_name (str): Name of the organization that owns the script. Default is "phantombuster".
            arguments (dict): Optional arguments to send with the agent creation request.
        
        Returns:
            (dict): ID of the created agent.
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
            (dict): A dictionary containing the response from the delete request.
        """
        return self.req.post(self.AGENT_DELETE, payload={'id': agent_id})