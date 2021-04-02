import sys, os

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

