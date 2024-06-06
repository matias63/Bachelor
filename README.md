
###### Bachelor project READ-ME ######

### INSTALL packages ###
import json
from pathlib import Path
import os
import re
import glob
import shutil # to remove directories - clean()
import numpy
import time
import datetime 
import requests # get card images online - search id
from PIL import Image # convert bytes to images - search id
import io
import shutil # remove folders - thread_search
import threading


# OLD PACKAGES NOT USED ANYMORE
from enum import Enum # colour class for us in -  create()
import keyboard # for using buttons to navigate the database - main()
import ast
import datetime



### SETUP DATABASE ###
# Down load example test set and Create database:
python3 ./ Start_database.py
# this also shows info about the average text length of the database elements



# OPEN SERVER AND CLIENT ###
# - open 2 windows in the correct directory
# - open backend (server)
python3 ./backend.py
# - open frontend (client)
python3 ./client.py



### HOW TO USE ###
# the database can handle create, read, update, delete. - examples of operations are:
# search elf
# create name:Dog 
# create name:Dog, mana_cost:RGB          (creating an existing item UPDATES it)
# delete Dog





### VIEW LONGEST NAMES AND MEAN SYMBOL PER NAME ###
# in-comment find_item_length_mean() and find_item_length() in current.py (in comment the commands at the bottom and run current)
python3 ./current


### RUN TEST FILES ###
python3 ./test_concurrency_create_delete_connection_safety.py
python3 ./test_delete_create_mix.py
python3 ./test_delete_create_mix2.py
python3 ./test_overflooding.py
python3 ./test_search_algorithm.py
python3 ./test_V4_search_speed.py