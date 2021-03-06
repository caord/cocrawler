'''
Fetches some urls using aiohttp. Also serves as a minimum example of using aiohttp.

Good examples:

https://www.enterprisecarshare.com/robots.txt -- 302 redir lacking Location: raises RuntimeError

'''

import sys
import argparse

import asyncio

import cocrawler.conf as conf
import cocrawler.dns as dns

ARGS = argparse.ArgumentParser(description='CoCrawler dns fetcher')
ARGS.add_argument('--config', action='append')
ARGS.add_argument('--configfile', action='store')
ARGS.add_argument('--no-confighome', action='store_true')
ARGS.add_argument('hosts', nargs='+', help='list of hostnames to query')

args = ARGS.parse_args()

config = conf.config(args.configfile, args.config, confighome=not args.no_confighome)

ns = config['Fetcher'].get('Nameservers')
if not isinstance(ns, list):
    ns = [ns]

dns.setup_resolver(ns)
print('set nameservers to', ns)


async def main(hosts):
    for host in hosts:
        try:
            result = await dns.query(host, 'A')
            print(host, result)
        except Exception as e:
            result = None
            print('saw exception', e, 'but ignoring it')


loop = asyncio.get_event_loop()

loop.run_until_complete(main(args.hosts))
