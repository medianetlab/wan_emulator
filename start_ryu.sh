#!/bin/bash

# Start ryu controller application
printf '*** Starting RYU Controller on localhost ***\n'

ryu-manager ryu.app.simple_switch_13 ryu.app.gui_topology.gui_topology --observe-links &> ryu-logs.log &
sleep 10
