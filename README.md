slapi
=====
SoftLayer API Command Line Tool

Slapi is a command line tool to interface in SoftLayer's API

Installation
============
Install requirements
```
pip install -r requirements.txt
```

Create the following file to ~/.slapi.conf
```
{
    "softlayer": {
        "api_user": "<softlayer username>",
        "api_key": "<softlayer api key>"
    }
}
```

Usage
=====

To get help:

```
$ slapi help
```

To get a list of commands:

```
$ slapi commands
```

Examples
========

Show Hardware Information

```
$ slapi hardware show myserver

Id:             12345
Hostname:       myserver
Domain:         mydomain.net
FQDN:           myserver.mydomain.net
Public IP:      12.34.56.78
Private IP:     10.1.2.3
Management IP:  10.4.5.6
Datacenter:     
  Name:        San Jose 1
    Short Name:  sjc01
    Serial Number:  SL0000001
```

Show Hardware Components

```
$ slapi hardware show -p disk myserver 

Id:             12345
Hostname:       myserver
Domain:         mydomain.net
FQDN:           myserver.mydomain.net
Public IP:      12.34.56.78
Private IP:     10.1.2.3
Management IP:  10.4.5.6
Datacenter:     
  Name:        San Jose 1
    Short Name:  sjc01
    Serial Number:  SL0000001
Disks:          
  Model:  
    Capacity:      600
    Description:   SA-SCSI SASII:600:15000: Cheetah
    Version:       ST3600057SS
    Manufacturer:  Seagate
    Name:          Cheetah

  Model:  
    Capacity:      600
    Description:   SA-SCSI SASII:600:15000: Cheetah
    Version:       ST3600057SS
    Manufacturer:  Seagate
    Name:          Cheetah

  Model:  
    Capacity:      600
    Description:   SA-SCSI SASII:600:15000: Cheetah
    Version:       ST3600057SS
    Manufacturer:  Seagate
    Name:          Cheetah

  Model:  
    Capacity:      600
    Description:   SA-SCSI SASII:600:15000: Cheetah
    Version:       ST3600057SS
    Manufacturer:  Seagate
    Name:          Cheetah
```

Specifications
==============

Specifications allow you to search for and reference SoftLayer objects
in a number of different ways. Different object types have different
specifications that can be used to reference objects.

For example, when displaying hardware properties, you may want to
search for devices by hostname, or by IP address, or by SoftLayer
object ID.

Hostname:
```
slapi hardware show myserver
```

IP Address:
```
slapi hardware show 12.34.56.67
```

Object ID:
```
slapi hardware show 12345
```

*Hardware Specification*

```
hardware_spec := object_id | ip_address | fqdn
```

*Quote Specification*

```
quote_spec := object_id | name
```

*Location/Datacenter Specification*

```
location_spec := object_id | name
```

*VLAN Specification*
```
vlan_spec := vlan_number 
```
