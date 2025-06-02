# -*- coding: utf-8 -*-

class Org(object):

  ORG = "orgs/fetch"
  ORG_RESOURCES = "orgs/fetch-resources"
  ORG_AGENT_GROUPS = "orgs/fetch-agent-groups"

  def __init__(self, req):
    self._req = req


  def info(self):
      """Fetch all organizations"""
      return self._req.get(self.ORG)

  def usage(self):
      """Fetch resources for the organization"""
      return self._req.get(self.ORG_RESOURCES)