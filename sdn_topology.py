# put python here

import atexit

# Import Mininet classes
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.util import irange


# Define global vars
net = None
core_switch_list = []
k = 4

# Define the topology class
class SDNTopo(Topo):
  "SDN Topology"

  def __init__(self, k=4, **opts):

    # Initialize object argument
    super(SDNTopo, self).__init__(*opts)
    self.k = k

    # Create template host
    hconf = {'inNamespace':True}

    # Create the k switches of the mesh topology
    for i in irange(3,k+2):
      switch_name = self.addSwitch('s%s' % i)
      core_switch_list.append(switch_name)

    # Create the edge switches
    s1 = self.addSwitch('s1')
    s2 = self.addSwitch('s2')

    # Connect the edge switches with 2 switches
    self.addLink(s1, core_switch_list[0])
    self.addLink(s1, core_switch_list[1])
    self.addLink(s2, core_switch_list[-1])
    self.addLink(s2, core_switch_list[-2])

    # Connect the core switches in a mesh topology
    for i in irange(0,len(core_switch_list)-2):
      for j in irange(i+1,len(core_switch_list)-1):
        self.addLink(core_switch_list[i],core_switch_list[j])

# Start network functions
def startNetwork():
  "Creates and starts the network"

  global net, k
  info(' *** Creating Overlay Network Topology ***\n')
  # Create the topology object
  topo = SDNTopo(k)
  # Create and start the network
  c1= RemoteController("c1", ip="10.30.0.90")
  net = Mininet(topo=topo, link=TCLink, controller=c1, autoSetMacs=True)
  net.start
  info('*** Running CLI ***\n')
  CLI(net)


# Stop network functions
def stopNetwork():
  "Stops the network"

  global net
  if net is not None:
    info("*** Tearing down overlay network ***\n")
    net.stop()

# If run as a script
if __name__ == '__main__':
  # Force cleanup on exit by registering a cleanup function
  atexit.register(stopNetwork)

  # Print useful informations
  setLogLevel('info')

  # Start network
  startNetwork()

