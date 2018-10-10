#!/bin/bash

# ***** Configurations for the mininet to be running *****

ovs-vsctl add-port s10 eno1
ovs-vsctl add-port s20 eno2
ovs-ofctl add-flow s10 priority=100,in_port=1,action=2
ovs-ofctl add-flow s10 priority=100,in_port=2,action=1
ovs-ofctl add-flow s20 priority=100,in_port=1,action=2
ovs-ofctl add-flow s20 priority=100,in_port=2,action=1
