# see https://smarterbalanced.atlassian.net/wiki/spaces/IAT/pages/521175097/5.X4+Import+EQ+scoring+for+QTI

###########################################################################
#     Exports scoring json to flat files for migration
###########################################################################

# See https://docs.python.org/3/library/json.html
import csv
import json
import psycopg2
import time
import datetime
import getopt, sys
import os



### Log into DB
DB_HOST = "imrt-stage-cluster-v12-us-west-2b.c7g9woytu6d2.us-west-2.rds.amazonaws.com"
DB_NAME = "imrt"
DB_USER = "user"
DB_PASS = "pwd"

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS)


cur = conn.cursor()




###########################################################################



print("running ")

print("opening 'EQ to Migrate.txt'")

file = open("EQ to Migrate.txt")
lines = file.readlines()

items = []
for i in lines[2:]:
    items.append(int(i[:-1]))

# creating folder
current_dir = (os.getcwd())
json_folder = "\\ScoringJSON"
json_folder_path = current_dir + json_folder

if not os.path.isdir(json_folder_path):
    os.makedirs(json_folder_path)
    print(json_folder_path + " was created for svg files")
else:
    print("svg files will saved to " + json_folder_path)

cur.execute("""select id, item_version, item_json -> 'core' -> 'scoring' from public.item where is_published = false AND
id IN ("""+str(items)[1:-1]+"""
)""")
rows = cur.fetchall()

print("Writing files to folder 'ScoringJSON'")

for r in rows:
    scoring_json = r[2]
    scoring_json["rubric"] = []
    del scoring_json["rubric"]
    del scoring_json["machineScoringManagedByIat"] 
    del scoring_json["isManagedByIat"]
    file_name = str(r[0]) + "." + "qti-scoring.json" 	
    a_file = open(json_folder_path+"\\"+file_name,"w")
    json.dump(scoring_json,a_file,indent=4)  
    a_file.close()	
    #rules_length = len(scoring_json["core"]["scoring"]["rules"])
    #print(rules_length)
    #print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    #print(scoring_json["core"]["scoring"])



###########################################################################
#                           TEST CASES END --> UPDATE CDS
###########################################################################
cur.close()
conn.close()



