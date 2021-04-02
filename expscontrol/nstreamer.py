'''
by: wontoniii
    wontoniii@gmail.com

Driver class by: Arash Molavi Kakhki
    Northeastern University
    arash.molavi@gmail.com
    ALL RIGHTS RESERVED

Description:

Notes: It is not possible to run it remotely as it requires a desktop environment for Chrome to run
'''

import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from expscontrol.utils import *
import argparse


class Driver():
  def __init__(self):
    self.driver = None

  def fireUp(self, chromeDriverPath, extensionPath=None, userDir=None, dataDir=None, useSocksProxy=False,
             userData=None, disableComponentUpdate=False, enableQUIC=False):
    userData=True
    args = []
    chromeOptions = webdriver.ChromeOptions()

    if useSocksProxy:
      args += ['--proxy-pac-url=file://{}'.format(os.path.abspath('netflix.pac'))]

    if userDir:
      if userDir == 'tmp':
        userDir = '/tmp/tmpUserDir'
      args += ['--user-data-dir={}'.format(userDir)]
    else:
      chromeOptions.add_experimental_option('excludeSwitches', ['user-data'])

    if dataDir:
      if dataDir == 'tmp':
        dataDir = '/tmp/tmpDataDir'
      args += ['--data-path={}'.format(dataDir)]
    else:
      chromeOptions.add_experimental_option('excludeSwitches', ['data-path'])

    if disableComponentUpdate:
      args += ['--disable-component-update']
    else:
      chromeOptions.add_experimental_option('excludeSwitches', ['disable-component-update'])

    if extensionPath:
      args += ['--load-extension={}'.format(extensionPath)]

    if enableQUIC:
      args += ['--enable-quic']

    for arg in args:
      chromeOptions.add_argument(arg)

    self.driver = webdriver.Chrome(executable_path=chromeDriverPath, chrome_options=chromeOptions)

  def get(self, url):
    self.driver.get(url)

  def closeAllTabs(self):
    for handle in self.driver.getAllWindowHandles():
      self.driver.switchTo().window(handle)
      self.driver.close()

  def closeTab(self):
    self.driver.close()

  def backToBrowse(self):
    self.driver.find_element_by_xpath("//*[@id='netflix-player']/a").click()

  def quit(self):
    self.driver.close()
    self.driver.quit()


