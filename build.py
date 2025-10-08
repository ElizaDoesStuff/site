import re
import argparse as ap
import json

def build(input,output):
	initial = input.read()

	output.seek(0)
	output.write(initial + "\nHello preprocessor!")

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
	output = open("static/" + page,)
	build(input, output)
	page.close()
