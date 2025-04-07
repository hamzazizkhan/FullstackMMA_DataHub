'''
x - date
y - win/loss +1/-1

label bars by name of fighter
'''

import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
from json import loads, dumps
import json


from sqlmodel import select, Session
from models import MMA_record, visited_links, profesional_record_data


# conn = sqlite3.connect('../data/fighters.sqlite')
# cur = conn.cursor()

# def individualStatsFig(fighterId, cur):

#     cur.execute('SELECT * FROM MMA_record WHERE fighterID= ?',(fighterId,)  )
#     rec = cur.fetchall()

#     resul_ind = 2
#     date_ind = 7 
#     opp_ind = 4
#     fighterId_index = 11
#     #print(rec)

#     rec = np.array(rec)
#     result = rec[:,resul_ind]

#     #print(result)

#     def check(result):
#         if result=='Win':
#             return(1)
#         elif result=='Draw':
#             return(0)
#         else:
#             return(-1)
#     result = list(result)
#     result = np.array(list(map(check, result)))
#     #print(result)

#     date = rec[:,date_ind]
#     opp = rec[:,opp_ind]
#     fighterId = rec[:,fighterId_index]

#     #print(date)
#     #print(opp)

#     color = ['yellow' if i==1  else 'red' for i in result  ]

#     plt.figure(figsize=(10, 3))  
#     plt.bar(date, result, color = color, label = opp)
#     plt.legend(bbox_to_anchor=(1, 1))
#     plt.xticks(rotation=90)
#     plt.yticks(result)
#     #plt.savefig(f'{fighterId}.png', bbox_inches='tight')

#     img_bytes = io.BytesIO()
#     plt.savefig(img_bytes, format='png', bbox_inches='tight',
#                 transparent=True)  # Save as PNG in memory
#     img_bytes.seek(0)  # Move cursor to the beginning

#     # Get binary data
#     binary_data = img_bytes.getvalue()  # Returns the image as binary

#     plt.close() 
#     return binary_data


def individualStatsFig(fighterId, cur):
    print(cur)
    rec = cur.exec(select(MMA_record).where(MMA_record.fighterID==fighterId)).all()
    # print(rec[0].result, type(rec))
    print([i.result for i in rec])

    resul_ind = 2
    date_ind = 7
    opp_ind = 4
    fighterId_index = 11
    # print(rec)

    rec = np.array(rec)
    # print(rec)
    
    result = np.array([i.result for i in rec])
    
    # print(result)

    def check(result):
        if result == 'Win':
            return (1)
        elif result == 'Draw':
            return (0)
        else:
            return (-1)
    result = list(result)
    result = np.array(list(map(check, result)))
    # print(result)

    date = np.array([i.date for i in rec])
    opp = np.array([i.opponent for i in rec])
    fighterId = np.array([i.fighterID for i in rec])

    color = ['yellow' if i == 1 else 'red' for i in result]

    plt.figure(figsize=(10, 3))
    plt.bar(date, result, color=color, label=opp)
    plt.legend(bbox_to_anchor=(1, 1))
    plt.xticks(rotation=90)
    plt.yticks(result)
    # plt.savefig(f'{fighterId}.png', bbox_inches='tight')

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png', bbox_inches='tight',
                transparent=True)  # Save as PNG in memory
    img_bytes.seek(0)  # Move cursor to the beginning

    # Get binary data
    binary_data = img_bytes.getvalue()  # Returns the image as binary

    plt.close()

    
    return binary_data


def individualStatsData(fighterId,df):
    # df = pd.read_csv('summaryStats.csv')
    # print('df in func \n')
    # print(df)
    fighter = df.loc[df['fighterId']==fighterId]
    # print('\n==========')
    # print(fighter.iloc[0,3], '============win P')
    # print(fighter.iloc[0,2], '============aveTime')
    winP = fighter.iloc[0,3]
    aveTime = fighter.iloc[0,2]

    winP = np.round(float(winP), 2)
    aveTime = np.round(float(aveTime), 2)
    d = {'winPercentage':str(winP), 'aveTime':str(aveTime)}
    return d

    # aveTime = fighter.iloc[fighter['aveTime']]
    # winP = fighter.loc['winPercentage']

    # print(aveTime)
    # print(winP)
# firstName = 'Dustin'
# lastName = 'Poirier'

# individualStatsFig(firstName, lastName)

# cur.close()
# conn.close()
# df = pd.read_csv('summaryStats.csv')
# d=individualStatsData(0, df)
# print(d)