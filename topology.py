#!/usr/bin/env python3

import csv
import argparse
import logging
import sys

# Constants
DEFAULT_RACK = '/default-rack'
HOST_RACK_MAP_FILE = '/etc/hadoop/conf/host-rack.map'

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def resolve_rack(host):
    """Map host to rack using host rack map file"""
    rack = DEFAULT_RACK

    try:
        with open(HOST_RACK_MAP_FILE, 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                h, r = row
                if h == host:
                    rack = r
                    break

    except FileNotFoundError:
        log.error("Error: Host-rack file not found.")
    except ValueError:
        log.error("Error: Malformed line in host-rack file.")
    except Exception as e:
        log.error("Error reading %s - %s", HOST_RACK_MAP_FILE, e)

    return rack

if __name__ == '__main__':
    # Parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('hosts', nargs='+', help='List of hosts')
    args = parser.parse_args()

    if not args.hosts:
        parser.error('No hosts provided')

    # Resolve rack for each host
    for host in args.hosts:
        rack = resolve_rack(host)
        print(f'{host} is in rack {rack}')
