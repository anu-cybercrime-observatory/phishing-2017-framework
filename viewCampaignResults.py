#!/usr/bin/python3

# Print the template out to the screen.

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

with open("htmlTemplates/viewCampaignResults.html") as inputFile:
    lines = inputFile.readlines()

for line in lines:
    line = line.strip()
    print(line)
