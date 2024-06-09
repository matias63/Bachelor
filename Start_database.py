import current as c
import requests 
import json
import os

def scrape(url):
    response = requests.get(url)
    data = response.json()
    with open('scrapped_bulk.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def empty_lib():
    directory_path = "C:/Users/enter/Desktop/bachelor Datalogi/git_project/Bachelor/name_database"
    os.makedirs(directory_path)

# BUILD single card database
def build_SDB():
    data = c.load_bulk()
    script_dir = os.path.dirname(__file__)
    for i in data:   
        name = f'{i["name"]}'.replace('//', '--').replace('"', '').replace('?', '').replace('!', '')
        rel_path = f"name_database/{name}.json"
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, 'w') as library:
            json.dump(i, library, indent=4)

def main():
    print("Downloading example test set - It may take a minute (this set may have increased in size since I started the project.)")
    url = 'https://data.scryfall.io/default-cards/default-cards-20240606090554.json'
    scrape(url)
    empty_lib()
    print("Building database with example test set. It may take several minutes")
    build_SDB()
    c.find_item_length()
    c.find_item_length_mean()


if __name__ == "__main__":
    main()
