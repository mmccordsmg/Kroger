from kroger_funcs import do_kroger_login, get_kroger_coupons, clip_kroger_coupons
import argparse

parser = argparse.ArgumentParser(description="Clips all kroger coupons for account specified")
parser.add_argument("-u",	"--username",		help="Username (Email address)",		required=True,	type=str)
parser.add_argument("-p",	"--password",		help="Password",										required=True,	type=str)
parser.add_argument("-d",	"--division",		help="Division #",									type=str, default="029")
parser.add_argument("-s",	"--store",			help="Store #",										  type=str, default="00515")

args = parser.parse_args()

loginresult = do_kroger_login(args.username, args.password)
if not loginresult:
	print ("Error logging in, exiting...")
	exit()
unclipped_coupons = get_kroger_coupons(args.division, args.store, False)
if unclipped_coupons:
	clip_kroger_coupons(unclipped_coupons)
