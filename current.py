import json
from pathlib import Path
import os
import ast
import re
import glob
import shutil # to remove directories - clean()
import numpy
import time
import datetime 
from enum import Enum # colour class for us in -  create()
import keyboard # for using buttons to navigate the database - main()
import requests # get card images online - search id
from PIL import Image # convert bytes to images - search id
import io
import shutil # remove folders - thread_search
import threading

class Color(Enum):
    red = re.compile('(([0-9|X])*)*(((W\/|U\/|B\/|G\/)R)|(R(\/W|\/U|\/B|\/G))|(R))+')
    green = re.compile('(([0-9|X])*)*(((W\/|U\/|B\/|R\/)G)|(G(\/W|\/U|\/B|\/R))|(G))+')
    white = re.compile('(([0-9|X])*)*(((R\/|U\/|B\/|G\/)W)|(W(\/R|\/U|\/B|\/G))|(W))+')
    black = re.compile('(([0-9|X])*)*(((W\/|U\/|R\/|G\/)B)|(B(\/W|\/U|\/R|\/G))|(B))+')
    blue = re.compile('(([0-9|X])*)*(((W\/|R\/|B\/|G\/)U)|(U(\/W|\/R|\/B|\/G))|(U))+')



# from https://www.geeksforgeeks.org/how-to-create-a-new-thread-in-python/
class thread(threading.Thread): 
    def __init__(self, thread_name, thread_ID): 
        threading.Thread.__init__(self) 
        self.thread_name = thread_name 
        self.thread_ID = thread_ID 
 
        # helper function to execute the threads
    def run(self): 
        print(str(self.thread_name) +" "+ str(self.thread_ID)); 


script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in



def find_item_length():
    path = f"search_index.json"
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)
    longest_name = 0
    for entry in data.keys():  
        if len(entry) > longest_name:
            longest_name = len(entry)
            print("item name:",entry)
            print("item length:",longest_name)
    print(f"longest name consists of:{longest_name} symbols")

def find_item_length_mean():
    path = f"search_index.json"
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)
    total_symbols = 0
    items_on_list = 0
    for entry in data.keys():  
        items_on_list +=1
        total_symbols += len(entry)
    average_length= total_symbols/items_on_list
    print("data set sample size:", items_on_list )
    print("average symbol lenth per item:", average_length )    


cache = {}


#open bulk file - not needed anymore
def load_bulk():
    # p = Path("C:\\Users\\enter\\Downloads").joinpath("scrapped_bulk.json") 
    rel_path = "scrapped_bulk.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)
    return data


# BUILD single card database - EVERYTHING INCLUDED -  {everything} line 1
def build_SDB():
    data = load_bulk()
    for i in data:   
        name = f'{i["name"]}'.replace('//','--').replace('"','').replace('?','').replace('!',''), f'{i}'
        rel_path = f"name_database/{name}.json"
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, 'w') as library:
            # library.write(json.dumps(i)) # ,separators = ("\n",":")
            # library.close()
            json.dump(i,library, indent = 4)

# Boyer-Moore Algorithm contributed on GeeksforGeeks contributed by Atul Kumar (www.facebook.com/atul.kr.007)
# https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/
# Knuth-Miller-Prath algortihm helper function
def computeLPSArray(pat, M, lps):
    len = 0 # length of the previous longest prefix suffix
 
    lps[0] # lps[0] is always 0
    i = 1
 
    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pat[i]== pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar 
            # to search step.
            if len != 0:
                len = lps[len-1]
            else:
                lps[i] = 0
                i += 1
 
# Boyer-Moore Algorithm contributed on GeeksforGeeks contributed by Atul Kumar (www.facebook.com/atul.kr.007)
# https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/
# Knuth-Miller-Prath algortihm (KMP) moded by me
def KMP_mod(pat, txt,M,lps):
    N = len(txt)
    j = 0 # index for pat[]
    i = 0 # index for txt[]
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1
        if j == M:
            return True
        # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return False


# Boyer-Moore Algorithm contributed on GeeksforGeeks contributed by Atul Kumar (www.facebook.com/atul.kr.007)
# https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/
# Knuth-Miller-Prath algortihm (KMP)
def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)

    # create lps[] that will hold the longest prefix suffix 
    # values for pattern
    lps = [0]*M
    j = 0 # index for pat[]
 
    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pat, M, lps)
 
    i = 0 # index for txt[]
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1
 
        if j == M:
            return True
 
        # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return False


