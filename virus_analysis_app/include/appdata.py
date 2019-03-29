import os, sys
import xml.etree.ElementTree as ElementTree
from .parserxml import XmlListConfig
from .parserxml import XmlDictConfig


class AppData(object):
  class __AppData(object):
    def __init__(self):
      self.data_path = os.path.join(os.getcwd(), 'include/appSpec/app.xml')
      self.datatree = ElementTree.parse(self.data_path)
      self.dataroot = self.datatree.getroot()
      self.datadict = XmlDictConfig(self.dataroot)

  instance = None

  def __new__(self):
    if not AppData.instance:
      AppData.instance = AppData.__AppData()
    return AppData.instance
