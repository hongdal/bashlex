#!/usr/bin/python

import os, sys
import fnmatch
import subprocess
from subprocess import PIPE
import filecmp

dataDir = os.path.join( os.getcwd(), '0_data/bashData/allscripts')
outputDir = os.path.join( os.getcwd(), '0_data/nodeData')

if not os.path.isdir( dataDir ):
  print dataDir, "isn't a directory"
  sys.exit( 1 )

files = os.listdir( dataDir )
passed = 0
failed = 0

for dirpath, dirnames, filenames in os.walk( dataDir ) :
  for x in files:
    if fnmatch.fnmatch(x, "VirusShare*"):
      malware_file = os.path.join(dirpath, x)
      output = x+".node"
      output2 = outputDir+"/"+output
      retcode = subprocess.call("python2.7 parser.py "+malware_file+">"+output2, shell=True)
      if retcode != 0:
        print "\tFAILED to parser the bash code.", x
        failed += 1
        os.remove(output2)
      else: 
        print x," passed"
        passed += 1
        os.remove(malware_file)
print passed, " bash scripts passed"
print failed, " bash scripts failed"
