import xml.etree.ElementTree as ElementTree
import os, sys
import re
from include.bashlex.bashlex import parser, ast
from .parserxml import XmlListConfig
from .parserxml import XmlDictConfig
import collections



class ScriptData(object):
  class __ScriptData(object):
    def __init__(self):
      self.data_path = os.path.join( os.getcwd(), 'include/appSpec/app.xml' )
      self.datatree = ElementTree.parse(self.data_path)
      self.dataroot = self.datatree.getroot()
      self.datadict = XmlDictConfig(self.dataroot)

    def findInText(regex, text, linesConf):
      '''
        return a list of maps, each map is a match to multilines,
                in a map, key is the line keyword
                          and value is the content corresponding to the key
      '''
      matched = regex.findall(text)
      if empty(matched):
          return []

      allMatched = []
      linePatternMap = buildLinePatternMap(linesConf)
      for onematch in matched:
          oneMatchedMap = buildOneMatchMap(linesConf, onematch, linePatternMap)
          allMatched.append(oneMatchedMap)
      return allMatched
    
    def readscript(slef, in_file):
      file_obj = open(in_file)
      filetext = ''
      for line in file_obj:
        filetext += line
      return filetext

    def getScriptCommands(self, in_file):
      # command = re.compile(r'Command.*\n.*)
      filetext = self.readscript(in_file)
      # print(filetext)
      allcommands = re.findall(r'CommandNode[^\n]*\n[^\n]*', filetext,re.DOTALL)
      for i in range(len(allcommands)):
        allcommands[i] = re.findall(r'word=[^\)]*', allcommands[i],re.DOTALL)[0]
        allcommands[i] = re.findall(r'\'[^\']*', allcommands[i],re.DOTALL)[0]
        allcommands[i] = allcommands[i][1:]
      frequency = collections.Counter(allcommands)
      freq_command = frequency.most_common()
      return freq_command

  instance = None
  def __new__(self):
    if not ScriptData.instance:
      ScriptData.instance = ScriptData.__ScriptData()
    return ScriptData.instance
  


if __name__ == '__main__':
  pass
