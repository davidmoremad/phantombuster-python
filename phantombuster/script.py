class Script(object):
    
    SCRIPTS = "scripts/fetch-all"
    SCRIPT = "scripts/fetch?id={}"

    def __init__(self, req):
      self.req = req


    def list(self, org_name="phantombuster"):
        """Fetch all scripts (Phantoms)"""
        return self.req.get(f'{self.SCRIPTS}?org={org_name}')

    def get(self, script_id):
        """Fetch a specific script by ID"""
        return self.req.get(self.SCRIPT.format(script_id))