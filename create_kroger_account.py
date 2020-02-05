from kroger_funcs import create_kroger_account, link_kroger_altid
import argparse


parser = argparse.ArgumentParser(description="Creates Kroger account using information provided in arguments")
parser.add_argument("-e",	"--email",			help="Email address",								required=True,	type=str)
parser.add_argument("-p",	"--password",		help="Password",										required=True,	type=str)
parser.add_argument("-f",	"--firstname",	help="First Name",									required=True,	type=str)
parser.add_argument("-l",	"--lastname",		help="Last Name",										required=True,	type=str)
parser.add_argument("-d",	"--division",		help="Division Number",							type=str, default="029")
parser.add_argument("-a",	"--altid",			help="Alternate Id (10 digits)",		required=True,	type=str)
parser.add_argument("-s",	"--store",			help="Store Number",								type=str, default="00515")

args = parser.parse_args()
if len(args.altid) != 10:
	print("%s must be 10 digits in length" % args.altid)
	quit()

token = create_kroger_account (args.email, args.password, args.division, args.store)
if not token:
	print("Error creating account %s" % args.email)
else:
	virtualCardNumber = link_kroger_altid(args.firstname, args.lastname, args.division, args.altid)
	if virtualCardNumber:
		print("Account %s created successfully! Virtual Card# is %s, AltId is %s" % (args.email, virtualCardNumber, args.altid))
	else:
		print("Error linking altid %s to account %s" % (args.altid, args.email))