class Streamer():
  PLATFORM_VARS = {
    "mac": {
      "driverpath": "chromeDrivers\win\chromedriver.exe"
    },
    "win": {
      "driverpath": "chromeDrivers\win\chromedriver.exe"
    },
    "linux": {
      "driverpath": "chromeDrivers\win\chromedriver.exe"
    }
  }

  def __init__(self):
    """

    """
    self.lenght = 600
    self.URL = 'https://www.netflix.com/watch/70165197'
    self.driverPath = ""
    self.driver = None
    self.login = False
    self.profile = None
    self.platform = get_platform()

  def config(self, length=10, URL=None, login=False, profile=None, platform=get_platform(), driverPath=None, enableQUIC=True):
    """
    Confgures the streamer
    :param length: Duration in seconds of the stream
    :param URL: The URL to stream
    :param login: Whether login is necessary for the app
    :param profile: Profile to be used by chrome
    :param platform: Which platform is this
    :return:
    """
    if length is not None:
      self.lenght = length
    if URL is not None:
      self.URL = URL
    if login is not None:
      self.login = login
    if profile is not None:
      self.profile = profile
    if platform is not None:
      self.platform = platform
    if driverPath is not None:
      self.driverPath = driverPath
    else:
      self.driverPath = Streamer.PLATFORM_VARS[self.platform]["driverpath"]
    self.enableQUIC = enableQUIC

  def doLogIn(self, app, username=None, password=None):
    if app.lower() == 'netflix':
      loginURL = 'https://www.netflix.com/Login'

      p = self.driver.getMultiprocess(loginURL)

      if self.driver.driver.current_url == loginURL.replace('Login', 'browse'):
        print('\tWas already logged in!')
        return True

      if username and password:
        try:
          self.driver.driver.find_element_by_name('email').send_keys(username)
        except selenium.common.exceptions.NoSuchElementException:
          self.driver.driver.find_element_by_name('emailOrPhoneNumber').send_keys(username)
        time.sleep(0.5)
        self.driver.driver.find_element_by_name('password').send_keys(password)
        time.sleep(0.5)
        self.driver.driver.find_element_by_xpath("//button[@type='submit']").click()
        return True

      else:
        print ('\n\nYou are not logged in!')
        print ('user the following switches to enter your credentials for login: (your credentials will ONLY be submitted to Netflix)')
        print ('--username=[your username] --password=[your password]')
        return False

  def moveMouse(self):
    """

    :return:
    """
    # Actions
    # action = new
    # Actions(webDriver);
    #
    # // First, go
    # to
    # your
    # start
    # point or Element
    # action.moveToElement(startElement);
    # action.perform();
    #
    # // Then, move
    # the
    # mouse
    # action.moveByOffset(x, y);
    # action.perform();
    #
    # // Then, move
    # again(you
    # can
    # implement
    # your
    # one
    # code
    # to
    # follow
    # your
    # curve...)
    # action.moveByOffset(x2, y2);
    # action.perform();
    #
    # // Finaly, click
    # action.click();
    # action.perform();

  def runSync(self):
    """

    :return:
    """
    if self.driver is not None:
      raise AttributeError("The driver already running")
    self.driver = Driver()
    chromeDriverPath = os.path.abspath(self.driverPath)
    self.driver.fireUp(chromeDriverPath, userDir=self.profile, enableQUIC=self.enableQUIC)
    if self.login:
      self.doLogIn()
    self.driver.get(self.URL)
    time.sleep(self.lenght)
    self.driver.get('http://google.com')
    #Make sure the extension uploads the file
    time.sleep(2)
    self.driver.quit()

  def runAsync(self):
    """
    NOT implemented for now
    :return:
    """
    if self.driver is not None:
      raise AttributeError("The driver already running")
    self.driver = Driver()
    chromeDriverPath = os.path.abspath(self.driverPath)
    self.driver.fireUp(chromeDriverPath, userDir=self.profile, enableQUIC=self.enableQUIC)
    if self.login:
      self.doLogIn()
    self.driver.get(self.URL)

  def stopAsync(self):
    """
    If running stops the driver
    :return:
    """
    self.driver.get('http://google.com')
    # Make sure the extension uploads the file
    time.sleep(2)
    self.driver.quit()

  def openWindow(self):
    """

    :return:
    """
    if self.driver is not None:
      raise AttributeError("The driver is already running")
    self.driver = Driver()
    chromeDriverPath = os.path.abspath(self.driverPath)
    self.driver.fireUp(chromeDriverPath, userDir=self.profile, enableQUIC=self.enableQUIC)
    time.sleep(self.lenght)
    self.driver.quit()

def main():
  """
  Run a single stream
  :return:
  """
  #def config(self, length=10, URL=None, login=False, profile=None, platform=get_platform(), driverPath=None):
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--page', type=str, required=True, help="Page to stream")
  parser.add_argument('-P', '--profile', type=str, required=False, help="Custom profile folder", default="")
  parser.add_argument('-d', '--driver', type=str, required=False, help="Path to drivers' folder", default=None)
  parser.add_argument('-l', '--length', type=int, required=False, help="Length of the stream in seconds", default=10)
  parser.add_argument('-L', '--login', action='store_true', help="Whether a login is required")
  parser.add_argument('-o', '--open', action='store_true', help="Starts a chromium session without doing anything")
  args = vars(parser.parse_args())

  streamer = Streamer()
  streamer.config(length=args["length"], profile=args["profile"], URL=args["page"], login=args["login"],
                driverPath=args["driver"])
  if args["open"]:
    streamer.openWindow()
  else:
    streamer.runSync()

if __name__ == "__main__":
  main()