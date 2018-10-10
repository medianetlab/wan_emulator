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

    # Create the bridge switches and Links
    s10 = self.addSwitch('s10')
    s20 = self.addSwitch('s20')
    self.addLink(s1, s10)
    self.addLink(s2, s20)

    # Connect the edge switches with 2 switches
    self.addLink(s1, core_switch_list[0])
    self.addLink(s1, core_switch_list[1])
    self.addLink(s2, core_switch_list[-1])
    self.addLink(s2, core_switch_list[-2])

    # **** Uncomment for WAN mesh topology ****
    # Connect the core switches in a mesh topology
    #for i in irange(0,len(core_switch_list)-2):
    #  for j in irange(i+1,len(core_switch_list)-1):
    #    self.addLink(core_switch_list[i],core_switch_list[j])

    # Make STP links
    self.addLink(core_switch_list[1],core_switch_list[3])

    # DEBUG: Add one host to each core switch
    h3 = self.addHost("h3", ip="10.100.112.101/20")
    h4 = self.addHost("h4", ip="10.100.112.102/20")
    self.addLink(h3, core_switch_list[0])
    self.addLink(h4, core_switch_list[1])

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
  net.start()
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
