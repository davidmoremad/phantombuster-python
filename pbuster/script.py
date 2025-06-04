# -*- coding: utf-8 -*-
class Script(object):
    
    SCRIPTS = "scripts/fetch-all"
    SCRIPT = "scripts/fetch?id={}"

    def __init__(self, req):
        self._req = req

    def list(self, org_name="phantombuster"):
        """Fetch all scripts (Phantoms)
        Args:
            org_name (str): Organization name to filter scripts by. Default is "phantombuster".
        Returns:
            dict: A dictionary containing all scripts for the specified organization.
        """
        return self._req.get(f'{self.SCRIPTS}?org={org_name}')

    def get(self, script_id):
        """Fetch a specific script by ID
        Args:
            script_id (str): The ID of the script to fetch.
        Returns:
            dict: A dictionary containing the script details.
        """
        return self._req.get(self.SCRIPT.format(script_id))
    

    def get_args(self, script_id):
        """Fetch the arguments of a specific script by ID
        Args:
            script_id (str): The ID of the script to fetch arguments for.
        Returns:
            dict: A dictionary containing the script's arguments.
        """
        script = self.get(script_id)
        return script.get('argumentTypes', {})