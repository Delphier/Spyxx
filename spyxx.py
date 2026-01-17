from pathlib import Path
import urllib.request
import json
import shutil

DOWNLOADS = Path("Downloads")
RELEASES = Path("Releases")

def download(url):
	with urllib.request.urlopen(url) as resp:
		return resp.read()

MANIFEST_URL = "https://aka.ms/vs/stable/channel"
print("Checking Visual Studio Manifest...")
chman = json.loads(download(MANIFEST_URL))
vsman_url = chman["channelItems"][0]["payloads"][0]["url"]
license = chman["channelItems"][1]["localizedResources"][0]["license"]
packages = json.loads(download(vsman_url))["packages"]

version = ""
filename = ""
url = ""
for i in range(len(packages)-1, -1, -1):
	if packages[i]["id"] == "Microsoft.VisualStudio.VC.Ide.Dskx":
		version = packages[i]["version"]
		filename = packages[i]["payloads"][0]["fileName"]
		url = packages[i]["payloads"][0]["url"]
		break

yes = input(f"Do you accept Microsoft Visual Studio license: {license} [Y/N] ? ")
if yes.upper() not in ["", "YES", "Y"]:
	exit(0)

print(f"Downloading {filename}...")
DOWNLOADS.mkdir(exist_ok=True)
with open(DOWNLOADS / filename, "wb") as file:
	file.write(download(url))

print(f"Unpacking {filename}...")
ARCHIVES = DOWNLOADS / "Archives"
shutil.rmtree(ARCHIVES, ignore_errors=True)
shutil.unpack_archive(DOWNLOADS / filename, ARCHIVES, "zip")

print(f"Creating Zip in {RELEASES.resolve()}...")
RELEASES.mkdir(exist_ok=True)
shutil.make_archive(f"{RELEASES.resolve()}/Spy++{version}", "zip", ARCHIVES / "Contents/Common7/Tools")

print("Done!")
