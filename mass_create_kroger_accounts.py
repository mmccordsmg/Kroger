import argparse
from kroger_funcs import create_kroger_account, link_kroger_altid

parser = argparse.ArgumentParser(description="Batch creates Kroger accounts.")
parser.add_argument("-e",	"--emailprefix",	help="Email prefix.  Will be appended by a 3 digit zero-padded number and the specified suffix.", required=True,	type=str)
parser.add_argument("-x",	"--emailsuffix",	help="Email suffix.  This is the part after the zero-padded 3 digit number.", required=True,	type=str)
parser.add_argument("-p",	"--password",	help="Password",								required=True,	type=str)
parser.add_argument("-f",	"--firstname",	help="First Name",						required=True,	type=str)
parser.add_argument("-l",	"--lastname",	help="Last Name",								required=True,	type=str)
parser.add_argument("-o",	"--phoneprefix",	help="Phone Number prefix.  7 numbers.  No parentheses or dashes.",	required=True,	type=int)
parser.add_argument("-s",	"--store",			help="Store Number",								type=str, default="00515")
parser.add_argument("-d",	"--division",		help="Division Number",							type=str, default="029")
parser.add_argument("-t",	"--startnumber",	help="Number to start from.", required=True, type=int)
parser.add_argument("-n",	"--endnumber",	help="Number to end on.",	required=True,	type=int)

args = parser.parse_args()

if len(str(args.phoneprefix)) != 7:
	print("Phone prefix must be 7 numeric digits")
	exit()
if (args.endnumber - args.startnumber) > 1000:
	print("Maximum 1000 accounts per run.")
	exit()
	
if (args.endnumber - args.startnumber) <=0:
	print("startnumber must be less than endnumber")
	exit()

for i in range(args.startnumber, args.endnumber+1):
	email=args.emailprefix + str(i).zfill(3) + args.emailsuffix
	if "@" not in email:
		print("email prefix and suffix do not create valid email address")
		exit()
	phone=str(args.phoneprefix) + str(i).zfill(3)
	token = create_kroger_account (email, args.password, args.division, args.store)
	if not token:
		print("Error creating account %s" % email)
	else:
		virtualCardNumber = link_kroger_altid(args.firstname, args.lastname, args.division, phone)
		if virtualCardNumber:
			print("Account %s created successfully! Virtual Card# is %s, AltId is %s" % (email, virtualCardNumber, phone))
		else:
			print("Error linking altid %s to account %s" % (phone, email))
