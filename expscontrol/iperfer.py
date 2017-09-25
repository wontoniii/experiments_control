'''
Definition
'''

from cmd_exec import Command, RemoteCommand, RemoteNode
import argparse
import re

class IPerferer:

  def __int__(self):
    """

    :return:
    """
    self.totaltime = 0
    self.UDP = False
    self.bandwidth = 0
    self.host = None
    self.dstHost = None
    self.version = None

  def config(self, dstHost=None, totaltime=0, UDP=False, bandwidth=1, host=None, version='3'):
    """

    :param latency:
    :param loss:
    :param host:
    :return:
    """
    if host is None:
      self.command = Command()
    else:
      self.command = RemoteCommand()
      self.host = RemoteNode()
      self.host.setHost(host)
      self.command.setRemoteNode(host)
    self.dstHost = dstHost
    self.totaltime = totaltime
    self.UDP = UDP
    self.bandwidth = bandwidth
    self.version = version

  def processOutput(self):
    """

    :param output:
    :return:
    """

  def runSync(self):
    """
    Run pinger waiting for it to complete before returning control
    :return:
    """
    cmd = "iperf"+self.version
    if self.UDP:
      cmd += " -u -b " + str(self.bandwidth)
    if self.totaltime > 0:
      cmd += " -t " + str(self.totaltime)
    cmd += " -c " + self.dstHost
    self.command.setCmd(cmd)
    if self.command.runSync() == 0:
      self.rawOutput = self.command.getStdout()
      self.processOutput()
      return 0
    else:
      self.rawOutput = self.command.getStdout()
      return -1

  def runAsync(self, callback=None):
    """
    Run pinger asynchronously and calls callback once finished
    Not implemented for now
    :param callback:
    :return:
    """
    cmd = "iperf3"
    if self.UDP:
      cmd += " -u -b " + str(self.bandwidth)
    if self.totaltime > 0:
      cmd += " -t " + str(self.totaltime)
    cmd += " -c " + self.dstHost
    self.command.setCmd(cmd)
    if self.command.runAsync() < 0:
      self.rawOutput = self.command.getStdout()
      self.processOutput()
      self.printRawOutput()
      return -1
    else:
      self.rawOutput = ""

  def stopAsync(self):
    """

    :return:
    """
    return self.command.stopAsync()

  def processFromFile(self, filename):
    """

    :param filename:
    :return:
    """
    with open(filename, "r") as myfile:
      self.rawOutput = myfile.read()
      myfile.close()
    self.processOutput()

  def printResults(self):
    """

    :return:
    """

  def printRawOutput(self):
    """

    :return:
    """
    print self.rawOutput