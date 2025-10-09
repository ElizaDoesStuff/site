import re
import argparse as ap
import json

def build(input,output):
	original = input.read()
	processed = ""	

	output.seek(0)
	output.write(processed)

parser = ap.ArgumentParser("Build.py", description="Runs a preprocessing script across all the site's files.")
parser.add_argument("--mode", help="Determines whether the build will be a dev build or a release build. Must be one of 'DEV' or 'RELEASE'", type=str)
args = parser.parse_args()

if args.mode == None: args.mode = "DEV"
print(args.mode)

build_settings = None
with open("build.json") as file:
	build_settings = json.load( file )

print(build_settings)

for page in build_settings["pages"]:
	input = open(page, mode="r")
	try:
		output = open("static/" + page, mode="w")
	except:
		output = open("static/" + page, mode="x")
	build(input, output)
	input.close()
	output.close()
