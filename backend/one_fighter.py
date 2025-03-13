import requests
from bs4 import BeautifulSoup
import os
from main_table import tables
import sqlite3
import pandas as pd
import numpy as np

# conn = sqlite3.connect('fighters.sqlite')
# cur = conn.cursor()


def check_tables_update(cur):
    cur.execute('SELECT * FROM profesional_record_data')
    have = len(cur.fetchall())

    cur.execute('SELECT * FROM visited_links')
    all = len(cur.fetchall())

    diff = all-have
    print(f'number of fighters in visited links {all} - fighters in profesional_record_data {have} = {diff} \n missing {diff} entries' )

    start_row = all-diff
    print(f'write to text from row {start_row} in visited links')
    return(diff,start_row)

def write_to_txt(diff, start_row, cur):
    fighters = open('fighters.txt','w')
    file = open('main_table.txt', 'w')


    if diff==0:
        start=False
        return
    else:
        start=True

    cur.execute('SELECT firstName, lastName, html FROM visited_links')
    data = cur.fetchall()
    if start:
        for row_index in range(start_row,len(data)):
            #print(row[0])
            html = data[row_index][2]
            fighter_name, prof_rec_table, main_rec_table = tables(html)
            #print(fighter_name, row_index)

            prof_rec_data = {}
            prof_rec_list = prof_rec_table.tbody.get_text().split()

            for i in range(len(prof_rec_list)):
                if i%2==0 and i<6:
                    prof_rec_data[prof_rec_list[i+1]] = prof_rec_list[i]
                if prof_rec_list[i]=='By':
                    prof_rec_data[prof_rec_list[i+1]+ 'Wins'] =  prof_rec_list[i+2]
                    prof_rec_data[prof_rec_list[i+1]+ 'Losses'] =  prof_rec_list[i+3]
            # print('\n')
            # print(prof_rec_data)

            # writing to text file
            
            fighters.write('firstName '+fighter_name.split()[0] + ' ')
            fighters.write('lastName '+fighter_name.split()[1] + ' ')

            for k,v in prof_rec_data.items():
                text = k + ' '+v + ' '
                fighters.write(text)
            fighters.write('\n')

            ################################ main table

            # print('\n')
            # print('=================')

            
            file.write(fighter_name.split()[0] + ' ' + fighter_name.split()[1]+ '// ')

            rows = main_rec_table.find_all('tr')
            qu = []
            i=0
            rowspan = []
            inserts=0
            for row in rows:
                if i ==0:
                    i=1
                    continue
                #print(row)
                td = row.find_all('td')
                text = [td_tag.text.strip() for td_tag in td]
                
                
                if len(rowspan)!=0:
                    for ele in rowspan:
                        text_insert = ele[0]
                        index_insert = ele[1]
                        
                        text.insert(index_insert, text_insert)
                    if inserts==1:
                        rowspan=[]
                        inserts=0
                    else:
                        inserts-=1

                else:
                    #rowspan = [(int(td_tag['rowspan'])-1, td_tag.text.strip(), i) for i, td_tag in enumerate(td) if 'rowspan' in td_tag.attrs]
                    for i, td_tag in enumerate(td):
                        if 'rowspan' in td_tag.attrs:
                            rowspan.append((td_tag.text.strip(), i))
                            inserts = int(td_tag['rowspan'])-1
                if len(text)<10:
                    diff = 10-len(text)
                    for _ in range(diff):
                        text.append('Null')


                #print(rowspan)

                #print('=================')
                

                for word in text:
                    file.write(word + '// ')

                #print('=================')
            file.write('\n')


        file.close()
        fighters.close()

    print('program started?', start)