# KMP Algorithm with bad character heuristic contributed on GeeksforGeeks by Bhavya Jain 
#https://www.geeksforgeeks.org/python-program-for-kmp-algorithm-for-pattern-searching-2/
# Bad character Heuristic for Boyer-Moore algorithm
NO_OF_CHARS = 256
def badCharHeuristic(string, size):
    badChar = [-1]*NO_OF_CHARS
    # Fill the actual value of last occurrence
    for i in range(size):
        badChar[ord(string[i])] = i
    # return initialized list
    return badChar

# KMP Algorithm with bad character heuristic contributed on GeeksforGeeks by Bhavya Jain 
#https://www.geeksforgeeks.org/python-program-for-kmp-algorithm-for-pattern-searching-2/
def Boyer_moore(txt, pat):
    m = len(pat)
    n = len(txt)
 
    # create the bad character list by calling
    badChar = badCharHeuristic(pat, m)
 
    # s is shift of the pattern with respect to text
    s = 0
    while(s <= n-m):
        j = m-1
        while j >= 0 and pat[j] == txt[s+j]:
            j -= 1
        # If the pattern is present at current shift,
        if j < 0:
            return True
        else:
            s += max(1, j-badChar[ord(txt[s+j])])
    else:
        return False


# Boyer-Moore Algorithm with bad character heuristic good suffix rule contribute on GeeksforGeeks by contributed by sanjeev2552
# https://www.geeksforgeeks.org/boyer-moore-algorithm-good-suffix-heuristic/
# preprocessing for strong good suffix rule
def preprocess_strong_suffix(shift, bpos, pat, m):

	# m is the length of pattern
	i = m
	j = m + 1
	bpos[i] = j

	while i > 0:
		
		'''if character at position i-1 is 
		not equivalent to character at j-1, 
		then continue searching to right 
		of the pattern for border '''
		while j <= m and pat[i - 1] != pat[j - 1]:
			
			''' the character preceding the occurrence 
			of t in pattern P is different than the 
			mismatching character in P, we stop skipping
			the occurrences and shift the pattern 
			from i to j '''
			if shift[j] == 0:
				shift[j] = j - i

			# Update the position of next border
			j = bpos[j]
			
		''' p[i-1] matched with p[j-1], border is found. 
		store the beginning position of border '''
		i -= 1
		j -= 1
		bpos[i] = j

# Boyer-Moore Algorithm with bad character heuristic good suffix rule contribute on GeeksforGeeks by contributed by sanjeev2552
# https://www.geeksforgeeks.org/boyer-moore-algorithm-good-suffix-heuristic/
# Preprocessing for case 2
def preprocess_case2(shift, bpos, pat, m):
	j = bpos[0]
	for i in range(m + 1):
		
		''' set the border position of the first character 
		of the pattern to all indices in array shift
		having shift[i] = 0 '''
		if shift[i] == 0:
			shift[i] = j
			
		''' suffix becomes shorter than bpos[0], 
		use the position of next widest border
		as value of j '''
		if i == j:
			j = bpos[j]

'''Search for a pattern in given text using 
Boyer Moore algorithm with Good suffix rule '''
# Boyer-Moore Algorithm with bad character heuristic good suffix rule contribute on GeeksforGeeks by contributed by sanjeev2552
# https://www.geeksforgeeks.org/boyer-moore-algorithm-good-suffix-heuristic/
def BM_with_good_suffix_rule(text, pat):

	# s is shift of the pattern with respect to text
	s = 0
	m = len(pat)
	n = len(text)

	bpos = [0] * (m + 1)

	# initialize all occurrence of shift to 0
	shift = [0] * (m + 1)

	# do preprocessing
	preprocess_strong_suffix(shift, bpos, pat, m)
	preprocess_case2(shift, bpos, pat, m)

	while s <= n - m:
		j = m - 1
		
		''' Keep reducing index j of pattern while characters of 
			pattern and text are matching at this shift s'''
		while j >= 0 and pat[j] == text[s + j]:
			j -= 1
			
		''' If the pattern is present at the current shift, 
			then index j will become -1 after the above loop '''
		if j < 0:
			return True
		else:
			
			'''pat[i] != pat[s+j] so shift the pattern 
			shift[j+1] times '''
			s += shift[j + 1]


