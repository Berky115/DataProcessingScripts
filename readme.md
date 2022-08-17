***Data Processing Scripts***

A collection of scripts used to manage Tims related data.


json_export_scoring.py - Export scoring data:
  Description:
    - This script reaches out to an item database and pulls scoring information based on a .txt file, listing items to pull and generate. The intent is for Item migrations from one environment to another.

  Installation:
  - Python 3
  - pip
  - psycopg2

use:
  - Set the top most parameters to determine where you are pulling information from (host,db, user,password)
  - Generate an Eq as Json.txt file
  - set list of items you would like migration (each item on a new line)
  -  run script