def appendToSql(diff, start_row, cur, conn):
    if diff==0:
        start=False
        return
    else:
        start=True

    cur.execute('SELECT firstName, lastName, html FROM visited_links')
    data = cur.fetchall()
    if start:
        for row_index in range(start_row,len(data)):
            #print(row[0])
            html = data[row_index][2]
            fighter_name, prof_rec_table, main_rec_table = tables(html)
        
            prof_rec_data = {}
            prof_rec_list = prof_rec_table.tbody.get_text().split()

            first_name=fighter_name.split()[0]
            last_name = fighter_name.split()[1]


            if len(prof_rec_list)<16:
                print('hereeeeeee')
                print(fighter_name)
                print(prof_rec_list)

            prof_rec_data['firstName'] = [first_name]
            prof_rec_data['lastName'] = [last_name]
            prof_rec_data['matches'] = int(prof_rec_list[0])
            prof_rec_data['wins'] = int(prof_rec_list[2])
            prof_rec_data['losses'] = int(prof_rec_list[4])

            knockInd=prof_rec_list.index('knockout')
            prof_rec_data['knockoutWins'] = int(prof_rec_list[knockInd+1])
            prof_rec_data['knockoutLosses'] = int(prof_rec_list[knockInd+2])
            
            try:
                subInd=prof_rec_list.index('submission')
                prof_rec_data['submissionWins'] = int(prof_rec_list[subInd+1])
                prof_rec_data['submissionLosses'] = int(prof_rec_list[subInd+2])
            except:
                prof_rec_data['submissionWins'] = 0
                prof_rec_data['submissionLosses'] = 0
            decInd=prof_rec_list.index('decision')
            prof_rec_data['decisionWins'] = int(prof_rec_list[decInd+1])
            prof_rec_data['decisionLosses'] = int(prof_rec_list[decInd+1])

          
            

            # print(prof_rec_list)
            # print('\n')
            # print(prof_rec_data)

            #print(prof_rec_data)
            # if 'loss' in prof_rec_data.keys(): 
            #     print(prof_rec_data)
            #     print(prof_rec_list)
            df_prof = pd.DataFrame(prof_rec_data)
            
            #print(df_prof)

            # Export the DataFrame to the SQLite database
            table_name = 'profesional_record_data'
            df_prof.to_sql(table_name, conn, if_exists='append', index=False)

            ################################ main table

            MMA_record = {'firstName':[], 'lastName':[], 'result':[], 'record':[], 'opponent':[], 'result':[], 'method':[], 'event':[], 'date':[], 
              'round':[], 'time':[], 'location':[], 'notes':[]}

            rows = main_rec_table.find_all('tr')
            qu = []
            i=0
            rowspan = []
            inserts=0
            texts=[]
            for row in rows:
                if i ==0:
                    i=1
                    continue
                #print(row)
                td = row.find_all('td')
                text = [td_tag.text.strip() for td_tag in td]


                if len(rowspan)!=0:
                    for ele in rowspan:
                        text_insert = ele[0]
                        index_insert = ele[1]
                        
                        text.insert(index_insert, text_insert)
                    if inserts==1:
                        rowspan=[]
                        inserts=0
                    else:
                        inserts-=1

                else:
                    #rowspan = [(int(td_tag['rowspan'])-1, td_tag.text.strip(), i) for i, td_tag in enumerate(td) if 'rowspan' in td_tag.attrs]
                    for i, td_tag in enumerate(td):
                        if 'rowspan' in td_tag.attrs:
                            rowspan.append((td_tag.text.strip(), i))
                            inserts = int(td_tag['rowspan'])-1
                if len(text)<10:
                    diff = 10-len(text)
                    for _ in range(diff):
                        text.append('Null')

                texts.append(text)

            #print(texts)

            for val in range(len(texts)):
                MMA_record['firstName'].append(first_name)
                MMA_record['lastName'].append(last_name)

            # print('\n')
            # print(MMA_record)

            # print('\n===')
            texts = np.array(texts)

            MMA_record['result'] = list(map(lambda x:x[0], texts[:,0:1]))
            MMA_record['record'] = list(map(lambda x:x[0], texts[:,1:2]))
            MMA_record['opponent'] = list(map(lambda x:x[0], texts[:,2:3]))
            MMA_record['method'] = list(map(lambda x:x[0], texts[:,3:4]))
            MMA_record['event'] = list(map(lambda x:x[0], texts[:,4:5]))
            MMA_record['date'] = list(map(lambda x:x[0], texts[:,5:6]))
            MMA_record['round'] = list(map(lambda x:x[0], texts[:,6:7]))
            MMA_record['time'] = list(map(lambda x:x[0], texts[:,7:8]))
            MMA_record['location'] = list(map(lambda x:x[0], texts[:,8:9]))
            MMA_record['notes'] = list(map(lambda x:x[0], texts[:,9:10]))

            df_MMArecord = pd.DataFrame(MMA_record)

            # # Export the DataFrame to the SQLite database
            table_name = 'MMA_record'
            df_MMArecord.to_sql(table_name, conn, if_exists='append', index=False)



# if __name__=="__one_fighter__":
#     pass

# diff, start_row = check_tables_update()
# write_to_txt(diff,start_row)