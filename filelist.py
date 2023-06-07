# VERSION: 1.0
# AUTHORS: a-x00src

import json, re
from novaprinter import prettyPrinter
from helpers import retrieve_url

class filelist(object):

    # Settings ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Change! Find passkey here -> https://filelist.io/my.php
    username = "YOUR_USERNAME_HERE"
    passkey  = "YOUR_PASSKEY_HERE"
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # DO NOT TOUCH
    url = 'https://filelist.io'
    name = 'FileListQbt'
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    """
    ---------------------------------------
    FL Category Identifier | Good to know
    ---------------------------------------
    (toate) = null
    Filme SD = 1
    Filme DVD = 2
    Filme DVD-RO = 3
    Filme HD = 4
    FLAC = 5
    Filme 4k = 6
    Programe = 8
    Jocuri PC = 9
    Jocuri Console = 10
    Audio = 11
    Videoclip = 12
    Sport = 13
    Desene = 15
    Docs = 16
    Linux = 17
    Diverse = 18
    Filme HD-RO = 19
    Filme Blu-Ray = 20
    Seriale HD = 21
    Mobile = 22
    Seriale SD = 23
    Anime = 24
    Filme 3D = 25
    Filme 4k Blu-Ray = 26
    Seriale 4K = 27
    """
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
   
    supported_categories = {
		'all':		  '',			
		'books':	  '16',
		'games':	  '10,9',
		'movies':	  '25,6,26,20,2,3,4,19,1',
		'music':	  '5,11',
		'software':	  '17,22,8',		
		'tv':             '27,21,23,13,15',
    		'anime':	  '24'
	}
    
    @staticmethod
    def validate_imdb(query):
        pattern = r'^(?:.*\/)?(tt\d{7})\/?$'
        match = re.match(pattern, query)
        return match.group(1) if match else None

    def search(self, what, cat='all'):
        category = self.supported_categories.get(cat, '')
        imdb_check = self.validate_imdb(what)
        query_type = "name" if imdb_check is None else "imdb"
        search_query = imdb_check or what
        url = f"https://filelist.io/api.php?username={self.username}&passkey={self.passkey}&action=search-torrents&query={search_query}&category={category}&type={query_type}"
        response = retrieve_url(url)
        data = json.loads(response)
        for item in data:
            result = {
                'link': item['download_link'],
                'name': item['name'],
                'size': f"{item['size']} B",
                'seeds': item['seeders'],
                'leech': item['leechers'],
                'engine_url': self.url,
                'desc_link': f"https://filelist.io/details.php?id={item['id']}"
            }
            if 'freeleech' in item and item['freeleech'] == 1:
                result['name'] += ' [Freeleech]'
            if 'doubleup' in item and item['doubleup'] == 1:
                result['name'] += ' [Doubleup]'
            prettyPrinter(result)
