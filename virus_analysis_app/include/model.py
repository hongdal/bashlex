#!/usr/bin/python3.5
import os
import sys
from .repository import Repository
import pickle as pkl
import sqlite3
import random
from datetime import date
from functools import reduce
import json
from six.moves import input

class Manager_Script(object):
  # TODO(Guoze): Create a function to update the view
  def __init__(self):
    self.code_dir = os.path.split(os.path.realpath(__file__))[0]
    self.db_path = os.path.join(self.code_dir, "script_manager.db")
    self.user_config_path = os.path.join(self.code_dir, "user_config.json")
    self.test_path = os.path.dirname(self.code_dir)
    self.test_path = os.path.abspath(self.test_path) + "/"+"dataset/bashData/allscripts"+ "/"
    self.script_item_list = ['script_name', 'importance',
                            'urgency', 'tags', 'path',
                            'read', 'date', 'id']
    self.user_config = self.get_user_config()
    self.conn = sqlite3.connect(self.db_path)
    self.rep_dict = self.user_config.get("all_repositories", {})
    self.cursor = self.conn.cursor()
    self.cur_rep = Repository('BashScript', self.test_path, 'bash')

    if self.user_config:
      pass
    else:
      self.create_test_repo()
    # get repository and path
    # self.select_repository()

  def create_test_repo(self):
    # try:
    #   generator = Generator(self.test_path)
    #   generator.generate()
    # except Exception as error:
    #   print( error )
    test_rep = ['BashScript', self.test_path, "[sh, pdf, mobi, doc]"]
    self.add_repository(test_rep)
    self.cur_rep = Repository(test_rep[0], test_rep[1], test_rep[2])
    new_scripts = self.refresh()
    for script in new_scripts:
      important_num = random.randint(1,3)
      urgeny_num = random.randint(1,3)
      tags = ["None","None","None","None","None","None"]
      tag = tags[random.randint(0,len(tags)-1)]
      if random.randint(0,10) > 5:
        read_flag = 'y'
      else:
        read_flag = 'n'
      self.insert_one(script,important_num, urgeny_num, tag, read_flag)

  # *****Repository Functions*****
  def get_user_config(self):
    if os.path.exists(self.user_config_path):
      with open(self.user_config_path) as f:
        user_config = json.load(f)
    else:
      user_config = {}
    return user_config

  def get_all_repository(self):
    return self.user_config

  def get_malware_info(self, file_name):
    outputDir = os.path.join( os.getcwd(), 'dataset/virtualtotal')
    file_report_name = file_name[:-3]+"_res.json"
    file_report_path = os.path.join(outputDir, file_report_name)
    def get_json_info(file_path):
      # print(file_path)
      if os.path.exists(file_path):
        with open(file_path) as f:
          user_config = json.load(f)
      else:
        user_config = {}
      return user_config
    script_report = get_json_info(file_report_path)
    return script_report
  # Create a New repository and refresh the scripts in this repsitory
  def add_repository(self, reps):
    rep_name = reps[0]
    rep_path = reps[1]
    support_suffix = reps[2]
    rep_dict = self.user_config.get("all_repositories", {})
    rep_dict[rep_name] = [rep_path, support_suffix]
    self.user_config["all_repositories"] = rep_dict
    self.cur_rep = Repository(rep_name, rep_path, support_suffix)
    self.create_a_new_table_for_repository(rep_name)
    self.refresh()
    self.repo_save()

  # Chenge the cur_rep and refresh the script infomation
  def select_repository(self,rep_name):
    rep_dict = self.user_config.get("all_repositories", {})
    if rep_name in rep_dict:
      rep_path, support_suffix = rep_dict[rep_name]
      self.cur_rep = Repository(rep_name, rep_path, support_suffix)
      return [self.cur_rep.name, self.cur_rep.path, self.cur_rep.support_suffix]
    return False

  def delete_repository(self,rep_name):
    rep_dict = self.user_config.get("all_repositories", {})
    if rep_name in rep_dict:
      if rep_name == self.cur_rep.name:
        return False
      del rep_dict[rep_name]
      self.user_config["all_repositories"] = rep_dict
      sql_drop = 'drop table {}'.format(rep_name)
      self.cursor.execute(sql_drop)
      self.repo_save()
    return True

  # *****Script Functions*****
  def refresh(self):
    self.cur_script_names = {}
    self.traverse_scripts(self.cur_rep.path)
    # print scripts_name_now
    old_scripts = self.cursor.execute("SELECT * FROM  {}".format(self.cur_rep.name)).fetchall()
    for old_script in old_scripts:
      old_name = old_script[self.script_item_list.index('script_name')]
      old_path = old_script[self.script_item_list.index('path')]
      # delete the script info that was already been deleted in os
      if old_name not in self.cur_script_names.keys():
        self.del_script_by_names([old_name])
      # if the script was moved, update the script path info
      elif old_path != self.cur_script_names[old_name]:
        self.cursor.execute("UPDATE {} SET path = ? WHERE script_name = ?".format(self.cur_rep.name)
                              , (self.cur_script_names[old_name], old_name))
    old_script_names = self.cursor.execute("SELECT script_name FROM  {}".format(self.cur_rep.name)).fetchall()
    old_script_names = [rec[0] for rec in old_script_names]
    new_scripts = []
    for now_script in self.cur_script_names.keys():
      # find a new script, put in infos
      if now_script not in old_script_names:
        new_scripts.append(now_script)
    return new_scripts

  def traverse_scripts(self, fa_path):
    # pre-ordered depth-first search for every script ends with 'supported suffix
    try:
      paths = os.listdir(fa_path)
    except FileNotFoundError:
      print("Can't find this path.")
      return False
    for path in paths:
      if os.path.isdir(os.path.join(fa_path, path)):
        self.traverse_scripts(os.path.join(fa_path, path))
      else:
        for one_suffix in self.cur_rep.support_suffix:
          if path.endswith(one_suffix):
            self.cur_script_names[path] = os.path.join(fa_path, path)
    return True

  # Get all scripts information form the database by this repo.
  def get_all_scripts(self):
    recs = self.cursor.execute("SELECT * FROM {} ".format(self.cur_rep.name)).fetchall()
    return recs

  # Insert one script information in the database
  def insert_one_script(self, new_script, id_num, script_im, script_ug, script_tags, read):
    self.insert_one(new_script, id_num, script_im,script_ug, script_tags, read)

  def edit_one_script(self, id_num, script_im, script_ug, script_tags, read):
    scripts = self.query_by_id(id_num)
    if len(scripts) > 0:
      self.update_one(scripts[0][0], script_im, script_ug, script_tags, read)
      return True
    else:
      return False

  def get_recommend_scripts(self):
    # select scripts i can read for the sake of importance and urgency
    rec_scripts = self.cursor.execute(
      "SELECT * FROM {} WHERE importance!='' AND urgency!='' AND read='n' ORDER BY urgency DESC , importance DESC LIMIT 5 ".format(
      self.cur_rep.name)).fetchall()
    if len(rec_scripts) > 0:
      return rec_scripts

  # get all tags of my scripts
  def get_all_tags(self):
    tags = self.cursor.execute("SELECT tags FROM {}".format(self.cur_rep.name)).fetchall()
    tags = [tag[0] for tag in tags]
    tag_set = set()
    for line in tags:
      for tag in line.strip().split(' '):
        if tag.strip() != '':
          tag_set.add(tag)
    tag_s = []
    for i, tag in enumerate(tag_set):
      tag_s.append(tag)
    return tag_s

  def get_script_path_by_nums(self, num_s):
    results = self.query_path_by_nums( str(num_s) )
    if len(results) > 0:
      for res in results:
        return res
    else:
      return False

  def open_script_by_num(self, num_s):
    results = self.query_path_by_nums(num_s)
    if len(results) == 0:
      print("Find nothing. Open script failed!")
      return False
    elif len(results) > 1:
      print("Too much nums, please input one id num !")
      return False
    else:
      # open script by system default software, only support linux platform now
      if sys.platform.startswith('linux'):
        file_path = '/'.join(results[0])
        os.system("xdg-open {} > log.txt 2>&1 &".format(file_path))
        return True
      else:
        print("Error:open file only support linux platform now !")
        return False

  # search scripts by tags
  def query_by_tags(self, tags_s):
    sets = []
    tags = tags_s.strip().split(' ')
    if len(tags) > 0:
      for tag in tags:
        recs = self.cursor.execute(
          "select * from {} where tags like '%{}%'".format(self.cur_rep.name, tag)).fetchall()
        if len(recs) > 0:
          res_set = set()
          for rec in recs:
            res_set.add(rec)
          sets.append(res_set)
    results = set()
    if len(sets) > 0:
      results = sets[0]
      if len(sets) > 1:
        for one_set in sets[1:]:
          results = results & one_set
    if len(results) > 0:
      return results
    else:
      return False

  def query_by_name(self, name_s):
    sets = []
    names = name_s.strip().split(' ')
    if len(names) > 0:
      for name in names:
        recs = self.cursor.execute(
          "select * from {} where script_name like '%{}%'".format(self.cur_rep.name, name)).fetchall()
        if len(recs) > 0:
          res_set = set()
          for rec in recs:
            res_set.add(rec)
          sets.append(res_set)
    results = set()
    if len(sets) > 0:
      results = sets[0]
      if len(sets) > 1:
        for one_set in sets[1:]:
          results = results & one_set
    if len(results) > 0:
      return results
    else:
      return False

  def query_path_by_nums(self, num_s):
    results = []
    nums = num_s.strip().split(' ')
    if len(nums) > 0:
      for num in nums:
        recs = self.cursor.execute("SELECT * FROM {} WHERE id=? ".format(self.cur_rep.name), (num,)).fetchall()
        if len(recs) > 0:
          for rec in recs:
            results.append(rec[4])
    return results

  # search scripts by id nums
  def query_by_nums(self, num_s):
    results = []
    nums = num_s.strip().split(' ')
    if len(nums) > 0:
      for num in nums:
        recs = self.cursor.execute("SELECT * FROM {} WHERE id=? ".format(self.cur_rep.name), (num,)).fetchall()
        if len(recs) > 0:
          for rec in recs:
            results.append(rec)
    if len(results) > 0:
      return results
    else:
      return False

  def query_by_id(self, id_num):
    scripts = self.cursor.execute("SELECT * FROM {} WHERE id=?".format(self.cur_rep.name), (id_num,)).fetchall()
    if len(scripts) == 1:
      return scripts
    else:
      return False

  # *****Script Database(SQLite3) Functions*****
  # create the table if not exist, table name is same as repository name
  def create_a_new_table_for_repository(self, rep_name):
    sql_create = 'create table if not exists {}' \
                ' ( script_name varchar(100) , ' \
                'importance integer, urgency integer, ' \
                'tags varchar(100), path varchar(100), ' \
                'read varchar(10), date TEXT, ' \
                'id integer primary key autoincrement)'.format(rep_name)
    self.cursor.execute(sql_create)

  def del_script_by_names(self, names):
    for name in names:
        self.cursor.execute("DELETE FROM {} WHERE script_name = ?".format(self.cur_rep.name), (name,))
    self.conn.commit()

  def insert_one(self, script_name, script_im, script_ug, script_tags, read):
    self.cursor.execute("INSERT INTO {} (script_name, importance, urgency, tags, path, read, date) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)".format(self.cur_rep.name), (script_name, script_im,
                                                                                    script_ug, script_tags,
                                                                                    self.cur_script_names[script_name],
                                                                                    read, str(date.today())))
    self.conn.commit()

  def update_one(self, script_name, script_im, script_ug, script_tags, read):
    self.cursor.execute("UPDATE {} SET importance=?, urgency=?, "
                        "tags=?, path=?, read=?, date=? WHERE script_name=?".format(self.cur_rep.name),
                        (script_im, script_ug, script_tags, self.cur_script_names[script_name],
                          read, str(date.today()), script_name))
    self.conn.commit()

  def repo_save(self):
    # save user data
    with open(self.user_config_path, 'w') as f:
      json.dump(self.user_config, f)

    self.user_config = self.get_user_config()
    self.rep_dict = self.user_config.get("all_repositories", {})

  def quit_script_manager(self):
    # save user data
    with open(self.user_config_path, 'w') as f:
      json.dump(self.user_config, f)
    # close the sqlite db
    self.cursor.close()
    self.conn.commit()
    self.conn.close()

if __name__ == '__main__':
  pass
