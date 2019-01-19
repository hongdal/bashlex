import xml.etree.ElementTree as ElementTree
import os, sys
import re
from include.bashlex.bashlex import parser, ast
from .parserxml import XmlListConfig
from .parserxml import XmlDictConfig
import subprocess
from subprocess import PIPE
import collections
import fnmatch
import json


class ScriptData(object):
  class __ScriptData(object):
    def __init__(self):
      self.data_path = os.path.join(os.getcwd(), 'include/appSpec/app.xml')
      self.datatree = ElementTree.parse(self.data_path)
      self.dataroot = self.datatree.getroot()
      self.datadict = XmlDictConfig(self.dataroot)
      self.commands_counter = collections.Counter()
      self.commands_dict = {}
      self.linux_commands_dict = {}
      self.loaddict()
      self.pattern_command = re.compile(r'CommandNode[^\n]*\n[^\n]*word[^\n]*')
      self.pattern_word = re.compile(r'word=[^\)]*')
      self.pattern_value = re.compile(r'\'[^\']*')

    def loaddict(self):
      def get_json_info(file_path):
        # print(file_path)
        if os.path.exists(file_path):
          with open(file_path) as f:
            user_config = json.load(f)
        else:
          user_config = {}
        return user_config

      command_path = os.path.join(os.getcwd(), 'res/commands.json')
      self.commands_dict = get_json_info(command_path)

    def findInText(self, regex, text, linesConf):
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

    def readscript(self, in_file):
      file_obj = open(in_file)
      filetext = ''
      for line in file_obj:
        filetext += line
      return filetext

    def getCommandsDict(self, in_file):
      return self.linux_commands_dict

    def getScriptCommands(self, in_file):
      total_commands = collections.Counter()
      if os.path.isdir(in_file):
        pass
      else:
        # command = re.compile(r'Command.*\n.*)
        filetext = self.readscript(in_file)
        # print(filetext)
        # pattern = re.compile(r'CommandNode[^\n]*\n[^\n]*word[^\n]*')
        # allcommands = self.pattern_command.findall(filetext, re.DOTALL)
        # print(allcommands)
        allcommands = re.findall(r'CommandNode[^\n]*\n[^\n]*word[^\n]*',
                                 filetext, re.DOTALL)
        for i in range(len(allcommands)):
          # print(i, "Node: ", allcommands[i])
          # if len(re.match(r'word=[^\)]*', allcommands[i], re.DOTALL)):
          #   allcommands[i] = re.findall(r'word=[^\)]*', allcommands[i],
          #                               re.DOTALL)[0]
          #   allcommands[i] = re.findall(r'\'[^\']*', allcommands[i],
          #                               re.DOTALL)[0]
          #   allcommands[i] = allcommands[i][1:]
          # else:
          #   allcommands[i] = " "
          if len(self.pattern_word.findall(allcommands[i], re.DOTALL)):
            allcommands[i] = self.pattern_word.findall(allcommands[i])[0]
            allcommands[i] = self.pattern_value.findall(
                allcommands[i])[0]
            allcommands[i] = allcommands[i][1:]
          else:
            allcommands[i] = " "
        frequency = collections.Counter(allcommands)
        total_commands = total_commands + frequency
      self.commands_counter += total_commands
      total_commands = total_commands.most_common()
      # print(total_commands)
      return total_commands

    def buildCommandsDict(self, total_commands):
      for command in total_commands:
        temp = command[0].split('/')[-1]
        if temp in self.commands_dict:
          print("Catch the key:", command[0])
          if temp not in self.linux_commands_dict:
            self.linux_commands_dict[temp] = command[1]
      print(self.linux_commands_dict)

    def getAllCommands(self, dir_path):
      self.commands_counter.clear()
      # files = os.listdir( dir_path )
      if os.path.isdir(dir_path):
        for dirpath, dirnames, filenames in os.walk(dir_path):
          for x in filenames:
            if fnmatch.fnmatch(x, "VirusShare*"):
              node_file = os.path.join(dirpath, x)
              # print(i, "Node:", node_file)
              self.getScriptCommands(node_file)
              # output = x[:-5]+".dot"
              # output2 = outputDir+"/"+output
              # retcode = subprocess.call("python3.5 parserDot.py "+malware_file+">"+output2, shell=True)
              # if retcode != 0:
              #   print "\tFAILED to parser the bash code.", x
              #   failed += 1
              #   os.remove(output2)
              # else:
              #   print x," passed"
              #   passed += 1
              #   os.remove(malware_file)
      else:
        self.getScriptCommands(in_file)

      total_commands = self.commands_counter.most_common()
      self.buildCommandsDict(total_commands)
      print(len(self.linux_commands_dict))
      return total_commands

  instance = None

  def __new__(self):
    if not ScriptData.instance:
      ScriptData.instance = ScriptData.__ScriptData()
    return ScriptData.instance


if __name__ == '__main__':
  pass
