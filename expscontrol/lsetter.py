'''
Definition
'''

from cmd_exec import Command, RemoteCommand
import argparse
import re


#ssh root@node19-20 "tc qdisc del dev eth0.1002 root; \
#                       tc qdisc add dev eth0.1002 root netem delay ${lat}ms"
#ssh root@node20-19 "tc qdisc add dev wlan0 root netem loss 6% 25%"

class LatencySetter:
  def __int__(self):
    """

    :return:
    """
    self.latency = None
    self.capacity = None
    self.lossavg = None
    self.losssd = None
    self.interface = None
    self.host = None
    self.sudo = False

  def config(self, interface="eth0", latency=0, lossavg=0, losssd=0, host=None, sudo=True, capacity=0):
    """

    :param interface: name of interface to apply the policy to
    :param latency: latency to apply in ms
    :param lossavg:
    :param losssd:
    :param host: RemoteHost object
    :param sudo: if it has to be run as sudo
    :param capacity: max capacity in kbps
    :return:
    """
    if host is None:
      self.command = Command()
    else:
      self.command = RemoteCommand()
      self.host = host
      self.host.setHost(host)
      self.command.setRemoteNode(host)
    self.interface = interface
    self.capacity = capacity
    self.latency = latency
    self.lossavg = lossavg
    self.losssd = losssd
    self.sudo = sudo

  def processOutput(self):
    """

    :param output:
    :return:
    """

  def createQDisc(self):
    """

    :return:
    """
    if (self.losssd is None or self.losssd <= 0) and \
      (self.lossavg is None or self.lossavg <= 0) and \
      (self.latency is None or self.latency <= 0):
      raise ValueError("Wrong values, set at least one value to >0")
    cmd = ""
    if self.sudo:
      cmd += "sudo"
    cmd += " tc qdisc add dev " + self.interface + " root netem"
    if self.latency > 0:
      cmd += " delay " + str(self.latency) + "ms"
    if self.capacity > 0:
      cmd += " rate " + str(self.capacity) + "kbit"
    if self.lossavg > 0:
      cmd += " loss {:d}%".format(self.lossavg)
      if self.losssd > 0:
        cmd += " {:d}%".format(self.losssd)
    if self.command.runSync() == 0:
      self.rawOutput = self.command.getStdout()
      self.processOutput()
      return 0
    else:
      self.rawOutput = self.command.getStdout()
      return -1


  def deleteQDisc(self):
    """

    :return:
    """
    cmd = ""
    if self.sudo:
      cmd += "sudo"
    cmd += " tc qdisc del dev " + self.interface + " root"
    if self.command.runSync() == 0:
      self.rawOutput = self.command.getStdout()
      self.processOutput()
      return 0
    else:
      self.rawOutput = self.command.getStdout()
      return -1

  def printRawOutput(self):
    """

    :return:
    """
    print self.rawOutput