# Qsearch Algorithm by github user mikolajp2137 https://github.com/Juliavister/AdvancedAlgorithms1/blob/main/Sunday.py
def sundaySearch(pattern, text):
    matches = []
    m = len(pattern)
    n = len(text)
    skip_table = {}
    for i in range(m):
        skip_table[pattern[i]] = m - i
    i = 0
    while i <= n - m:
        j = 0
        while j < m and (text[i + j] == pattern[j] or pattern[j] == "?"):
            j += 1
        if j == m:
            return True
        if i + m >= n:
            break
        if text[i + m] in skip_table:
            i += skip_table[text[i + m]]
        else:
            i += m + 1
    return False

# fetch images helper function - Thread_search
def fetch_pics(url, images):
    data = requests.get(url).content 
    image = Image.open(io.BytesIO(data))
    images.append(image)
    

# save image helper function - Thread_search
def saver(image:Image,search, j,rel_path):
    image.save(os.path.join(rel_path,f"{search}_cards_{j}.jpeg"),"JPEG")
    



# Search for id
def search_id(entry,local_cache,abs_file_path): 
    retries=3
    for i in range(0,retries): 
        try:  
            with open(abs_file_path, 'r') as library:
                data = json.load(library)
                # if 'image_uris' in data:
                #     if 'normal' in data['image_uris']:
                if data['layout'] != "art_series" and data['layout'] != "scheme":
                    if 'image_uris' in data:
                        local_cache[entry] = data['image_uris']['normal']  # Update local_cache with the new entry
                    else:
                        local_cache[entry] = data['card_faces'][0]['image_uris']['normal']
                return
        except Exception as e: 
            # NOTE: if card is in search_index, but cant find meta_data, try again (card must be updating)
            if i < retries:
                time.sleep(0.1)
            else:
                print("Could not find:",entry,"- Skipping card")  
                return
            
def KMP_mod_preperation(search):
    M = len(search)
    lps = numpy.array([0]*M)
    # # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(search, M, lps)
    return M, lps

def thread_search_before_indexing(search):
    try:
        # start_time = time.time()
        threads = []
        local_cache = {}
        path = f"name_database"
        obj = os.scandir(path)
        
        # M,lps = KMP_mod_preperation(search) # For use with KMP mod
        for entry in obj:
            # if KMPSearch(search,entry.name.lower()) and entry.name  not in local_cache:
            # if KMP_mod(search,entry.name.lower(),M,lps) and entry.name  not in local_cache:     # activate KMP_mod_prperation
            if search in entry.name.lower() and entry.name  not in local_cache:
            # if Boyer_moore(entry.name.lower(),search) and entry.name  not in local_cache:
            # if BM_with_good_suffix_rule(entry.name.lower(),search) and entry.name  not in local_cache: 
            # if sundaySearch(search,entry.name.lower()) and entry.name  not in local_cache:
                abs_file_path = os.path.join(script_dir, path,entry.name.lower())
                thread =threading.Thread(target = search_id, args = (entry,local_cache,abs_file_path))
                thread.start()
        threads.append(thread)
        for thread in threads:
            thread.join()
        # print("--- %s seconds ---" % (time.time() - start_time))
        return local_cache
    except:
        return "error"


def thread_search(search):
    # start_time = time.time()
    threads = []
    local_cache = {}
    path = f"search_index.json"
    
    # M,lps = KMP_mod_preperation(search) # For use with KMP mod
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            data = json.load(file)
        for entry in data.keys():                                                      
            # if KMPSearch(search,entry.lower()) and entry  not in local_cache:
            # if KMP_mod(search,entry.lower(),M,lps) and entry  not in local_cache: # activate KMP_mod_prperation
            if search in entry.lower() and entry  not in local_cache:
            # if BM_with_good_suffix_rule(entry.lower(),search) and entry  not in local_cache:
            # if Boyer_moore(entry.lower(),search) and entry  not in local_cache:
            # if sundaySearch(search,entry.lower()) and entry  not in local_cache:
                abs_file_path = os.path.join(script_dir, "name_database",entry+".json")
                try:
                    thread =threading.Thread(target = search_id, args = (entry,local_cache,abs_file_path))
                    threads.append(thread)
                    thread.start()
                except:
                    print("Could not find:",entry,"- Skipping card")   
        for thread in threads:
            thread.join()
        # print("--- %s seconds ---" % (time.time() - start_time))
        return local_cache
    except:
        return "error"
    
