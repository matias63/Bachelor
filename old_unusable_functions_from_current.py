
# OLD STUFF NOT USED ANYMORE 



# OLD STUFF FOR OLD V3 DATABASE 
def find_curr_id():
    rel_path = f"name_database"
    abs_file_path = os.path.join(script_dir, rel_path + "/*")
    list_of_files = glob.glob(abs_file_path)
    # latest_file = max(list_of_files, key=os.path.getctime)
    return len(list_of_files)


# OLD STUFF FOR V3 DATABASE 
def make_search_index():
    data = load_bulk()
    rel_path = f"search_index.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    index_dict = {}
    for i in data:
        name = i["name"].replace('//','--').replace('"','').replace('?','').replace('!','')
        index_dict[name] = ""
    with open(abs_file_path, 'w', encoding='utf-8', errors='ignore') as file:
        json.dump(index_dict,file)
# make_search_index()


# UN-USED in new setup
def cache_len():
    print(len(cache))


# OLD STUFF FOR PROTOTYPE DATABASE - With colored schemas
# Search for id
# def search_id(entry,local_cache,abs_file_path):    
     
# def search_id(search,colortable,local_cache):                          # changed to search name

    # for colour in colourtable:        TO DO!!!!!
    # create thread                     TO DO!!!!!
    # thread run through code below     TO DO!!!!!
    # path = f"name_database"
    # obj = os.scandir(path)
    # for entry in cache:
    #     if search in entry.name.lower() and entry.name  not in local_cache:
    #          if entry['layout'] != "art_series":
    #                 if 'image_uris' in entry:
    #                     local_cache[entry.name] = entry['image_uris']['normal']  # Update local_cache with the new entry
    #                 else:
    #                     local_cache[entry.name] = entry['card_faces'][0]['image_uris']['normal']
    # path = f"name_database"
    # obj = os.scandir(path)
    # for entry in obj:
    #     # binary search would probably be the way to go here
    #                                                                                         #INSERT THREAD for loop here instead of the one in thread search
    #     if search in entry.name.lower() and entry.name  not in local_cache:
    #         abs_file_path = os.path.join(script_dir, path,entry.name.lower())
            # print(script_dir+path+"\\"+entry.name.lower())
            # with open(abs_file_path, 'r') as library:
            #     data = json.load(library)
            #     # if 'image_uris' in data:
            #     #     if 'normal' in data['image_uris']:
            #     if data['layout'] != "art_series":
            #         if 'image_uris' in data:
            #             local_cache[entry.name] = data['image_uris']['normal']  # Update local_cache with the new entry
            #         else:
            #             local_cache[entry.name] = data['card_faces'][0]['image_uris']['normal']
                
    
        # if search == entry.name.lower():
        #     with open(abs_file_path, 'r') as library:
        #         data = json.load(library)
        #     local_cache = data[f'image_uris'][f'normal']
        #     break
    # rel_path = f"{colortable}.json"
    # abs_file_path = os.path.join(script_dir, rel_path)
    # with open(abs_file_path, 'r') as library:
    #     data = json.load(library)
    # for key in data:
    #     if search in key[f'name'].lower() and key[f'name']  not in local_cache:
    #         # print(key)
    #         # print(cachetest[key])
    #         # matches.append(cachetest[key])
    #         # print(key[f'image_uris'][f'normal'])
    #         local_cache[key[f'name']] = key[f'image_uris'][f'normal']
    #         # if exact name card is found
    #         if search == key:
    #             # stop threads          TO DO!!!
    #             #clear file + copy search
    #             local_cache = local_cache[key[f'name']] = key[f'image_uris'][f'normal']
    #             break
                # return

        
    # # search = input("Search: ")
    # # search color
    # for colour in Color:
    #     if search == colour.name:
    #         # print(search),print(colour.value)
    #         matching_cards = []
    #         for key,value in cache.items():
    #                 # print(str(value['colors']).strip("[]"))
    #                 if bool(re.search(colour.value,str(value['colors']).strip("[]"))):
    #                     #ORINGIAL VERSION WORKS
    #         #             matching_cards.append(data)
    #         #             print(value['name'])
    #         # with open("output_file", 'w', encoding='utf-8', errors='ignore') as file:
    #         #     json.dump(matching_cards,file, indent = 4)  
                          
    #                       # V2
    #                     rel_path = f"name_database/{key}.json"
    #                     abs_file_path = os.path.join(script_dir, rel_path)
    #                     start_time = time.time()
    #                     with open(abs_file_path, 'r') as library:
    #                         data = json.load(library)
    #                         matching_cards.append(data)
    #         with open("output_file.json", 'w', encoding='utf-8', errors='ignore') as file:
    #             json.dump(matching_cards,file, indent = 4) 

    #         print("Time taken: --- %s seconds ---" % (time.time() - start_time))
                        
    #                     # # V3
    #                     # # wont work if specifyng mana cost criteria  - therefore abandoning -- before fixing for multicolor
    #                     # start_time = time.time()
    #                     # shutil.copy(f"{search}.json", 'output_file.json')
    #                     # print("--- %s seconds ---" % (time.time() - start_time))
                            
            
            
            
    #     #search for card id
    #     else:
    #         start_time = time.time()
    #         rel_path = f"name_database/{search}.json"
    #         abs_file_path = os.path.join(script_dir, rel_path)
    #         with open(abs_file_path, 'r') as library:
    #             data = json.load(library)
    #         refill_cache(data)
    #         print("--- %s seconds ---" % (time.time() - start_time))
    #         return data['id'],data['name'],data
        


      

