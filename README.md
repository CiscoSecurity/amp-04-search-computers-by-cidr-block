[![Gitter chat](https://img.shields.io/badge/gitter-join%20chat-brightgreen.svg)](https://gitter.im/CiscoSecurity/AMP-for-Endpoints "Gitter chat")

### AMP for Endpoints search computers by CIDR block:

Takes a CIDR block as input and queries the environment for computers with an assigned IP Address within that range. Collects hostname, GUID, and network interfaces of computers that match. This is information is written to disk as ```output.json``` along with the CIDR block that was searched for, the timestamp of the query, the IP address hits, and the total number of hits. If a CIDR block is not provided as a command line argument, the script will prompt for one.

### Before using you must update the following:
The authentictaion parameters are set in the ```api.cfg``` :
- client_id 
- api_key

### Usage:
```
python search_computers_cidr_block.py
```
or
```
python search_computers_cidr_block.py 10.10.10.25/27
```

### Example script output:  
```
search_cidr_block.py 10.10.10.25/27
Querying 32 IP addresses
Found 1 host with 10.10.10.15
Found 1 host with 10.10.10.17
Found 1 host with 10.10.10.18
Found 1 host with 10.10.10.20
Found 1 host with 10.10.10.21
Found 1 host with 10.10.10.22
Found 1 host with 10.10.10.23
Found 1 host with 10.10.10.25
Finished!
Found 8 GUIDs from 8 IP Addresses
Writing results to output.json
```
