# QueryCbus
Some Python scripts to query for information on a CBUS layout.

## Scripts

### QueryNodes.py
Queries for nodes that are online on a CBUS network. 
This script does not take any command line parameters.

Sends a QNN message and collects the PNN responses from the nodes and presents them
in a human readable form.

### QueryNodeParameters.py
Queries a node for its parameters and presents these parameters in a human readable
form.
This script takes an optional command line parameter that is the node number of
the node to be queried. 

## Supporting files
The scripts above makes use of the following files:

### canmessage.py
A class that represents a CAN frame and its information.

### CbusServerConnection.py
Makes a connection to a CBUS Server on network port 5550 on the localhost.
Provides functions for sending and receiving CAN messages on this port.

### GridConnect.py
Converts `canmessage` to and from a GridConnect format that can be used when
communicating with the CBUS server.

### CbusInfo.py
Interprets CBUS numbers into something human readable.

### vlcbdefs.py
Contains CBUS constants. 
Copied from https://github.com/SvenRosvall/VLCB-defs

### vlcbdictionaries.py
Contains dictionaries for looking up human readable text for CBUS numbers.

### generateVlcbLookup.sh
Generates `vlbdictionaries.py` from https://github.com/SvenRosvall/VLCB-defs