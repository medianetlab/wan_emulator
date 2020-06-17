#!/usr/bin/env python3.7

import atexit
import argparse
import logging
import subprocess
import os
import random

# Import Mininet classes
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info, debug
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.util import irange

# Create logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)

# Create the argparser
parser = argparse.ArgumentParser(description="Mininet WAN Emulator")
parser.add_argument(
    "--bandwidth",
    "-b",
    dest="bw",
    required=False,
    default=1000,
    help="Define the Bandwidth on the links in Mbps (Example: 1000)",
    type=int,
)
parser.add_argument(
    "--delay",
    "-d",
    dest="delay",
    required=False,
    default=None,
    help="Define the Delay on the links in ms (Example 1)",
    type=int,
)
parser.add_argument(
    "--loss",
    "-l",
    dest="loss",
    required=False,
    default=None,
    help="Define the Loss on the links in percentage (Example 1)",
    type=int,
)
parser.add_argument(
    "--ryu", action="store_true", help="Start RYU Controller with Simple Switch module on localhost"
)
parser.add_argument(
    "--controller",
    "-c",
    dest="ctl",
    required=False,
    default=None,
    help="Define a custom SDN Controller for switches in the form controller_ip:port."
    " By default it will try localhost",
    type=str,
)
parser.add_argument(
    "--nodes",
    "-n",
    dest="nodes",
    required=False,
    default=4,
    choices=range(3, 20),
    help="Define the number of intermediate nodes/switches in the system. Default=4",
    type=int,
)
parser.add_argument(
    "--hosts",
    dest="hosts",
    required=False,
    default=0,
    choices=range(1, 10),
    help="Add hosts to random switches on the topology",
    type=int,
)
parser.add_argument(
    "--random",
    action="store_true",
    help="Create a random switch topology and block loops using STP",
)

args = parser.parse_args()

# Global vars
net = None


# Define the topology class
class SDNTopo(Topo):
    """SDN Mininet Topology"""

    def __init__(self, **opts):

        # Initialize object argument
        super(SDNTopo, self).__init__(*opts)
        self.k = args.nodes
        self.switch_list = []

        # Create the k switches of the mesh topology
        for i in irange(3, self.k + 2):
            new_switch = self.addSwitch(f"s{i}", dpid=f"{i}")
            self.switch_list.append(new_switch)

        # Create the edge switches
        e1 = self.addSwitch("edge1", dpid="101")
        e2 = self.addSwitch("edge2", dpid="102")

        # Create the bridge switches and Links
        s1 = self.addSwitch("s1", dpid="1")
        s2 = self.addSwitch("s2", dpid="2")
        self.addLink(s1, e1, bw=args.bw, loss=args.loss, delay=args.delay)
        self.addLink(s2, e2, bw=args.bw, loss=args.loss, delay=args.delay)

        # Connect the edge switches with 2 switches
        self.addLink(s1, self.switch_list[0], bw=args.bw, loss=args.loss, delay=args.delay)
        self.addLink(s2, self.switch_list[-1], bw=args.bw, loss=args.loss, delay=args.delay)
        if not self.k % 2 and not args.random:
            self.addLink(s2, self.switch_list[-2], bw=args.bw, loss=args.loss, delay=args.delay)

        # Make STP links
        if not args.random:
            # Connect each switch in a defined topology
            for i in range(0, len(self.switch_list) - 2, 2):
                for j in range(1, 3):
                    self.addLink(
                        self.switch_list[i],
                        self.switch_list[i + j],
                        bw=args.bw,
                        loss=args.loss,
                        delay=args.delay,
                    )
        else:
            # Connect each switch with a random previous one
            for i in range(1, len(self.switch_list)):
                connect_switch = random.choice(self.switch_list[:i])
                self.addLink(
                    self.switch_list[i],
                    connect_switch,
                    bw=args.bw,
                    loss=args.loss,
                    delay=args.delay,
                )

        # Add one host to each core switch
        for i in range(args.hosts):
            new_host = self.addHost(f"h{i}", ip=f"10.10.10.{i+1}/24")
            self.addLink(
                new_host,
                self.switch_list[random.randint(0, len(self.switch_list) - 1)],
                bw=args.bw,
                loss=args.loss,
                delay=args.delay,
            )


# Start network functions
def startNetwork():
    "Creates and starts the network"

    global net

    cwd = os.getcwd()

    if args.ryu:
        subprocess.run([f"{cwd}/start_ryu.sh"])

    info(" *** Creating Overlay Network Topology ***\n")
    # Create the topology object
    topo = SDNTopo()
    # Create and start the network
    # Create the controller
    if args.ctl:
        ctl_ip, ctl_port = args.ctl.split(":")
        ctl_port = int(ctl_port)
        info(ctl_ip, ctl_port)
    else:
        ctl_ip, ctl_port = "127.0.0.1", None
    c1 = RemoteController("c1", ip=ctl_ip, port=ctl_port)
    net = Mininet(topo=topo, link=TCLink, controller=c1, autoSetMacs=True)
    net.start()
    # Add the external host ports to the edge bridges
    bridge_commands = [f"{cwd}/bridge_mn.sh"]
    if args.random:
        stp = args.nodes
    else:
        stp = 0
    bridge_commands.append(str(stp))
    ans = input("Connect external ifaces? (Y/n) > ")
    port1, port2 = "0", "0"
    if ans != "n":
        port1 = input("Interface 1 name: ")
        port2 = input("Interface 2 name: ")
        bridge_commands += [port1, port2]
    subprocess.run(bridge_commands)
    info("*** Running CLI ***\n")
    CLI(net)


# Stop network functions
def stopNetwork():
    "Stops the network"

    if net is not None:
        info("*** Tearing down overlay network ***\n")
        net.stop()
        subprocess.run(["mn", "-c"])


# If run as a script
if __name__ == "__main__":
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)
    # Print useful informations
    setLogLevel("info")
    # Start network
    startNetwork()
