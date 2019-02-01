#!/bin/python
import argparse
import json
import unicodedata

def parse_args():
    parser = argparse.ArgumentParser(description='Generate Rundeck Node Definition (YML) from Ansible Inventory (JSON)')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Enable debug output')
    parser.add_argument('--file', required=True,
                    help='Location of Ansible Inventory Inputfile (Required)')
    return parser.parse_args()

# Remove Control Caracters if there are any in the inventory
def clean(s):
    if s is None:
        return ""
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def addhost(child,host,inventory):
    print("- "+host+":")
    print("  nodename: "+host)
    print("  tags: "+child)
    for var in inventory['_meta']['hostvars'][host]:
        print("  "+var+": "+clean(unicode(inventory['_meta']['hostvars'][host][var])))

def main():

    args = parse_args()
    hostlist=set([])
    grouplist=dict(list())

    try:

        with open(args.file,'r') as fin:
            inventory=json.load(fin)
            if 'hosts' in inventory['all']:
                for host in inventory['all']['hosts']:
                    hostlist.add(host)

            if 'children' in inventory['all']:
                for child in inventory['all']['children']:
                    if 'hosts' in inventory[child]:
                        for host in inventory[child]['hosts']:
                            hostlist.add(host)
                            if not host in grouplist:
                                grouplist[host] = list()
                            grouplist[host].append(child)

        for host in hostlist:
            tags = ""
            for childs in grouplist[host]:
                tags+=childs+","
            addhost(tags[:-1],host,inventory)  
    
    except Exception, error:
        print "An exception was thrown!"
        print str(error)


if __name__ == "__main__":
    main()