def image_processing(local_cache,search):
    try:
        # start_time = time.time()
        threads = []
        images = []
        for url in local_cache.values():
            thread =threading.Thread(target = fetch_pics, args = (url,images))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        # make dir for search images
        abs_file_path = os.path.join(script_dir, f"cards_{search}")
        if os.path.exists(abs_file_path):
            shutil.rmtree(abs_file_path)
        os.mkdir(abs_file_path)
        rel_path = f"cards_{search}"
        height = 680*4 
        combined_image = Image.new('RGB', (1952, height))
        x_offset = 0
        y_offset = 0
        i,j = 0,0
        for image in images:
            try:
                i += 1
                empty = False
                combined_image.paste(image, (x_offset, y_offset))
                if i % 4 == 0:
                    x_offset = 0
                    y_offset += image.height
                    if y_offset >= height:
                        j+=1
                        thread =threading.Thread(target = saver, args = (combined_image,search,j,rel_path))
                        threads.append(thread)
                        thread.start()
                        x_offset = 0
                        y_offset = 0
                        empty = True
                        combined_image = Image.new('RGB', (1952, height))
                else:
                    x_offset += image.width
            except Exception as e:
                print(f"Error processing image: {e}")
                return "error"
        if empty == False:
            j += 1
            combined_image.save(os.path.join(rel_path,f"{search}_cards_{j}.jpeg"),"JPEG")
        for thread in threads:
            thread.join()
        # combined_image.show()
        all_img = []
        for i in range(j+1):
            all_img.append(os.path.join(abs_file_path, f"{search}_cards_{i}.jpeg"))
        # print("--- %s seconds ---" % (time.time() - start_time))
        return all_img
    except:
        return "error"
    
  
    
                


# Create new card in name_database (some features left out)
# Replaces the original so also updates. All data viewed is downloaded images, so wont disturb a search
# GUIDE:
# create name:EXAMPLE_NAME, Attribute_1:Parameter_1 (and so on)
def create(param):
    # imput manipulator and extract the name
    card ={}
    pair = param.split(", ")
    for p in pair:
        key, value = p.split(":")
        card[key] = value
    n = ""
    for i in card:
        if i == "name":
            n = card["name"]
    n = n.title()
    # put in SDB
    rel_path = f"name_database"
    with open(script_dir+"\\"+rel_path+"\\"+n+".json", 'w') as library:
        json.dump(card,library, indent = 4)
    print("created card:", n)
    return n
  

# deletes a card if possible or else tells it doesnt exist
def delete(card_name: str):
    try:
        rel_path = f"name_database/{card_name}.json"
        abs_file_path = os.path.join(script_dir, rel_path)
        # Delete card
        os.remove(abs_file_path)    
        return card_name +" is removed from SDB"
    except: 
        return card_name +" Doesn't exist"












# OLD KEYBOARD  UI
# def main():
    # print("q = quit")
    # print("+ = create")
    # print("- = delete")
    # print(". = update")
    # print("8 = build color database")
    # print("9 = build single card database")
    # print("1 = search for card")
    # print("2 = search cache")

    # while True: 
    #     try:  
    #         if keyboard.is_pressed('q'):   
    #             break  # finishing the loop
    #         if keyboard.is_pressed('+'): 
    #             print("creating")
    #             create()
    #         # if keyboard.is_pressed('8'): 
    #         #     print("building color")
    #         #     build_colour_dbs()

    #         # if keyboard.is_pressed('9'):  
    #         #     print("building single card")
    #         #     build_SDB()
    #         if keyboard.is_pressed('1'):   
    #             print("searching")
    #             id, name, card = search_id()

    #             print(id,name,card)
    #             print("done")
    #         if keyboard.is_pressed('-'):  
    #             print("deleting")
    #             card_id = delete()
    #         if keyboard.is_pressed('.'):  
    #             print("updating")
    #             update()
    #             # concurrent_update()
    #         if keyboard.is_pressed('2'):  
    #             print("showing cache")
    #             print(cache[input()],"\n")
    #     except:
    #         # print("\nENDED")
    #         # break
    #         continue





# if __name__ == "__main__":
#     main()





# find_item_length_mean()
# find_item_length()
