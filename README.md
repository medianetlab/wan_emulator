# Mininet network for the SDN Infrastracture

WAN emulator uses Mininet in order to implement a random network topology, like the one depicted in the image below.
![Network](https://github.com/themisAnagno/wan_emulator/blob/master/image_preview.png)

Then two external interfaces of the host are connected to the edge bridges of the topology, to allow incoming traffic from one interface to go through the virtual network in Mininet and to exit the host from the other interface. This way, WAN emulator can be used as part of a larger physical Network, adding various traffic parameters, such as delay, bandwidth and loss.

## Requirements

* Mininet >= 2.2 [Install Mininet](http://mininet.org/download/)
* Python >= 3.6 [Install Python](https://www.python.org/downloads/)

## Install

```bash
git clone https://github.com/medianetlab/wan_emulator.git
cd wan_emulator
```

## Start

Run the script sdn_topology.py with sudo in order to start the network. The network will be created and the Mininet CLI will come up. Type `exit` to exit the WAN emulator.

```man
usage: sdn_topology.py [-h] [--bandwidth BW] [--delay DELAY] [--loss LOSS]
                       [--ryu] [--controller CTL]
                       [--nodes {3..19}]
                       [--hosts {1..9}] [--random]

Mininet WAN Emulator

optional arguments:
  -h, --help            show this help message and exit
  --bandwidth BW, -b BW
                        Define the Bandwidth on the links in Mbps (Example:
                        1000)
  --delay DELAY, -d DELAY
                        Define the Delay on the links in ms (Example 1)
  --loss LOSS, -l LOSS  Define the Loss on the links in percentage (Example 1)
  --ryu                 Start RYU Controller with Simple Switch module on
                        localhost
  --controller CTL, -c CTL
                        Define a custom SDN Controller for switches in the
                        form controller_ip:port. By default it will try
                        localhost
  --nodes {3..19}, -n {3..19}
                        Define the number of intermediate nodes/switches in
                        the system. Default=4
  --hosts {1..9}
                        Add hosts to random switches on the topology
  --random              Create a random switch topology and block loops using
                        STP
```
