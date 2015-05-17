import csv, json

from bs4 import BeautifulSoup
from progressbar import ProgressBar


with open('config.json', 'r') as fd:
    """ 'config.json' is of format:
         {
             "name": "fubar",
             "file": "path/to/facebook.data"
         }
    """
    config = json.load(fd)

def clean_partner_info(s):
    return s.replace(config['name'], '').replace(', ', '')

print('Opening file')
with open(config['file'], 'r') as fd:
    soup = BeautifulSoup(fd.read())

print('Loading content')
content = soup.find('div', {'class': 'contents'})
threads = content.find_all('div', {'class': 'thread'})

with open('messages.csv', 'w') as fd:
    cw = csv.writer(fd, quoting=csv.QUOTE_ALL)
    cw.writerow(['partner', 'message_origin', 'date', 'message'])

    pbar = ProgressBar(maxval=len(threads))
    pbar.start()
    for i, thread in enumerate(threads):
        partner = clean_partner_info(thread.contents[0])

        for msg in thread.find_all('div', {'class': 'message'}):
            msg_ori = msg.find('span', {'class': 'user'}).text
            meta = msg.find('span', {'class': 'meta'}).text
            msg = msg.next_sibling.text

            cw.writerow([partner, msg_ori, meta, msg])
        pbar.update(i)
    pbar.finish()
