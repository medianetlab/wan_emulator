#!/bin/bash

# ***** Configurations for the mininet to be running *****

ovs-vsctl add-port edge1 eno1
ovs-vsctl add-port edge2 eno2
ovs-ofctl add-flow edge1 priority=100,in_port=1,action=2
ovs-ofctl add-flow edge1 priority=100,in_port=2,action=1
ovs-ofctl add-flow edge2 priority=100,in_port=1,action=2
ovs-ofctl add-flow edge2 priority=100,in_port=2,action=1

# Enable STP on switch
if [ ! -z "${1+x}" ];
then
for i in $(seq "${1}");
do
echo "s${i}"
ovs-vsctl set bridge "s${i}" stp-enable=true;
done
fi
