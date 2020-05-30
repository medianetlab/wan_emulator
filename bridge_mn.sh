#!/bin/bash

# ***** Configurations for the mininet to be running *****

# Connect external interfaces to edge bridges
if [ ! -z "${2+x}" ] && [ ! -z "${3+x}" ];
then
ovs-vsctl add-port edge1 "${2}"
ovs-vsctl add-port edge2 "${3}"
ovs-ofctl add-flow edge1 priority=100,in_port=1,action=2
ovs-ofctl add-flow edge1 priority=100,in_port=2,action=1
ovs-ofctl add-flow edge2 priority=100,in_port=1,action=2
ovs-ofctl add-flow edge2 priority=100,in_port=2,action=1
fi

# Enable STP on switch
for i in $(seq 3 $(($1 + 2)));
do
ovs-vsctl set bridge "s${i}" stp-enable=true;
done
