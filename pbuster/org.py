# -*- coding: utf-8 -*-

class Org(object):

  ORG = "orgs/fetch"
  ORG_RESOURCES = "orgs/fetch-resources"
  ORG_AGENT_GROUPS = "orgs/fetch-agent-groups"

  def __init__(self, req):
    self._req = req


  def info(self):
      """Fetch all organizations
      
      Returns:
          (dict): A dictionary containing information about the organization."""
      return self._req.get(self.ORG)

  def usage(self):
      """Fetch resources for the organization
      
      Returns:
          (dict): A dictionary containing the resources used by the organization.
      """
      return self._req.get(self.ORG_RESOURCES)