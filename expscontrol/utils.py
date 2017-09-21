import sys, os, ConfigParser, math, json, time, subprocess, commands, random, string, logging, logging.handlers, socket, StringIO

def curlDownload(url, outfile='/dev/null'):
  cmd = ['curl', '-k', '\"{}\"'.format(url), '>', outfile]
  os.system(' '.join(cmd))

  class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
      if cls not in cls._instances:
        cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
      return cls._instances[cls]

def get_platform():
  if sys.platform == "linux" or sys.platform == "linux2":
    return "linux"
  elif sys.platform == "darwin":
    return "mac"
  elif sys.platform == "win32":
    return "win"


# class Configs(object):
#   '''
#   This object holds all configs
#
#   BE CAREFUL: it's a singleton!
#   '''
#   __metaclass__ = Singleton
#   _Config = None
#   _configs = {}
#
#   def __init__(self, config_file=None):
#     self._Config = ConfigParser.ConfigParser()
#     self.action_count = 1
#     self._maxlen = 0
#     if config_file != None:
#       read_config_file(config_file)
#
#   def read_config_file(self, config_file):
#     with open(config_file, 'r') as f:
#       while True:
#         try:
#           l = f.readline().strip()
#           if l == '':
#             break
#         except:
#           break
#
#         a = l.partition('=')
#
#         if a[2] in ['True', 'true']:
#           self.set(a[0], True)
#         elif a[2] in ['False', 'false']:
#           self.set(a[0], False)
#         else:
#           try:
#             self.set(a[0], int(a[2]))
#           except ValueError:
#             try:
#               self.set(a[0], float(a[2]))
#             except ValueError:
#               self.set(a[0], a[2])
#
#   def read_args(self, args):
#     self.set('000-scriptName', args[0])
#     for arg in args[1:]:
#       a = ((arg.strip()).partition('--')[2]).partition('=')
#
#       if a[0] == 'ConfigFile':
#         self.read_config_file(a[2])
#
#       if a[2] in ['True', 'true']:
#         self.set(a[0], True)
#
#       elif a[2] in ['False', 'false']:
#         self.set(a[0], False)
#
#       else:
#         try:
#           self.set(a[0], int(a[2]))
#         except ValueError:
#           try:
#             self.set(a[0], float(a[2]))
#           except ValueError:
#             self.set(a[0], a[2])
#             #         if 'ConfigFile' in self._configs:
#             #             self.read_config_file(self._configs['ConfigFile'])
#
#   def check_for(self, list_of_mandotary):
#     try:
#       for l in list_of_mandotary:
#         self.get(l)
#     except:
#       print '\nYou should provide \"--{}=[]\"\n'.format(l)
#       sys.exit(-1)
#
#   def get(self, key):
#     return self._configs[key]
#
#   def is_given(self, key):
#     try:
#       self._configs[key]
#       return True
#     except:
#       return False
#
#   def set(self, key, value):
#     self._configs[key] = value
#     if len(key) > self._maxlen:
#       self._maxlen = len(key)
#
#   def show(self, key):
#     print key, ':\t', value
#
#   def show_all(self):
#     for key in sorted(self._configs):
#       print '\t', key.ljust(self._maxlen), ':', self._configs[key]
#
#   def __str__(self):
#     return str(self._configs)
#
#   def reset_action_count(self):
#     self._configs['action_count'] = 0
#
#   def reset(self):
#     _configs = {}
#     self._configs['action_count'] = 0