# UN-USED in new setup
def update():
    update_card = delete()
    create(update_card)



# UN-Used in new setup
def refill_cache(data):
    print("refill cache")
    for color_name in data["colors"]:
        for colour in Color:
            if  colour.value.search(color_name):
                # print(colour.name)
                with open(f"{script_dir}\{colour.name}.json", 'r') as library:
                    color_library = json.load(library)
                    for card in color_library:
                        # print("caching: ",card['id'])
                        # print(re.search('Creature',card['type_line']))
                        try:
                            if re.search('Creature',(card['type_line'])):
                                cache[card['name']] = ({'id' : card['id'],'colors':card['colors'],'mana_cost':card['mana_cost'],'type_line':card['type_line'],'power':card['power'],'toughness':card['toughness']})
                            else:  
                                cache[card['name']] = ({'id' : card['id'],'colors':card['colors'],'mana_cost':card['mana_cost'],'type_line':card['type_line']})
                        except: 
                            continue
    print("caching done")
              

# UN-USED in new setup
# def concurrent_update():
#     id,name,card = search_id()
#     rel_path = f"single_card_library/{id}.json"
#     abs_file_path = os.path.join(script_dir, rel_path)

#     print(os.stat(abs_file_path))
#     # dt = datetime.datetime.fromtimestamp(p.stat().st_ctime)
#     # create(id)
#     # update_card = delete()
#     # print(d)


#UN-USED
# helped out version (format = [dict,dict,dict, ....] with indentation)  
def build_colour_dbs():
    matching_cards = []

    # Load bulk data
    data = load_bulk()  # You need to define load_bulk() function

    # Hardcoded search string for testing
    search = input("Search color: ").lower() # example write: c=red

    # Extract color from search string
    reg_col = re.search('(c(olo(u)?r)?( )?=?)( )?(\w+)*', search)
    colour = reg_col.group(6)
    # print(colour)
    if colour == "red":
        colour_pattern = re.compile(
            '(\{([0-9|X])*\})*((\{(W\/|U\/|B\/|G\/)R\})|(\{R(\/W|\/U|\/B|\/G)\})|(\{R\}))+')
    if colour == "green":
        colour_pattern = re.compile(
            '(\{([0-9|X])*\})*((\{(W\/|U\/|B\/|R\/)G\})|(\{G(\/W|\/U|\/B|\/R)\})|(\{G\}))+')
    if colour == "white":
        colour_pattern = re.compile(
            '(\{([0-9|X])*\})*((\{(R\/|U\/|B\/|G\/)W\})|(\{W(\/R|\/U|\/B|\/G)\})|(\{W\}))+')
    if colour == "black":
        colour_pattern = re.compile(
            '(\{([0-9|X])*\})*((\{(W\/|U\/|R\/|G\/)B\})|(\{B(\/W|\/U|\/R|\/G)\})|(\{B\}))+')
    if colour == "blue":
        colour_pattern = re.compile(
            '(\{([0-9|X])*\})*((\{(W\/|R\/|B\/|G\/)U\})|(\{U(\/W|\/R|\/B|\/G)\})|(\{U\}))+')

    # Iterate through cards in data
    for card in data:
        for key, value in card.items():
            if key == 'mana_cost' and bool(re.search(colour_pattern, value)):
                matching_cards.append(card)
                # cache[card['id']] = card
    # Write matching cards to file
    output_file = f"{colour}.json"
    with open(output_file, 'w', encoding='utf-8', errors='ignore') as file:
            json.dump(matching_cards,file, indent = 4)
    print(f"Succesfully build {colour} table")


    
# un-tested - UN-USED
def clean():
    # remove SDB, recreate and populate
    path = './single_card_database'
    shutil.rmtree(path)
    os.mkdir(path)
    build_SDB()
    # remove red.json,create and populate 
    path = './red.json'
    os.remove(path)
    build_colour_dbs()


    