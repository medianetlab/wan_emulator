# Mininet network for the SDN Infrastracture

## Topology
The sdn_topology.py file implements an example topology of a network depicted below, implemented within the WAN emulator.
![Network](https://github.com/themisAnagno/wan_emulator/blob/master/image_preview.png)

* Create the Mininet network
```
sudo python sdn_topology.py &
```
* Add the host's physical NICs as ports to the virtual switches
```
sudo ./bridge_mn.sh
```


[Dropbox Paper](https://paper.dropbox.com/doc/SDN-on-Mininet--APA7aDHgzHQfkdX1sr4lAZo7Ag-6JB5pxs7wLXU3PkhRVzpQ)
