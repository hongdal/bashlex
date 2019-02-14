import os, time, sys
import subprocess
import fnmatch

bright_level = 1.5

pid = ''
word = ''
display = ''

test_dir = "res/"
out_dir = "out/"

def trace(linux_command, out_file):
  linux_command = linux_command.strip()
  tmp = linux_command.split(" ")
  command = "strace -ttt -T -f -o " + out_file + " " + linux_command
  sp = subprocess.Popen(
      command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def tracebuiltin(linux_command, out_file):
  linux_command = linux_command.strip()
  tmp = linux_command.split(" ")
  command = "strace -ttt -T -f -o " + out_file + " bash -c " + linux_command
  sp = subprocess.Popen(
      command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def visitTestDir(dir_path, out_path):
  if os.path.isdir(dir_path):
    for dirpath, dirnames, filenames in os.walk(dir_path):
      for x in filenames:
        if fnmatch.fnmatch(x, "*.cmd"):
          command_file = os.path.join(dirpath, x)
          file = open(command_file)
          basename = os.path.basename(command_file)[:-4]
          test_command = "type " + basename
          
          sp = subprocess.Popen(
              test_command,
              shell=True,
              stdout=subprocess.PIPE,
              stderr=subprocess.STDOUT)
          out_data = sp.stdout.read()
          out_data = out_data.decode("utf-8")

          builtin = False
          if out_data.find("builtin") >= 0:
            builtin = True
          while 1:
            lines = file.readlines(50)
            count = 0
            if not lines:
              break
            for line in lines:
              count += 1
              basename = os.path.basename(command_file)[:-4]
              out_file = out_path + basename + "-" + str(count) + ".log"
              if builtin:
                tracebuiltin(line, out_file)
              else:
                trace(line, out_file)


# def filter(line):
#   if word in line:
#     print line
#     return True
#   return False

# def taskend(line):
#   if '+++ exited with' in line:
#     return True
#   return False

# def screen_flicker(brightness, interval):
#   subprocess.Popen(
#       ('xrandr --output ' + display + ' --brightness ' +
#        str(brightness)).split(),
#       stdout=subprocess.PIPE,
#       stderr=subprocess.PIPE)
#   time.sleep(interval)

# def notify():
#   for i in xrange(6):
#     time.sleep(0.1)
#     print '\a'

#   print '************************RETARD ALERT************************'
#   try:
#     screen_flicker(bright_level, 0.1)
#     screen_flicker(1.0, 0.3)
#   finally:
#     screen_flicker(1.0, 0)

# def init_setting():
#   xrandr_p = subprocess.Popen(
#       'xrandr -q'.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#   for line in iter(xrandr_p.stdout.readline, ''):
#     if ' connected' in line:
#       global display
#       display = line.split()[0]
#       return
#     if not line: break


def main():
  pwd_path = os.getcwd()
  test_path = os.path.join(pwd_path, test_dir)
  out_path = os.path.join(pwd_path, out_dir)
  visitTestDir(test_path, out_path)


if __name__ == "__main__":
  main()
