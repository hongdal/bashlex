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


# FunctionNode(lineno=69, pos=(1823, 2914), parts=[
#   ReservedwordNode(lineno=49, pos=(1823, 1831), word='function'),
#   WordNode(lineno=49, pos=(1832, 1842), word='enable_ssh'),
      # Some Setting for the command pattern for the bash scripts
      self.pattern_command = re.compile(r'CommandNode[^\n]*\n[^\n]*word[^\n]*')
      self.pattern_special_command = re.compile(r'CommandNode[^\n]*\n[^\n]*\n[^\n]*word[^\n]*')
      self.pattern_function = re.compile(r'FunctionNode[^\n]*\n[^\n]*\n[^\n]*word[^\n]*')
      self.pattern_word = re.compile(r'word=[^\)]*')
      self.pattern_value = re.compile(r'\'[^\']*')
      self.cd_pattern_value = re.compile(r'\ncd')
      self.down_commands_list = ["wget", "ftp", "tftp", "curl"]
      self.command_to_file_dict = {}
      self.loaddict()

    def getcommand_to_file_dict(self):
      command_to_file_dict = {}
      for v in self.command_to_file_dict:
        temp_list = []
        for item in self.command_to_file_dict[v]:
          temp_list.append(item)
        command_to_file_dict[v] = temp_list
      return command_to_file_dict

    def getCommandsClass(self, command):
      command = command.strip()
      temp = command.split(' ')[0]
      temp = temp.split('/')[-1]
      if temp in self.commands_dict:
        if "category" in self.commands_dict[temp]:
          return self.commands_dict[temp]["category"]
        else:
          return "Others"
      else:
        return False

    def dealDownloadCommand(self, ans):
      command = ans["name"]
      text = ans["text"]
      filename = text.split('/')[-1]
      if command == "wget":
        searchObj = re.search(r'-O[ ]*[\/\.]*[^ ]*', text)
        if searchObj:
          temp = str(searchObj.group())
          filename = text.split('/')[-1]
        ans["filename"] = filename
      elif command == "ftp":
        pass
      elif command == "curl":
        pass
      elif command == "tftp":
        pass

      if filename:
        ans["filename"] = filename

      return ans

    def isBinaryFile(self, ans):
      text = ans["text"]
      command = text.lstrip()
      if command[0:2] == "./":
        return True
      return False

    def inquiryCommandInfo(self, commandtext):
      # 1) Detect whether this is a Linux Command in the dictionary
      # a) Detect whether this is a network command, if this is a network command,
      # add the filename part in the dictionary.
      # b) If this is not a network command, then return it
      # TODO: Deal with if, which and a assignment
      ans = {}
      command = commandtext.strip()
      temp = command.split(' ')[0]
      temp = temp.split('/')[-1]
      ans["text"] = commandtext
      ans["name"] = temp
      ans["filename"] = ""
      if self.isBinaryFile(ans):
        ans["category"] = "binaryfile"
        ans["text"] = "Run BinaryFile"
        return ans

      if command[:2] == '\[' and command[-2:] == '\]':
        ans["category"] = "condition"
        ans["text"] = commandtext
        return ans

      if "=" in command:
        ans["category"] = "assignment"
        ans["text"] = commandtext
        return ans

      if temp in self.commands_dict:
        if "category" in self.commands_dict[temp]:
          ans["category"] = self.commands_dict[temp]["category"]
          if self.commands_dict[temp]["category"] == "network":
            if temp in self.down_commands_list:
              ans["downloaded"] = True
            else:
              ans["downloaded"] = False
            ans = self.dealDownloadCommand(ans)
        else:
          ans["category"] = "others"
      else:
        ans["category"] = "unknown"
      return ans

    def isLinuxCommand(self, command):
      command = command.strip()
      temp = command.split(' ')[0]
      temp = temp.split('/')[-1]
      if temp in self.commands_dict:
        return self.commands_dict[temp]
      else:
        return False

    def getCommandsDict(self):
      return self.linux_commands_dict

    def getSortedCommandsDict(self):
      items = self.linux_commands_dict.items()
      backitems = [[v[1], v[0]] for v in items]
      backitems.sort(reverse=True)
      res = []
      for i in range(0, len(backitems)):
        command_class = self.getCommandsClass(backitems[i][1])
        tup = (backitems[i][1], backitems[i][0], command_class)
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
      file_obj = open(in_file, encoding="ISO-8859-1")
      filetext = ''
      for line in file_obj:
        filetext += line
      return filetext

    def readscriptSpace(self, in_file):
      file_obj = open(in_file, encoding="ISO-8859-1")
      filetext = ''
      for line in file_obj:
        filetext += "\n" + line
      return filetext

    def getScriptCommands(self, in_file):
      total_commands = collections.Counter()
      if os.path.isdir(in_file):
        pass
      else:
        filetext = self.readscript(in_file)
        func_commands = self.pattern_function.findall(filetext)

        for i in range(len(func_commands)):
          if len(self.pattern_word.findall(func_commands[i])):
            func_commands[i] = self.pattern_word.findall(func_commands[i])[1]
            func_commands[i] = self.pattern_value.findall(func_commands[i])[0]
            func_commands[i] = func_commands[i][1:]
          else:
            func_commands[i] = " "
        except_set = set(func_commands)


        allcommands = self.pattern_command.findall(filetext)
        special_command = self.pattern_special_command.findall(filetext)
        for i in range(len(allcommands)):
          if len(self.pattern_word.findall(allcommands[i])):
            allcommands[i] = self.pattern_word.findall(allcommands[i])[0]
            allcommands[i] = self.pattern_value.findall(allcommands[i])[0]
            allcommands[i] = allcommands[i][1:]
          else:
            allcommands[i] = " "


        for command in allcommands:
          if command in except_set:
            allcommands.remove(command)

        basename = os.path.basename(in_file)[:-5]
        for command in allcommands:
          if command not in self.command_to_file_dict:
            temp_set = set([basename])
            self.command_to_file_dict[command] = temp_set
          else:
            self.command_to_file_dict[command].add(basename)

        frequency = collections.Counter(allcommands)
        total_commands = total_commands + frequency
      self.commands_counter += total_commands
      total_commands = total_commands.most_common()
      return total_commands

    def detectScript(self, in_file):
      # cd_pattern_value
      # total_commands = collections.Counter()
      detect_flags = []
      if os.path.isdir(in_file):
        pass
      else:
        filetext = self.readscriptSpace(in_file)
        # print(filetext)
        allcommands = self.cd_pattern_value.findall(filetext)
        # print(allcommands)
        if len(allcommands) > 4:
          detect_flags.append("CD_PATTERN")
        else:
          detect_flags.append("NOT_CD")

      return detect_flags


    def buildCommandsDict(self, total_commands):
      for command in total_commands:
        # if (self.isLinuxCommand(command))
        # temp = command[0].split('/')[-1]
        temp = command[0].strip()
        # print(temp)
        res = self.inquiryCommandInfo(temp)
        if res:
          if len(temp) > 0:
            if temp[0] == '/' or res["category"] == 'unknown' or res[
                "category"] == 'binaryfile' or res["category"] == "assignment":
              pass
            else:
              self.linux_commands_dict[temp] = command[1]
      return self.linux_commands_dict

    def getAllCommands(self, dir_path):
      self.commands_counter.clear()
      if os.path.isdir(dir_path):
        for dirpath, dirnames, filenames in os.walk(dir_path):
          for x in filenames:
            if fnmatch.fnmatch(x, "*.node"):
              node_file = os.path.join(dirpath, x)
              self.getScriptCommands(node_file)
      else:
        self.getScriptCommands(dir_path)

      total_commands = self.commands_counter.most_common()
      self.buildCommandsDict(total_commands)
      # print( self.command_to_file_dict)
      # print(len(self.linux_commands_dict))
      return total_commands

  instance = None

  def __new__(self):
    if not ScriptData.instance:
      ScriptData.instance = ScriptData.__ScriptData()
    return ScriptData.instance


if __name__ == '__main__':
  pass
