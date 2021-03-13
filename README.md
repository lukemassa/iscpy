# python3-iscpy

iscpy Python3 library. Reads and writes ISC-syled configuration files such as
ISC BIND8/BIND9 and ISC-DHCP server/client.  Additional features such as adding zone and write to file

## Usage

```
ParseISCString(isc_string)
```
Returns `parsed bind config file` in python dictionary format(ISC dictionary) and `keys` without childkeys e.g. include

```
AddZone(json_zone, isc_dict)
```
Adding zone. Input is in json string. Returns ISC dictionary with added zone. This method doesn't include writing to output file

```
WriteToFile(isc_dict, isc_specialkeys, filename)
```
Write ISC dictionary to a file

```
ReadFromFile(filename)
```
Read an ISC file into a dictionary
