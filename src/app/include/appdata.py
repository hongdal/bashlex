import xml.etree.ElementTree as ElementTree
import os, sys
from .parserxml import XmlListConfig
from .parserxml import XmlDictConfig
# import parsexml

class AppData(object):
  class __AppData(object):
    def __init__(self):
      self.data_path = os.path.join( os.getcwd(), 'include/appSpec/app.xml' )
      self.datatree = ElementTree.parse(self.data_path)
      self.dataroot = self.datatree.getroot()
      self.datadict = XmlDictConfig(self.dataroot)

  instance = None
  def __new__(self):
    if not AppData.instance:
      AppData.instance = AppData.__AppData()
    return AppData.instance


# class OnlyOne(object):
#     class __OnlyOne:
#         def __init__(self):
#             self.val = None
#         def __str__(self):
#             return `self` + self.val
#     instance = None
#     def __new__(cls): # __new__ always a classmethod
#         if not OnlyOne.instance:
#             OnlyOne.instance = OnlyOne.__OnlyOne()
#         return OnlyOne.instance
#     def __getattr__(self, name):
#         return getattr(self.instance, name)
#     def __setattr__(self, name):
#         return setattr(self.instance, name)


