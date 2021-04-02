'''

'''

import subprocess, shlex
from subprocess import Popen


class NoCommandDefinedException(BaseException):
  def __init__(self, args):
    """

    """
    BaseException.__init__(self, args)


class NoHostDefinedException(BaseException):
  def __init__(self, args):
    """

    """
    BaseException.__init__(self, args)


class Command:
  def __init__(self):
    """

    """
    self.cmd = None
    self.outcode = None
    self.stdout = None
    self.stderr = None
    self.running = False
    self.popen = None
    self.async = False

  def setCmd(self, cmd):
    """

    :param cmd:
    :return:
    """
    self.cmd = cmd

  def getCmd(self):
    """

    :return:
    """
    return self.cmd

  def isRunning(self):
    """

    :return:
    """
    return self.running

  def runSync(self):
    """

    :return:
    """
    if self.cmd == None:
      raise NoCommandDefinedException()
    print("Executing: " + self.cmd)
    # args = self.cmd.split()
    args = shlex.split(self.cmd)
    # args = self.cmd
    try:
      self.running = True
      self.stdout = subprocess.check_output(args)
      self.running = False
      self.outcode = 0
      return 0
    except subprocess.CalledProcessError as ex:
      self.stdout = ex.output
      self.outcode = ex.returncode
      return -1

  def runAsync(self):
    """

    :return:
    """
    if self.cmd == None:
      raise NoCommandDefinedException()
    print("Executing: " + self.cmd)
    # args = self.cmd.split()
    args = shlex.split(self.cmd)
    # args = self.cmd
    try:
      self.async = True
      self.popen = Popen(args, stdout=subprocess.PIPE)
      self.running = True
      return 0
    except subprocess.CalledProcessError as ex:
      self.stdout = ex.output
      self.outcode = ex.returncode
      return -1
    except OSError as ex:
      self.outcode = ex.errno
      self.stdout = ex.message
      return -1

  def isAsyncDone(self):
    """

    :return:
    """
    if self.async is False:
      raise BaseException("Checking a non async process")
    if self.running is False:
      return True
    if self.popen is None:
      return True
    else:
      self.outcode = self.popen.poll()
      if self.outcode is None:
        return False
      else:
        self.stdout = self.popen.communicate()[0]
        return True

  def stopAsync(self):
    """

    :return:
    """
    if self.async is False:
      raise BaseException("Checking a non async process")
    if self.running is False:
      return False
    if self.popen is None:
      return False
    self.outcode = self.popen.poll()
    if self.outcode is None:
      self.popen.kill()

  def getStdout(self):
    """

    :return:
    """
    return self.stdout

  def getStderr(self):
    """

    :return:
    """
    return self.stderr

  def getOutcode(self):
    """

    :return:
    """
    return self.getOutcode()

class RemoteNode:
  def __init__(self):
    """

    """
    self.host = None
    self.key = None

  def setHost(self, host):
    """

    :param host:
    :return:
    """
    self.host = host

  def getHost(self):
    """

    :return:
    """
    return self.host

  def setKey(self, key):
    """

    :return:
    """
    self.key = key

  def getKey(self):
    """

    :return:
    """
    return self.key


class RemoteCommand(Command):
  def __init__(self):
    """

    """
    Command.__init__(self)
    self.remoteNode = None
    self.baseCmd = None

  def setRemoteNode(self, node):
    """

    :param node:
    :return:
    """
    self.remoteNode = node

  def getRemoteNode(self):
    """

    :return:
    """
    return self.remoteNode

  def setCmd(self, cmd):
    """

    :param cmd:
    :return:
    """
    self.baseCmd = cmd

  def getCmd(self):
    """

    :return:
    """
    return self.baseCmd

  def runSync(self):
    """

    :return:
    """
    if self.remoteNode is None:
      raise NoHostDefinedException()
    cmd = 'ssh'
    if self.remoteNode.getKey() != None:
      cmd += ' -i ' + self.remoteNode.getKey()
    cmd += ' ' + self.remoteNode.getHost() + ' "' + self.baseCmd + '"'
    Command.setCmd(self, cmd)
    return Command.runSync(self)

  def runAsync(self):
    """

    :return:
    """
    if self.remoteNode is None:
      raise NoHostDefinedException()
    cmd = 'ssh'
    if self.remoteNode.getKey() != None:
      cmd += ' -i ' + self.remoteNode.getKey()
    cmd += ' ' + self.remoteNode.getHost() + ' "' + self.baseCmd + '"'
    Command.setCmd(self, cmd)
    return Command.runAsync(self)