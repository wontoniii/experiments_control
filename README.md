# SSH based experiment control management

Allows to execute simple experiments on local and remote hosts.

## Installation

From GirHub:

``pip install --upgrade 'git+https://github.com/wontoniii/experiments_control.git'``

From local sources:

``pip install --upgrade ./``

Browser streaming is based on selenium. Requires the download of the interface drivers at: 

``http://selenium-python.readthedocs.io/installation.html#drivers``

And the installation of the selenium library:

``pip install selenium``

Further, the pinger module uses `https://github.com/ssteinerx/pingparser` for parsing.

NOTE: Windows supports expects cygwin to be installed (i.e. ssh to be a valid command line tool)


## Installation

Currently supported commands:

- Pinger: icmp ping
- MPPinger: see ``https://github.com/wontoniii/go-mp-ping``
- Iperferer: iperf network tool
- NStramer: run browser sessions (used to stream a video and then close the page automatically)

NOTE: To use remote hosts you need to setup passowrd less access to the node. Key-pair based authentication is supported.

