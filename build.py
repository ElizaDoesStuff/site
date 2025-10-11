import re # Regex
import argparse as ap # CLI Argument Parsing
import json # JSON Parsing
import shutil # File utilities
import os # More file stuff

#############################################################################################################################################################
## @@@@ @@@@ @@@@ @  @  @@@@
## @    @     @   @  @  @  @
## @@@@ @@@   @   @  @  @@@@
##    @ @     @   @  @  @
## @@@@ @@@@  @   @@@@  @
#############################################################################################################################################################

# Parse command line arguments
parser = ap.ArgumentParser("Build.py", description="Runs a preprocessing script across all the site's files.")
parser.add_argument("--mode", 
	help="Determines whether the build will be a dev build or a release build.",
	choices=["DEV","RELEASE"],
	nargs="?", 
	default="DEV"
)
parser.add_argument("--clean", 
	help="Tells the script to empty the output directory and start from scratch.",
	action=ap.BooleanOptionalAction
)
args = parser.parse_args()

# Open the build file and parse it into an object
build = None
with open("build.json") as file:
	build = json.load( file )

# If the --clean flag is set, delete all built files and start from scratch
if args.clean and os.path.exists("Static"):
	shutil.rmtree("Static")

assets_table = {}

#############################################################################################################################################################
## @@@  @  @ @@@@ @    @@@  @@@@ @  @ @@@@      @@@@ @@@@ @@@@ @@@@ @@@@
## @  @ @  @  @   @    @  @  @   @@ @ @         @  @ @  @ @    @    @
## @@@@ @  @  @   @    @  @  @   @ @@ @ @@      @@@@ @@@@ @ @@ @@@  @@@@
## @  @ @  @  @   @    @  @  @   @ @@ @  @      @    @  @ @  @ @       @
## @@@  @@@@ @@@@ @@@@ @@@  @@@@ @  @ @@@@      @    @  @ @@@@ @@@@ @@@@
#############################################################################################################################################################

def build_page(file):
	input = open(file["path"], "r")
	output = None
	if os.path.exists("Static/" + file["path"]):
		output = open("Static/" + file["path"], "w") 
	else:
		output = open("Static/" + file["path"], "x")
	
	raw = input.read()
	cooked = raw
	
	# Insert assets
	cooked = re.sub( r"(\w+?)\={(\w+)\}", lambda match: f"{match[1]}='{assets_table[ match[2] ]}'", cooked )
	cooked = re.sub( r"\{(\w+)\}", lambda match: f"<img src='{ assets_table[ match[1] ]}'/>", cooked )
	print(cooked)

	output.write(cooked)

#############################################################################################################################################################
## @@@@ @@@@ @@@@ @  @ @@@@ @@@@ @  @ @@@@ @@@@
## @     @   @  @ @  @ @     @   @  @ @  @ @   
## @@@@  @   @@@@ @  @ @     @   @  @ @@@@ @@@
##    @  @   @@@  @  @ @     @   @  @ @@@  @
## @@@@  @   @  @ @@@@ @@@@  @   @@@@ @  @ @@@@
#############################################################################################################################################################

def is_file_node(node): return ("name" in node.keys()) and ("type" in node.keys())

# If the 'Static' directory does not already exist, create it
if not os.path.exists("Static/"):
	os.mkdir("Static")

# Create all necessary directories within the Static/ directory
# Also creates a list of all file nodes for later use
build_files = []
def build_directories(root=build, path="."):
	if is_file_node(root):
		if root["name"] in [ i["name"] for i in build_files ]: return
		build_files.append( { "name": root["name"], "type": root["type"], "path": path } )
		return
	
	if not os.path.exists("Static/" + path):
		os.mkdir("Static/" + path)
	for key in root.keys():
		build_directories(root[key], path + "/" + key)

# Locate all asset nodes and add them to the assets table
def build_assets():
	print("\x1b[31m——— Processing assets: ———\x1b[m")
	for file in build_files:
		if file["type"] != "asset": continue
		print("Processing asset '" + file["name"] + "'...")
		shutil.copy(file["path"], "Static/" + file["path"])
		assets_table[ file["name"] ] = file["path"]

def build_components():
	print("\x1b[34m——— Processing components: ———\x1b[m")

def build_pages():
	print("\x1b[33m——— Processing pages: ———\x1b[m")
	for file in build_files:
		if file["type"] != "page": continue
		print(f"Processing page '{file["name"]}' ({file["path"]})...")
		build_page(file)

build_directories()
build_assets()
build_components()
build_pages()