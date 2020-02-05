from kroger_funcs import do_kroger_login, clip_kroger_coupons, check_kroger_coupon
import argparse

parser = argparse.ArgumentParser(description="Clips kroger coupons in couponfile for account specified")
parser.add_argument("-u",	"--username",		help="Username (Email address)",		required=True,	type=str)
parser.add_argument("-p",	"--password",		help="Password",										required=True,	type=str)
parser.add_argument("-f", "--couponfile", help="File with coupon ids to clip", required=True, type=str)
args = parser.parse_args()

loginresult = do_kroger_login(args.username, args.password)
if not loginresult:
	print ("Error logging in, exiting...")
	exit()
	
#unclipped_coupons = get_kroger_coupons(args.division, args.store, False)

with open(args.couponfile, "r") as coupon_file:
	coupons_to_clip = coupon_file.read().splitlines()

tosubmit = []
for coupon_to_clip in coupons_to_clip:
	clipped, description = check_kroger_coupon(coupon_to_clip)
	if clipped:
		print("%s - %s already clipped on account %s" % (coupon_to_clip, description, args.username))
	else:
		tosubmit.append({"id": coupon_to_clip, "description": description})

if tosubmit:
	clip_kroger_coupons(tosubmit)
else:
	print("Nothing found to clip on account %s" % args.username)	
