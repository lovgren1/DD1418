import bs4
import sys
import requests

wiki_page = 'Elon_Musk'
res = requests.get(f'https://sv.wikipedia.org/wiki/{wiki_page}' )
res.raise_for_status()
wiki = bs4.BeautifulSoup(res.text,"html.parser")

# open a file named as your wiki page in write mode
with open(wiki_page+".txt", "w", encoding="utf-8") as f:
    for i in wiki.select('p'):
        # write each paragraph to the file
        f.write(i.getText())