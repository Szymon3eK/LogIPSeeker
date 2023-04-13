import re
import sys
import os
from colored import fg, bg, attr
log = sys.argv[1]
import zipfile
import gzip
import shutil
from io import BytesIO
import chardet

namelogfile = 0;


allip = [];

if os.path.exists('temp'):
    try:
        os.rmdir('temp')
        print(f"{bg(1)}{attr(1)} REMOVED TEMP FOLDER {attr(0)}")
    except OSError as e:
        shutil.rmtree('temp')
        print(f"{bg(1)}{attr(1)} REMOVED TEMP FOLDER {attr(0)}")

os.mkdir(f"temp")

print(f"{bg(2)}{attr(1)} CREATED TEMP FOLDER {attr(0)}")

folder = os.listdir(log)
for i in folder:
    namelogfile = namelogfile + 1;
    if(i != "latest.log"):
        with open(f'{log}/{i}', 'rb') as f:
            file_content = f.read()
        with gzip.GzipFile(fileobj=BytesIO(file_content)) as decompressed_file:
            decompressed_content = decompressed_file.read()

        with open(f'./temp/{namelogfile}.log', 'wb') as f:
            f.write(decompressed_content)
            print(f"{fg(2)}UNZIPPED {i} TO ./temp/{namelogfile}.log {attr(0)}")
    else:
        shutil.copy(f'{log}/latest.log', f'temp/{namelogfile}.log')
        print(f"{fg(2)} MOVED {i} TO ./temp/{namelogfile}.log {attr(0)}")


tempvar = 0;

tempfolder = os.listdir("temp")

for i in tempfolder:
    with open(f"./temp/{i}", "r", encoding='cp1250') as file:

        print(f"{bg(2)}{attr(1)} OPEN {i} LOOKING FOR HITS... {attr(0)}")

        tempvar = 0;

        try:
            for line in file:

                check = line.find("logged in with entity id")

                if(check != -1):
                    tempvar = 1
                    split = re.split(r'\s', line)
                    replace = split[3].replace("[", "")
                    replace = replace.replace("]", "")
                    replace = replace.replace("/", " ")
                    deleteport = replace.split(":")[0]
                    print(f"[!] {fg(2)}{attr(1)}HIT: {attr(0)} {fg(2)} {deleteport} ({i}) {attr(0)}")
                    allip.append(deleteport)

            if(tempvar == 0):
                print(f"[X] {fg(1)}{attr(1)} NO HITS FOUND ON {i} {attr(0)}")
        

        except Exception as e:
            print(f"[X] {fg(1)}{attr(1)} ERROR ON {i} ({e}){attr(0)}")
            pass

shutil.rmtree('temp')
print(f"{bg(1)}{attr(1)} REMOVED TEMP FOLDER {attr(0)}")
print(f"{bg(2)}{attr(1)} TY FOR USING :) GOODBYE! {attr(0)}")