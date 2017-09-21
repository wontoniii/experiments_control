'''
Definition
'''

from cmd_exec import Command, RemoteCommand, RemoteNode
import argparse
import re

class LatencySetter:
  def __int__(self):
    """

    :return:
    """
    self.latency = None
    self.loss = None
    self.host = None

  def config(self, latency=0, loss=0, host=None):
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
    self.latency = latency
    self.loss = loss

  def processOutput(self):
    """

    :param output:
    :return:
    """

  def setLatency(self):
    """

    :return:
    """

  def cancelLatency(self):
    """

    :return:
    """

  def printRawOutput(self):
    """

    :return:
    """
    print self.rawOutput