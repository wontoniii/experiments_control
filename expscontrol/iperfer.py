'''
Definition
'''

from cmd_exec import Command, RemoteCommand, RemoteNode
import argparse
import re

class IPerferer:
  V_COMMANDS = {"2": "iperf", "3": "iperf3"}

  def __int__(self):
    """

    :return:
    """
    self.totaltime = 0
    self.UDP = False
    self.bandwidth = 0
    self.host = None
    self.dstHost = None
    self.version = "2"
    self.packetSize = 0
    self.json = True
    self.reverse = False
    self.configured = False

  def config(self, dstHost=None, totaltime=0, UDP=False, bandwidth=1, host=None, version='2', packetSize=0, json=True, reverse=False):
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
      self.host = host
      self.command.setRemoteNode(host)
    self.dstHost = dstHost
    self.totaltime = totaltime
    self.UDP = UDP
    self.bandwidth = bandwidth
    if version not in IPerferer.V_COMMANDS.keys():
      raise ValueError("Incorrect version option")
    self.version = version
    self.packetSize = packetSize
    self.json = json
    self.reverse = reverse
    self.configured = True

  def processOutput(self):
    """

    :param output:
    :return:
    """

  def prepareCommand(self):
    """

    :return:
    """
    cmd = IPerferer.V_COMMANDS[self.version]
    if self.UDP:
      cmd += " -u -b " + str(self.bandwidth)
    if self.totaltime > 0:
      cmd += " -t " + str(self.totaltime)
    if self.packetSize > 0:
      cmd += " -l " + str(self.packetSize)
    if self.json and self.version == "3":
      cmd += " -J"
    if self.reverse and self.version == "3":
      cmd += " -R"
    cmd += " -c " + self.dstHost
    self.command.setCmd(cmd)

  def runSync(self):
    """
    Run pinger waiting for it to complete before returning control
    :return:
    """
    self.prepareCommand()
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
    self.prepareCommand()
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

# def main():
#   """
#   Run a single pinger or processes the output from a file
#   :return:
#   """
#   parser = argparse.ArgumentParser()
#   parser.add_argument('-d', '--dest', type=str, required=False, help="Destination for the pings")
#   parser.add_argument('-s', '--src', type=str, required=False, help="Source for the pings", default=None)
#   parser.add_argument('-c', '--count', type=int, required=False, help="Number of pings", default=10)
#   parser.add_argument('-i', '--interval', type=float, required=False, help="Period of pings", default=1)
#   parser.add_argument('-I', '--interface', type=str, required=False, help="Interface to be used", default=None)
#   parser.add_argument('-f', '--file-name', type=str, required=False, help="Files to process the ping output from. "
#                                                                            "Makes the other arguments irrelevant",
#                       default=None)
#   args = vars(parser.parse_args())
#
#   if args["file_name"] is not None:
#     pinger = Pinger()
#     pinger.processFromFile(args["file_name"])
#     pinger.printRawOutput()
#     pinger.printResults()
#   elif args["dest"] is not None:
#     pinger = Pinger()
#     if args["src"] is not None:
#       src = RemoteNode()
#       src.setHost(args["src"])
#     else:
#       src = None
#     pinger.config(dst=args["dest"], src=src, count=args["count"], interval=args["interval"],
#                   interface=args["interface"])
#     if pinger.runSync() < 0:
#       print "error running ping"
#       pinger.printRawOutput()
#       return
#     pinger.printRawOutput()
#     pinger.printResults()
#   else:
#     print "You need to provide a destination or a file!"
#     parser.print_help()
#
# if __name__ == "__main__":
#   main()