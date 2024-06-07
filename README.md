# Bachelor project READ-ME 

### CLONE LIBRARY ###
    - git clone https://github.com/matias63/Bachelor


### INSTALL packages ###
Install by running
pip install json
pip install pathlib

pip install re
pip install glob
pip install shutil
pip install numpy
pip install time
pip install datetime 
pip install requests
pip install PIL
pip install threading





### SETUP DATABASE ###
Download example test set and Create database:
This also shows info about the average text length of the database elements
    python3 ./ Start_database.py



### OPEN SERVER AND CLIENT ###
The back-end logs lock information and client actions
Open Back-end (server):
    python3 ./backend.py
Open Front-end (client)
    python3 ./client.py



### HOW TO USE ###
While in client:
The database can handle create, read, update, delete. - examples of operations are:
    search elf
    create name:Dog 
Creating an existing item UPDATES it
    create name:Dog, mana_cost:RGB          
    delete Dog





### VIEW LONGEST NAMES AND MEAN SYMBOL PER NAME ###
In-comment find_item_length_mean() and find_item_length() in current.py (in comment the commands at the bottom and run current)
    python3 ./current


### RUN TEST FILES ###
Change current algorithm manually in current.py by commenting in the algorithm you want to test in thread_search and thread_csearch_old
    python3 ./test_concurrency_create_delete_connection_safety.py
    python3 ./test_delete_create_mix.py
    python3 ./test_delete_create_mix2.py
    python3 ./test_overflooding.py
    python3 ./test_search_algorithm.py
    python3 ./test_V4_search_speed.py



### OLD PACKAGES - Only used for old part of code ###
pip install these if you want to test the old parts of the database. But IT PROBABLY IS NOT runnable anymore
    pip install enum 
    pip install keyboard
    pip install ast
