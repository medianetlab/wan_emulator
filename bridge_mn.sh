#!/bin.bash

# ***** Configurations for the mininet to be running *****

ovs-ofctl del-flows s10
ovs-vsctl add-port s10 eno1
ovs-ofctl add-flow s10 in_port=1,action=2
ovs-ofctl add-flow s10 in_port=2,action=1
