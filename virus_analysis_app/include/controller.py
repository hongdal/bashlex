#!/usr/bin/python3.5
import os
import sys
import tkinter as tk
from . import view
from . import model
from .model import *
from . import repository
from .repository import *
import fnmatch


class Controller(object):
  def __init__(self):
    self.script_manager = model.Manager_Script()
    self.view = view.View(self)
    self.view.open_rep()
    self.script_manager.refresh()

  # *****Repository API *****
  def get_all_repository(self):
    rep_dict = self.script_manager.get_all_repository()
    return rep_dict

  def add_repository(self, rep_info, test=True):
    if test:
      rep = {}
      rep["name"] = rep_info[0]
      rep["path"] = rep_info[1]
      self.script_manager.create_test_repo(rep)
    else:
      self.script_manager.add_repository(rep_info)
      self.refresh_scripts()
      self.update_scripts_table()

  def select_rep(self, rep_name):
    res = self.script_manager.select_repository(rep_name)

    if res:
      self.refresh_scripts
      self.update_scripts_table()
      return res
    else:
      return False

  def import_json_to_database(self, file_path):
    res = self.script_manager.import_json_to_database(file_path)
    if res:
      self.refresh_scripts
      self.update_scripts_table()
      return True
    return False

  def delete_rep(self, rep_name):
    res = self.script_manager.delete_repository(rep_name)
    if res:
      self.refresh_scripts()
      return True
    else:
      return False

  def get_all_tags(self):
    script_tags = self.script_manager.get_all_tags()
    return script_tags

  # ***** View API *****
  def get_malware_report(self, names):
    malware_report = self.script_manager.get_malware_info(names)
    return malware_report

  # ***** View API *****
  def update_scripts_table(self):
    # self.refresh()
    self.refresh_scripts()
    recs = self.script_manager.get_all_scripts()
    # print(recs)
    self.view.update_scripts_table(recs)
    return True

  # ***** Script information API  *****
  def get_recommend_scripts(self):
    rec_scripts = self.script_manager.get_recommend_scripts()
    return rec_scripts

  #***** Script information API  *****
  def get_scripts_graph(self, in_file, out_dir):
    script_graph = self.script_manager.getGraph(in_file, out_dir)
    return script_graph

  def get_script_commands(self, in_file, script_path=None):
    script_commands = self.script_manager.getCommands(in_file, script_path)
    return script_commands

  def get_all_commands(self, dir_path):
    all_commands = self.script_manager.getAllCommands(dir_path)
    return all_commands

  def get_all_linux_commands(self, dir_path):
    all_commands = self.script_manager.getAllLinuxCommands(dir_path)
    return all_commands

  def open_script_by_num(self, num_s):
    res = self.script_manager.open_script_by_num(num_s)
    return res

  def generate_virussummary(self, dir_path):
    res = self.script_manager.generate_virussummary(dir_path)
    return res

  def get_malware_detail(self, script_info):
    script_info = self.view.display_details(script_info)
    if script_info is not False:
      script_id, script_im, script_ug, script_tags, read = script_info
      self.script_manager.edit_one_script(script_id, script_im, script_ug,
                                          script_tags, read)
      self.update_scripts_table()

  def change_script_info(self, script_info):
    script_info = self.view.edit_script_info(script_info)
    if script_info is not False:
      script_id, script_im, script_ug, script_tags, read = script_info
      self.script_manager.edit_one_script(script_id, script_im, script_ug,
                                          script_tags, read)
      self.update_scripts_table()

  #***** Output some cache files *****
  def generate_allscripts_graph(self, node_dir, out_dir):
    if os.path.isdir(node_dir):
      for dirpath, dirnames, filenames in os.walk(node_dir):
        for x in filenames:
          if fnmatch.fnmatch(x, "VirusShare*"):
            node_file = os.path.join(node_dir, x)
            self.script_manager.getGraph(node_file, out_dir)
      return True
    else:
      return False

  def update_allscripts_tags(self, node_dir):
    if os.path.isdir(node_dir):
      for dirpath, dirnames, filenames in os.walk(node_dir):
        for x in filenames:
          if fnmatch.fnmatch(x, "VirusShare*"):
            node_file = os.path.join(node_dir, x)
            self.script_manager.getScriptTags(node_file)
      return True
    else:
      return False

  def update_scripts_property(self, low_bound = 0):
    print("Low Bound Value: ", low_bound)
    scripts = self.script_manager.get_all_scripts()
    res = True
    cnt = {}
    cnt["total"] = 0
    cnt["passed"] = 0
    cnt["failed"] = 0
    fail_record = {}
    fail_dict = {}
    fail_dict["GraphFail"] = 0
    for script in scripts:
      name = script[0]
      properties_set = self.script_manager.getScriptProperty(name)
      script_report = self.script_manager.get_malware_info(name)
      properties = ""
      if "positives" in script_report:
        if(script_report["positives"] >= low_bound):
          properties += "P#"
        else:
          properties += "N#"
        properties += str(script_report["positives"]) + "#" + str(script_report["total"])
        # print(script_report["positives"], " : ", script_report["total"])
      else:
        properties += "N#0#0"
      
      properties += ", "
      
      if properties_set:
        graph_successful = properties_set[0]
        properties_info = properties_set[1]
        if graph_successful:
          cnt["passed"] += 1
          for p in properties_info:
            properties += p
            properties += ", "
        else:
          cnt["failed"] += 1
          fail_dict["GraphFail"] += 1
          fail_record[name] = properties_info
          for p in properties_info:
            if p in fail_dict:
              fail_dict[p] += 1
            else:
              fail_dict[p] = 0
      else:
        cnt["failed"] += 1
      properties = properties[:-2]
      res = self.script_manager.update_script_property(name, properties)
    cnt["total"] = cnt["passed"] + cnt["failed"]
    print("Size: ", len(fail_dict), fail_dict)
    if res:
      self.update_scripts_table()
      return cnt
    else:
      return False

  # def open_script_by_num(self, num_s):
  #   self.script_manager.open_script_by_num(num_s)
  #   return True

  def del_script_by_name(self, names):
    self.script_manager.del_script_by_name(names)
    return True

  def get_script_path_by_nums(self, nums):
    res = self.script_manager.get_script_path_by_nums(nums)
    return res

  # ***** Search API *****
  # TODO(Guoze):Complete this function
  def query_by_name(self, name_s):
    res_scripts = self.script_manager.query_by_name(name_s)
    return res_scripts

  def query_by_tags(self, tags_s):
    res_scripts = self.script_manager.query_by_tags(tags_s)
    return res_scripts

  def query_by_property(self, s_property):
    res_scripts = self.script_manager.query_by_property(s_property)
    return res_scripts

  def query_by_nums(self, num_s):
    res_scripts = self.script_manager.query_by_nums(num_s)
    return res_scripts

  def query_by_id(self, id_num):
    res_scripts = self.script_manager.query_by_id(id_num)
    return res_scripts

  '''
      Refresh the scripts in the repo and ask user to add scripts infomation
      Called: select repo || new_repo || delete repo || update table
  '''

  def refresh_scripts(self):
    new_scripts = self.script_manager.refresh()

    def add_script_info(new_script):
      return self.view.ask_script_info(new_script)

    for script in new_scripts:
      # TODO(Guoze): Create a Script class to manager this
      # script_im, script_ug, script_tags, read = add_script_info(script)
      script_im = 1
      script_ug = 1
      script_tags = "None"
      read = "y"
      self.script_manager.insert_one(script, script_im, script_ug, script_tags,
                                     read)

  # ***** System API *****
  def quit(self):
    self.script_manager.quit_script_manager()
    exit(0)


if __name__ == "__main__":
  controller = Controller()
  tk.mainloop()