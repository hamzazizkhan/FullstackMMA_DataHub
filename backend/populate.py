import requests
from bs4 import BeautifulSoup
import os
from main_table import tables
import sqlite3

from one_fighter import check_tables_update, write_to_txt, appendToSql
from fighterDB import add_to_main_table, add_to_prof_rec

conn = sqlite3.connect('.../data/fighters.sqlite')
cur = conn.cursor()

diff, start_row = check_tables_update(cur)
# alrdy checks for diff - write_to_txt

textVersion = False

if textVersion:
    write_to_txt(diff,start_row, cur)

    if diff!=0:
        add_to_prof_rec(cur)
        conn.commit()
        add_to_main_table(cur)
        conn.commit()
    else:
        print('prof_record_data and MMA_record tables up to date!')

    cur.close()
else:
    if diff!=0:
        
        appendToSql(diff,start_row, cur, conn)
        
        conn.commit()
        cur.close()
    else:
        print('prof_record_data and MMA_record tables up to date!')
    