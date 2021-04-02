'''
Definition
'''

from expscontrol.cmd_exec import Command, RemoteCommand, RemoteNode
import argparse
import re
import sys
import pingparser
from expscontrol.pinger import Pinger

class MPPinger(Pinger):


  def __int__(self):
    """

    :return:
    """
    self.train = False
    self.trainS = 0
    self.trainI = 0
    self.gamma = 0
    self.pattern = []

  def config(self, dst=None, src=None, count=100, interval=1, interface=None,
             train=False, trainS=0, trainI=0, gamma=0, pattern=None):
    """

    :param dst:
    :param src:
    :param count:
    :param interval:
    :param interface:
    :param train:
    :param trainS:
    :param trainI:
    :return:
    """
    Pinger.config(self, dst=None, src=None, count=100, interval=1, interface=None)
    self.train = train
    self.trainS = trainS
    self.trainI = trainI
    self.gamma = gamma
    self.pattern = pattern

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
    #mpping requires
    cmd = "sudo mpping "
    cmd += self.dstHost
    if self.interval > 0:
      cmd += " -i " + str(self.interval)
    if self.count > 0:
      cmd += " -c " + str(self.count)
    if self.interface is not None:
      cmd += " -s " + self.interface
    if self.train and self.trainS > 0:
      cmd += " -t " + str(self.trainS)
    if self.trainI > 0:
      cmd += " -I " + str(self.trainI)
    if self.gamma > 0:
      cmd += " -g " + str(self.gamma)
    if self.pattern is not None:
      cmd += " -p "
      i = 0
      for value in self.pattern:
        if i > 0:
          cmd += ","
        cmd += str(value)
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
    # mpping requires
    cmd = "sudo mpping "
    cmd += self.dstHost
    if self.interval > 0:
      cmd += " -i " + str(self.interval)
    if self.count > 0:
      cmd += " -c " + str(self.count)
    if self.interface is not None:
      cmd += " -s " + self.interface
    if self.train and self.trainS > 0:
      cmd += " -t " + str(self.trainS)
    if self.trainI > 0:
      cmd += " -I " + str(self.trainI)
    if self.gamma > 0:
      cmd += " -g " + str(self.gamma)
    if len(self.pattern) > 0:
      cmd += " -p "
      i = 0
      for value in self.pattern:
        if i > 0:
          cmd += ","
        cmd += str(value)
    self.command.setCmd(cmd)
    self.command.runAsync()

def processTrain():
  """
  Process comma separated int values and returns list
  :return:
  """



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
  parser.add_argument('-s', '--source', type=str, required=False, help="IP address to be used", default=None)
  parser.add_argument('-T', '--train', action='store_true', help="Active train of consecutive pings")
  parser.add_argument('-t', '--trainS', type=int, required=False, help="Number of pings in a train", default=0)
  parser.add_argument('-I', '--trainI', type=int, required=False, help="Interval in between pings in a train", default=0)
  parser.add_argument('-g', '--gamma', type=int, required=False, help="Gamma for uniform distribuition "
                                                                      "in between pings", default=0)
  parser.add_argument('-p', '--pattern', type=processTrain(), required=False, help="Sizes of pings", default=None)
  parser.add_argument('-f', '--file-name', type=str, required=False,
                      help="Files to process the ping output from. Makes the other arguments irrelevant", default=None)
  args = vars(parser.parse_args())

  if args["file_name"] is not None:
    pinger = MPPinger()
    pinger.processFromFile(args["file_name"])
    pinger.printRawOutput()
    pinger.printResults()
  elif args["dest"] is not None:
    pinger = MPPinger()
    if args["src"] is not None:
      src = RemoteNode()
      src.setHost(args["src"])
    else:
      src = None
    pinger.config(dst=args["dest"], src=src, count=args["count"], interval=args["interval"],
                  interface=args["source"], train=args["train"], trainS=args["trainS"],
                  trainI=args["trainI"], gamma=args["gamma"], pattern=args["pattern"])
    if pinger.runSync() < 0:
      print ("error running ping")
      pinger.printRawOutput()
      return
    pinger.printRawOutput()
    pinger.printResults()
  else:
    print ("You need to provide a destination or a file!")
    parser.print_help()

if __name__ == "__main__":
  main()