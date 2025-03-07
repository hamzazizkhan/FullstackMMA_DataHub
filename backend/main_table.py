import sqlite3
import requests
from bs4 import BeautifulSoup
import os

# returns prof rec table and main table
def tables(html_content):
    # html_content=requests.get(link).text
    #print(html_content)
    soup = BeautifulSoup(html_content, "html.parser")

    fighter_name = soup.find('h1').get_text()
    heading_two = soup.find_all('h2')


    prof_rec_table = None
    main_rec_table = None
    
    for heading in heading_two:
        # Mixed martial arts record section
        if 'id' in heading.attrs:
            if heading['id'].lower()=='Mixed_martial_arts_record'.lower():

                #print('found Mixed martial arts record section')
                # print(heading)

                # Professional record breakdown table
                for ele in heading.next_elements:
                    if ele.name == 'table':
                        prof_rec_table = ele
                        #print('found Professional record breakdown table \n')
                        #print(prof_rec_table.prettify)
                        break

                # MMA record table
                for ele in prof_rec_table.next_elements:
                    if ele.name == 'table':
                        main_rec_table = ele
                        #print('found main rec table \n')
                        # print(main_rec_table.prettify)
                        break
                #print('=================')
                break
    
    return(fighter_name, prof_rec_table, main_rec_table)

def links_qu(main_rec_table):
    #print(main_rec_table)
    rows = main_rec_table.find_all('tr')

    qu = []
    i=0
    for row in rows:
        if i ==0:
            i=1
            continue
        #print(row)
        td = row.find_all('td')
        #print('=================')
        #print('fighters link!')
        opponent = td[2]

        a_tag = opponent.a
        if a_tag is not None:
            href = a_tag['href']
            link = 'https://en.wikipedia.org'+href
            if link not in qu:
                qu.append(link)
        #print('=================')
    return(qu)

def get_qu_str(html, tables, links_qu, all_hrefs=[]):
    fighter_name, prof_rec_table, main_rec_table = tables(html)

    first_name = fighter_name.split()[0]
    last_name = fighter_name.split()[1]

    if main_rec_table is None:
        return (first_name, last_name, '')


    qu = links_qu(main_rec_table)
    #print(qu)

    qu_str = ''
    for e in qu:
        if (e,) in all_hrefs: 
            print(f'this link was skipped {e} from {fighter_name.split()[0]}')
            continue
        qu_str = qu_str + e + ' '

    

    return (first_name, last_name, qu_str)





