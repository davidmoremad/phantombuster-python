class Org(object):

  ORG = "orgs/fetch"
  ORG_RESOURCES = "orgs/fetch-resources"
  ORG_AGENT_GROUPS = "orgs/fetch-agent-groups"

  def __init__(self, req):
    self.req = req


  def info(self):
      """Fetch all organizations"""
      return self.req.get(self.ORG)
  
  def usage(self):
      """Fetch resources for the organization"""
      return self.req.get(self.ORG_RESOURCES)