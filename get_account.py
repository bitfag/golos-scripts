#!/usr/bin/env python

import json
import argparse
import logging
import yaml
from golos import Steem
from golos.account import Account


log = logging.getLogger('functions')


def main():

    parser = argparse.ArgumentParser(
        description='', epilog='Report bugs to: https://github.com/bitfag/golos-scripts/issues'
    )
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug output'),
    parser.add_argument('-c', '--config', default='./common.yml', help='specify custom path for config file')
    parser.add_argument('account', help='account name')
    args = parser.parse_args()

    # create logger
    if args.debug is True:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    # parse config
    with open(args.config, 'r') as ymlfile:
        conf = yaml.safe_load(ymlfile)

    golos = Steem(nodes=conf['nodes_old'], keys=conf['keys'])
    a = Account(args.account, steemd_instance=golos)
    j = json.dumps(a, indent=4)
    print(j)


if __name__ == '__main__':
    main()
