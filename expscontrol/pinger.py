'''
Definition
'''

from expscontrol.cmd_exec import Command, RemoteCommand, RemoteNode
import argparse
import re
import sys
import pingparser

class Pinger:


  def __int__(self):
    """

    :return:
    """
    self.command = None
    self.srcHost = None
    self.dstHost = None
    self.interface = None
    self.count = None
    self.interval = None
    self.rawOutput = None
    self.rtts = []
    self.tot = None
    self.rec = None
    self.loss = None
    self.std = None
    self.min = None
    self.max = None
    self.avg = None

  def config(self, dst=None, src=None, count=100, interval=1, interface=None):
    """

    :param dst:
    :param remote:
    :param src:
    :param count:
    :param interval:
    :param interface:
    :return:
    """
    self.command = Command()
    if src is None:
      self.command = Command()
    else:
      self.command = RemoteCommand()
      self.srcHost = src
      self.command.setRemoteNode(self.srcHost)
    self.dstHost = dst
    self.interval = interval
    self.count = count
    self.interface = interface

  def processOutput(self):
    """

    :param output:
    :return:
    """
    self.rtts = re.findall(r'time=(\d+.\d+)', self.rawOutput)
    self.rtts[:] = [float(x) for x in self.rtts]
    results = pingparser.parse(self.rawOutput)
    self.tot = int(results["sent"])
    self.lost = self.tot - int(results["received"])
    self.rec = int(results["received"])
    self.max = float(results["maxping"])
    self.min = float(results["minping"])
    self.std = float(results["jitter"])
    self.avg = float(results["avgping"])
    self.loss = float(results["packet_loss"])

  def runSync(self):
    """
    Run pinger waiting for it to complete before returning control
    :return:
    """
    if self.interval < 1:
      cmd = "sudo ping "
    else:
      cmd = "ping "
    cmd += self.dstHost
    if self.interval > 0:
      cmd += " -i " + str(self.interval)
    if self.count > 0:
      cmd += " -c " + str(self.count)
    if self.interface is not None:
      cmd += " -I " + self.interface
    self.command.setCmd(cmd)
    if self.command.runSync() == 0:
      self.rawOutput = self.command.getStdout()
      self.processOutput()
      return 0
    else:
      self.rawOutput = self.command.getStdout()
      self.processOutput()
      return -1

  def runAsync(self, callback=None):
    """
    Run pinger asynchronously and calls callback once finished
    Not implemented for now
    :param callback:
    :return:
    """
    if self.interval < 1:
      cmd = "sudo ping "
    else:
      cmd = "ping "
    cmd += self.dstHost + " -i " + str(self.interval) + " -c " + str(self.count)
    if self.interface is not None:
      cmd += " -I " + self.interface
    self.command.setCmd(cmd)
    self.command.runAsync()

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
    #print the results
    print(str(self.tot)+" packets transmitted, "+str(self.rec)+" packets received, "+\
      str(self.loss)+" packet loss")
    print("round-trip min/avg/max/stddev = "+str(self.min)+"/"+str(self.avg)+"/"+str(self.max)+"/"+str(self.std)+" ms")

  def printRawOutput(self):
    """

    :return:
    """
    print(self.rawOutput)

  def printRawToFilew(self, outfolder, outfile):
    """

    :return:
    """
    with open(outfolder+outfile, "w") as myfile:
      myfile.write(self.rawOutput)
      myfile.close()


def main():
  """
  Run a single pinger or processes the output from a file
  :return:
  """
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--dest', type=str, required=False, help="Destination for the pings")
  parser.add_argument('-s', '--src', type=str, required=False, help="Source for the pings", default=None)
  parser.add_argument('-c', '--count', type=int, required=False, help="Number of pings", default=10)
  parser.add_argument('-i', '--interval', type=float, required=False, help="Period of pings", default=1)
  parser.add_argument('-I', '--interface', type=str, required=False, help="Interface to be used", default=None)
  parser.add_argument('-f', '--file-name', type=str, required=False, help="Files to process the ping output from. "
                                                                           "Makes the other arguments irrelevant",
                      default=None)
  args = vars(parser.parse_args())

  if args["file_name"] is not None:
    pinger = Pinger()
    pinger.processFromFile(args["file_name"])
    pinger.printRawOutput()
    pinger.printResults()
  elif args["dest"] is not None:
    pinger = Pinger()
    if args["src"] is not None:
      src = RemoteNode()
      src.setHost(args["src"])
    else:
      src = None
    pinger.config(dst=args["dest"], src=src, count=args["count"], interval=args["interval"],
                  interface=args["interface"])
    if pinger.runSync() < 0:
      print("error running ping")
      pinger.printRawOutput()
      return
    pinger.printRawOutput()
    pinger.printResults()
  else:
    print("You need to provide a destination or a file!")
    parser.print_help()

if __name__ == "__main__":
  main()