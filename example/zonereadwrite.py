#!/usr/bin/python

"""Zone read-write-read
DO NOT EVER RUN THIS TEST AGAINST A PRODUCTION DATABASE.
"""

__copyright__ = 'None'
__license__ = 'BSD 3-Clause'
__version__ = '1.8'


import unittest
import os
import types

import iscpy


NAMED_FILE = 'bind/example.named.conf'


class TestNamedImport(unittest.TestCase):


  def testMakeISC(self):
    self.assertEqual(iscpy.MakeISC(
        {'level1': {'level2': {'level3': {'level4': {
            'test1': True, 'test2': True, 'test3': True}}}},
         'newarg': 'newval', 'new_stanza': {'test': True}}),
        'new_stanza { test; };\n'
        'level1 { level2 { level3 { level4 { test1;\n'
                                            'test3;\n'
                                            'test2; }; }; }; };\n'
        'newarg newval;')
    self.assertEqual(iscpy.MakeISC(iscpy.ParseISCString(self.named_file)),
      'acl control-hosts { 127.0.0.1/32;\n'
      '192.168.1.3/32; };\n'
      'acl admin { 192.168.1.2/32;\n'
      '192.168.1.4/32;\n'
      '192.168.0.0/16; };\n'
      'view "authorized" { zone "smtp.university.edu" { masters { 192.168.11.37; };\n'
      'type master;\n'
      'file "test_data/test_zone.db"; };\n'
      'allow-query-cache { network-authorized; };\n'
      'allow-recursion { network-authorized; };\n'
      'recursion yes;\n'
      'zone "university.edu" { check-names ignore;\n'
      'masters { 192.168.11.37; };\n'
      'type slave;\n'
      'file "test_data/university.db.bak"; };\n'
      'match-clients { network-authorized; };\n'
      'zone "." { type hint;\n'
      'file "named.ca"; };\n'
      'additional-from-cache yes;\n'
      'additional-from-auth yes; };\n'
      'controls { inet * allow { control-hosts; } keys { rndc-key; }; };\n'
      'view "unauthorized" { zone "1.210.128.in-addr.arpa" { allow-query { network-unauthorized; };\n'
      'type master;\n'
      'file "test_data/test_reverse_zone.db"; };\n'
      'recursion no;\n'
      'match-clients { network-unauthorized; };\n'
      'zone "." { type hint;\n'
      'file "named.ca"; };\n'
      'zone "0.0.127.in-addr.arpa" { masters { 192.168.1.3; };\n'
      'type slave;\n'
      'file "test_data/university.rev.bak"; };\n'
      'additional-from-cache no;\n'
      'additional-from-auth no; };\n'
      'logging { category "update-security" { "security"; };\n'
      'category "queries" { "query_logging"; };\n'
      'channel "query_logging" { syslog local5;\n'
      'severity info; };\n'
      'category "client" { "null"; };\n'
      'channel "security" { file "/var/log/named-security.log" versions 10 size 10m;\n'
      'print-time yes; }; };\n'
      'include "/etc/rndc.key";\n'
      'options { directory "/var/domain";\n'
      'recursion yes;\n'
      'allow-query { any; };\n'
      'max-cache-size 512M; };')


def print_isc(isc_config):
    print("print_isc: called")
    # ISC Section (not GROUP)
    print("len(isc_config):",len(isc_config))
    print("type(isc_config):",type(isc_config))
    if type(isc_config)==list:
        for item1 in isc_config:
            print("type(item1):",type(item1),": ",item1)

    if isinstance(isc_config,dict):
        print("isc_config.items:",len(isc_config.items()))
        for k1, v1 in isc_config.items():
            print("k1: len:",len(k1),"type:",type(k1)," :", k1)
            print("v1: len:",len(v1),"type:",type(v1))
            if isinstance(v1,str):
                print("v1: ",v1)
            if isinstance(v1,dict):
                for k2, v2 in v1.items():
                    print("    k2: len:",len(k2),"type:",type(k2)," :", k2)
                    print("    v2: len:",len(v2),"type:",type(v2))
                    if isinstance(v2,str):
                        print("    v2:", v2)
                    if isinstance(v2,dict):
                        for k3, v3 in v2.items():
                            print("        k3: len:",len(k3),"type:",type(k3)," :", k3)
                            print("        v3: len:",len(v3),"type:",type(v3))
                            if isinstance(v3,str):
                                print("        v3:", v3)
                            if isinstance(v3,dict):
                                for k4, v4 in v3.items():
                                    print("            k4: len:",len(k4),"type:",type(k4)," :", k4)
                                    print("            v4: len:",len(v4),"type:",type(v4))
                                    if isinstance(v4,str):
                                        print("            v4:", v4)
                                    if isinstance(v3,dict):
                                        print("            v4: dict (not-expanded here)")
    return
    for keyname1, value1 in isc_config:
        print("keyname1:",keyname1)
        if (type(value1)!=list):
            print("value1:",value1)
        if (type(value1)==list):
            for keyname2, value2 in value1.items():
                print("keyname2:",keyname2, "value2:",value2)
                if (type(value2)==list):
                    for keyname3, value3 in value2.items():
                        print("keyname2:",keyname3, "value2:",value3)

def main():
    named_file = open(NAMED_FILE).read()
    print("named_file:",named_file)
    scrubbed_named_file = iscpy.ScrubComments(named_file)
    print(" ");
    print("scrubbed_named_file:",scrubbed_named_file)
    print(" ");
    named_lexical = iscpy.Explode(scrubbed_named_file)
    print("type(named_list):",type(named_lexical))
    print("Lexicaled into a named_list:",named_lexical)
    print(" ");
    named_parsed = iscpy.ParseTokens(named_lexical)
    print("type(named_parsed):",type(named_parsed))
    print("Tokenized into a named_parsed:",named_parsed)
    print("print_isc(named_lexical")
    print_isc(named_lexical)

    #  Back to named_file (ignores named_lexical and named_parsed)
    print(" ");
    named_dict = iscpy.dns.MakeNamedDict(named_file)
    print("type(named_dict):",type(named_dict))
    print("Dictionary made as named_dict:",named_dict)
    print(" ");

    # Focused on named_dict
    print("print_isc(named_dict)")
    print_isc(named_dict)
    print(" ");

    named_header = iscpy.dns.DumpNamedHeader(named_dict)
    print("type(named_header):",type(named_header))
    print("header of named_header:",named_header)
    print(" ");
    named_zone_dict = iscpy.dns.MakeZoneViewOptions(named_dict)
    print("type(named_zone_dict):",type(named_zone_dict))
    print("Dictionary made as named_zone_dict:",named_zone_dict)
    print(" ");
    print("print_isc(named_zone_dict")
    print_isc(named_zone_dict)



if( __name__ == '__main__' ):
  main()
