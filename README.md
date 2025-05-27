# QueryVlcb
Some Python scripts to query for information on a VLCB/CBUS layout and perform
some actions that are not provided by the [Module Management Console](https://github.com/david284/MMC-SERVER) (MMC).

The scripts connect to a running CBUS Server on network port 5550 on the localhost.
Such a server can be provided by MMC, JMRI CBUS Hub or Nigel Phillip's CBUS Server.

Note: CBUS® is the registered trademark of Dr. Mike Bolton.

## Scripts

<dl>
<dt>QueryNodes.py</dt>
<dd>Queries for nodes that are online on a VLCB/CBUS network. 
This script does not take any command line parameters.

Sends a QNN message and collects the PNN responses from the nodes and presents them
in a human-readable form.
</dd>

<dt>QueryNodeParameters.py</dt>
<dd>Queries a node for its parameters and presents these parameters in a human readable
form.
This script takes an optional command line parameter that is the node number of
the node to be queried. 
</dd>

<dt>CountCANCABs.py</dt>
<dd>Sends a parameter query to node number 65535, which is dedicated to CANCAB,
and counts the received responses.
This assumes that each connected CANCAB responds to this parameter query.
</dd>

<dt>CanActivity.py</dt>
<dd>Shows CAN message counts and other info that indicates activity on the CAN bus.
</dd>

<dt>CanErrors.py</dt>
<dd>Shows errors on the CAN bus for each VLCB node.
</dd>

<dt>CanBufferHighWatermark.py</dt>
<dd>Queries all nodes and for each VLCB node query the CAN Service
high watermark diagnostic. 
This is useful to identify potential CAN problems.

This was created as an early test and is now incorporated into CanActivity.py.
</dd>

<dt>NodeActivity.py</dt>
<dd>Shows counters that show activity for each VLCB node such as counts of
produced and consumed events.
</dd>

<dt>NodeErrors.py</dt>
<dd>Shows some error counters for each VLCB node.
</dd>

<dt>ManufacturerReset.py</dt>
<dd>Resets a node to manufacturer settings.
</dd>

</dl>

## Supporting files
The scripts above makes use of the following files:

<dl>
<dt>CanMessage.py</dt>
<dd>A class that represents a CAN frame and its information.
</dd>

<dt>CbusServerConnection.py</dt>
<dd>Makes a connection to a CBUS Server on network port 5550 on the localhost.
Provides functions for sending and receiving CAN messages on this port.
</dd>

<dt>GridConnect.py</dt>
<dd>Converts `canmessage` to and from a GridConnect format that can be used when
communicating with the CBUS server.
</dd>

<dt>CbusInfo.py</dt>
<dd>Interprets CBUS numbers into something human-readable.
</dd>

<dt>vlcbdefs.py</dt>
<dd>Contains VLCB/CBUS constants. 
Copied from <a href="https://github.com/SvenRosvall/VLCB-defs">https://github.com/SvenRosvall/VLCB-defs</a>
</dd>

<dt>vlcbdictionaries.py</dt>
<dd>Contains dictionaries for looking up human-readable text for VLCB/CBUS numbers.
</dd>

<dt>generateVlcbLookup.sh</dt>
<dd>Generates `vlbdictionaries.py` from https://github.com/SvenRosvall/VLCB-defs
</dd>
</dl>