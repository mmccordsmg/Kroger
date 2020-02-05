from kroger_funcs import do_kroger_login, get_kroger_coupons, unclip_kroger_coupons
import argparse

parser = argparse.ArgumentParser(description="Unclips all kroger coupons for account specified")
parser.add_argument("-u",	"--username",		help="Username (Email address)",		required=True,	type=str)
parser.add_argument("-p",	"--password",		help="Password",										required=True,	type=str)
parser.add_argument("-d",	"--division",		help="Division #",									type=str, default="029")
parser.add_argument("-s",	"--store",			help="Store #",										  type=str, default="00515")

args = parser.parse_args()

loginresult = do_kroger_login(args.username, args.password)

if not loginresult:
	print ("Error logging in, exiting...")
	exit()
clipped_coupons = get_kroger_coupons(args.division, args.store, True)
if clipped_coupons:
	unclip_kroger_coupons(clipped_coupons)
else:
	print("Nothing clipped on account %s" % args.username)