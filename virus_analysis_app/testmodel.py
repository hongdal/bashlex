import os
import sys
import unittest
import json
import sqlite3
import shutil
import include.model as model
from include.model import Manager_Script

class TestManager_Script(unittest.TestCase):
  def setUp(self):
    self.script_manager = model.Manager_Script()
    self.base_path = os.path.abspath(os.curdir)
    self.script_manager.db_path = os.path.join(self.base_path,
                                                "test_script_manager.db")
    self.script_manager.user_config_path = os.path.join(self.base_path,
                                                        "test_user_config.json")
    self.script_manager.conn = sqlite3.connect(self.script_manager.db_path)
    self.script_manager.cursor = self.script_manager.conn.cursor()
    self.script_path = os.path.join(self.base_path, "test_script")
    if not os.path.exists(self.script_path):
      os.makedirs(self.script_path)
    for i in range(5):
      script = self.script_path+"/"+ str(i) +".pdf"
      f = open(script,'w')
      f.write("Test")
      f.close()
    self.test_reps=["Tang",self.script_path,"pdf"]
    self.script_manager.add_repository(self.test_reps)
    for i in range(3):
      script_name = str(i) + ".pdf"
      self.script_manager.insert_one(script_name,i,i,"Network"+str(i),"n")

  def tearDown(self):
    self.script_manager.conn.commit()
    self.script_manager.cursor.close()
    self.script_manager.conn.close()
    os.remove(self.script_manager.db_path)
    os.remove(self.script_manager.user_config_path)
    shutil.rmtree(self.script_path)

  def test_get_user_config(self):
    if os.path.exists(self.script_manager.user_config_path):
      with open(self.script_manager.user_config_path) as f:
        expect_config = json.load(f)
    else:
      expect_config={}
    user_config = self.script_manager.get_user_config()
    self.assertEqual(user_config, expect_config)

  def test_get_all_repository(self):
    self.assertEqual(self.script_manager.get_all_repository(),
                    self.script_manager.user_config)

  def test_add_repository(self):
    new_rep = ["New_rep",self.script_path,"mobi"]
    self.script_manager.add_repository(new_rep)
    self.script_manager.select_repository("New_rep")
    self.assertEqual(self.script_manager.cur_rep.path
                      ,self.script_path)
    self.assertEqual(self.script_manager.cur_rep.name
                      ,"New_rep")
    self.assertEqual(self.script_manager.cur_rep.support_suffix
                      ,"mobi")


  def test_select_repository(self):
    self.script_manager.select_repository("Tang")
    self.assertEqual(self.script_manager.cur_rep.path
                      ,self.script_path)
    self.assertEqual(self.script_manager.cur_rep.name
                      ,"Tang")
    self.assertEqual(self.script_manager.cur_rep.support_suffix
                      ,"pdf")

  def test_delete_repository(self):
    self.script_manager.select_repository("Tang")
    self.assertFalse(self.script_manager.delete_repository("Tang"))

    new_rep = ["New_rep",self.script_path,"pdf"]
    self.script_manager.add_repository(new_rep)
    self.assertTrue(self.script_manager.delete_repository("Tang"))

  def test_refresh(self):
    new_scripts = self.script_manager.refresh()
    expect_scripts=['3.pdf', '4.pdf']
    self.assertEqual(len(new_scripts), len(expect_scripts) )

  def test_get_all_scripts(self):
    all_scripts = self.script_manager.get_all_scripts()
    self.assertEqual(len(all_scripts)
                      ,3)
    script_name = "4.pdf"
    self.script_manager.insert_one(script_name,2,3,"Network","n")

    all_scripts = self.script_manager.get_all_scripts()
    self.assertEqual(len(all_scripts)
                      ,4)

  def test_edit_one_peper(self):
    script_name = "4.pdf"
    self.script_manager.insert_one(script_name,2,3,"Test","n")

    all_scripts = self.script_manager.get_all_scripts()
    index_script = len(all_scripts) - 1
    index_id = len(all_scripts[3]) - 1
    index_tags = 3
    self.assertEqual(all_scripts[index_script][index_id]
                      ,4)
    self.assertEqual(all_scripts[index_script][index_tags]
                      ,"Test")
    script_id = all_scripts[index_script][index_id]
    self.script_manager.edit_one_script(script_id, 5, 5, "Update","y")

    all_scripts = self.script_manager.get_all_scripts()
    self.assertEqual(all_scripts[index_script][index_tags]
                      ,"Update")

  def test_get_recommend_scripts(self):
    rec_scripts = self.script_manager.get_recommend_scripts()
    index_script = 0
    index_name = 0
    self.assertEqual(rec_scripts[index_script][index_name]
                      ,"2.pdf")

  def test_get_all_tags(self):
    tags = self.script_manager.get_all_tags()
    expect_tags = ['Network0', 'Network1', 'Network2']
    self.assertEqual(len(tags),len(expect_tags))

  def test_get_script_path_by_nums(self):
    all_scripts = self.script_manager.get_all_scripts()
    index_script = len(all_scripts) - 1
    index_id = len(all_scripts[index_script]) - 1
    index_name = all_scripts[index_script][0]
    script_path = self.script_manager.get_script_path_by_nums(all_scripts[index_script][index_id])
    expect_path = self.script_path+"/"+ str(index_name)
    self.assertEqual(script_path,expect_path)

  def test_query_by_tags(self):
    search_tag = "Network2"
    res_script = self.script_manager.query_by_tags(search_tag)
    self.assertEqual(len(res_script),1)

if __name__=="__main__":
  unittest.main()
