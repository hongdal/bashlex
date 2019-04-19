#!/usr/bin/python

import os, sys
import fnmatch
import subprocess
from subprocess import PIPE
import filecmp
import requests
import json
import ast
import time

api_key = 'fa7637acf76e8dde829003893c7d3589e2232f0e909bd589413cea9c6948b81a'
dataDir = os.path.join(os.getcwd(), 'dataset/bashData/allscripts')
# dataDir = os.path.join( os.getcwd(), '0_data/test_data_bash')
outputDir = os.path.join(os.getcwd(), 'dataset/virtualtotal')
request_file_path = os.path.join(os.getcwd(), "request.json")
report_file_path = os.path.join(os.getcwd(), "report.json")
request_file_test_path = os.path.join(os.getcwd(), "request_test.json")
report_file__test_path = os.path.join(os.getcwd(), "report_test.json")


def get_json_info(file_path):
  # print(file_path)
  if os.path.exists(file_path):
    with open(file_path) as f:
      user_config = json.load(f)
  else:
    user_config = {}
  return user_config


def save_json_info(file_path, information):
  # save user data
  with open(file_path, 'w') as f:
    json.dump(information, f)


def request_scan(script_file):
  file_name = os.path.basename(os.path.normpath(script_file))
  params = {'apikey': api_key}
  files = {'file': (file_name, open(script_file, 'r'))}
  response = requests.post(
      'https://www.virustotal.com/vtapi/v2/file/scan',
      files=files,
      params=params)
  json_response = response.json()
  # TEST
  # json_response = get_json_info(request_file_path)
  return json_response


def download_report(resource_code):
  import requests
  params = {'apikey': api_key, 'resource': resource_code}
  headers = {
      "Accept-Encoding":
          "gzip, deflate",
      "User-Agent":
          "gzip,  My Python requests library example client or username"
  }
  response = requests.get(
      'https://www.virustotal.com/vtapi/v2/file/report',
      params=params,
      headers=headers)
  json_response = response.json()
  # json_response = get_json_info(report_file_path)
  return json_response


def re_scan(md5_num):
  import requests
  params = {'apikey': api_key, 'md5': '0a49b16535e90e17e6a55252cf49e329'}
  headers = {
      "Accept-Encoding":
          "gzip, deflate",
      "User-Agent":
          "gzip,  My Python requests library example client or username"
  }
  response = requests.post(
      'https://www.virustotal.com/vtapi/v2/file/rescan', params=params)
  json_response = response.json()
  return json_response


def get_query(script_file_path):
  time.sleep(16)
  file_name = os.path.basename(os.path.normpath(script_file_path))
  re_output = file_name[:-3] + "_que.json"
  re_output2 = outputDir + "/" + re_output
  # if os.path.exists(re_output2):
  #   print("We have this file: ", re_output2)
  #   return True

  res_request = request_scan(script_file_path)
  save_json_info(re_output2, res_request)
  resource_code = res_request["resource"]

  # print(resource_code)
  # print(res_request["resource"])
  time.sleep(16)
  res_report = download_report(resource_code)
  res_output = file_name[:-3] + "_res.json"
  res_output2 = outputDir + "/" + res_output
  save_json_info(res_output2, res_report)

  json_test_request = get_json_info(re_output2)
  json_test_respond = get_json_info(re_output2)
  # time.sleep(16)

  if json_test_request["resource"] == json_test_respond["resource"]:
    return True
  else:
    return False

  # print(res_report)
  # Save the res_report


def main():
  if not os.path.isdir(dataDir):
    print(dataDir, "isn't a directory")
    sys.exit(1)

  files = os.listdir(dataDir)
  passed = 0
  failed = 0
  cnt = 0
  for dirpath, dirnames, filenames in os.walk(dataDir):
    for x in files:
      if fnmatch.fnmatch(x, "VirusShare*"):
        malware_file = os.path.join(dirpath, x)
        cnt = cnt + 1
        # Test Info
        # print(malware_file)
        # mlwarefile_path = os.path.join( os.getcwd(), 'VirusShare_0a03b61f1f885a402eff7224a9798048.sh')
        file_basename = os.path.basename(os.path.normpath(malware_file))
        output_path = file_basename[:-3] + "_que.json"
        output_path = outputDir + "/" + output_path
        if os.path.exists(output_path):
          print(cnt, " Passed: ", output_path)
          continue

        retcode = get_query(malware_file)

        if retcode == False:
          print("\tFAILED to parser the bash code.", x)
          failed += 1
          os.remove(output2)
        else:
          print(cnt, ": ", x, " passed ", format(time.strftime("%H:%M:%S")))
          passed += 1
          # os.remove(malware_file)
  print(passed, " bash scripts passed")
  print(failed, " bash scripts failed")


if __name__ == "__main__":
  # mlwarefile_path = os.path.join( os.getcwd(), 'VirusShare_0a03b61f1f885a402eff7224a9798048.sh')
  # get_query(mlwarefile_path)
  main()
