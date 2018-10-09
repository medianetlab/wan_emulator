# put python here

# Import Mininet classes
from mininet.top import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import RemoteController


# Define global vars
net = None
switch_list = []

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
  for i in irange(3,k+3):
    switch_name = self.addSwitch('s%s' % i)
    switch_list.append(switch_name)

  # Create the edge switches
  s1 = self.addSwitch('s1')
  s2 = self.addSwitch('s2')

  # Connect the edge switches with 2 switches
  self.addLink(s1, switch_list[0])
  self.addLink(s1, switch_list[1])
  self.addLink(s2, switch_list[-1])
  self.addLink(s2, switch_list[-2])
