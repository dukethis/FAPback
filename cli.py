#!/usr/bin/python3
# coding: UTF-8
# QUICK SERVER INTERFACE SCRIPT

import argparse,requests,json

if __name__ == '__main__':
	argp = argparse.ArgumentParser()
	argp.add_argument("--server", default="http://localhost:8000")
	argp.add_argument("--activities", nargs="+", type=int)
	argp.add_argument("--users",          nargs="+", type=str)
	args = argp.parse_args()

	url = args.server

	if args.users and args.activities:
		for a in args.activities:
			req = requests.request('GET', f'{url}/activities/{a}')
			res = req.content.decode('utf8') if req else None
			res = res[a] if type(res)==list and len(res)>a else res
			res = json.loads(res) if res else res
			print( json.dumps( res, indent=2 ) )

	elif args.activities:
		for a in args.activities:
			req = requests.request('GET', f'{url}/activities/{a}')
			res = req.content.decode('utf8') if req else None
			res = json.loads(res)
			print( json.dumps( res, indent=2 ) )
	elif args.users:
		for a in args.users:
			req = requests.request('GET', f'{url}/activities/{a}')
			res = req.content.decode('utf8') if req else None
			res = json.loads(res)
			print( json.dumps( res, indent=2 ) )
	else:
		print("Nop")