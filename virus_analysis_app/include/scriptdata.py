import xml.etree.ElementTree as ElementTree
import os, sys
import re
from include.bashlex.bashlex import parser, ast
import subprocess
from subprocess import PIPE
import collections
import fnmatch
import json


class ScriptData(object):
  class __ScriptData(object):
    def __init__(self):
      self.commands_counter = collections.Counter()
      self.commands_dict = {}
      self.linux_commands_dict = {}

      #Some Setting for the command pattern for the bash scripts
      self.pattern_command = re.compile(r'CommandNode[^\n]*\n[^\n]*word[^\n]*')
      self.pattern_word = re.compile(r'word=[^\)]*')
      self.pattern_value = re.compile(r'\'[^\']*')
      self.loaddict()
    
    def isLinuxCommand(self, command):
      temp = command.split(' ')[0]
      temp = temp.split('/')[-1]
      if temp in self.commands_dict:
        return temp
      else:
        return False

    def getCommandsDict(self):
      return self.linux_commands_dict

    def getSortedCommandsDict(self):
      items = self.linux_commands_dict.items()
      backitems=[[v[1],v[0]] for v in items]
      backitems.sort(reverse=True)
      res = []
      for i in range(0,len(backitems)):
        tup = (backitems[i][1], backitems[i][0])
        res.append(tup)
      #temp = sorted(self.linux_commands_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
      return res
    
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

    def readscript(self, in_file):
      file_obj = open(in_file)
      filetext = ''
      for line in file_obj:
        filetext += line
      return filetext

    def getScriptCommands(self, in_file):
      total_commands = collections.Counter()
      if os.path.isdir(in_file):
        pass
      else:
        filetext = self.readscript(in_file)
        allcommands = self.pattern_command.findall(filetext)
        for i in range(len(allcommands)):
          if len(self.pattern_word.findall(allcommands[i])):
            allcommands[i] = self.pattern_word.findall(allcommands[i])[0]
            allcommands[i] = self.pattern_value.findall(allcommands[i])[0]
            allcommands[i] = allcommands[i][1:]
          else:
            allcommands[i] = " "
        frequency = collections.Counter(allcommands)
        total_commands = total_commands + frequency
      self.commands_counter += total_commands
      total_commands = total_commands.most_common()
      return total_commands

    def buildCommandsDict(self, total_commands):
      for command in total_commands:
        # if (self.isLinuxCommand(command))
        temp = command[0].split('/')[-1]
        if self.isLinuxCommand(temp):
        # if temp in self.commands_dict:
          if temp not in self.linux_commands_dict:
            self.linux_commands_dict[temp] = command[1]
      print(self.linux_commands_dict)

    def getAllCommands(self, dir_path):
      self.commands_counter.clear()
      if os.path.isdir(dir_path):
        for dirpath, dirnames, filenames in os.walk(dir_path):
          for x in filenames:
            if fnmatch.fnmatch(x, "VirusShare*"):
              node_file = os.path.join(dirpath, x)
              self.getScriptCommands(node_file)
      else:
        self.getScriptCommands(dir_path)

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
