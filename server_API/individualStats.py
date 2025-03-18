'''
x - date
y - win/loss +1/-1

label bars by name of fighter
'''

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# conn = sqlite3.connect('../data/fighters.sqlite')
# cur = conn.cursor()

def individualStatsFig(firstName, lastName, cur):

    cur.execute('SELECT * FROM MMA_record WHERE (firstName, lastName)= (?,?)',(firstName,lastName)  )
    rec = cur.fetchall()

    resul_ind = 2
    date_ind = 7 
    opp_ind = 4

    print(rec)

    rec = np.array(rec)
    result = rec[:,resul_ind]

    print(result)

    def check(result):
        if result=='Win':
            return(1)
        elif result=='Draw':
            return(0)
        else:
            return(-1)
    result = list(result)
    result = np.array(list(map(check, result)))
    print(result)

    date = rec[:,date_ind]
    opp = rec[:,opp_ind]
    print(date)
    print(opp)

    color = ['green' if i==1  else 'red' for i in result  ]

    plt.figure(figsize=(10, 3))  
    plt.bar(date, result, color = color, label = opp)
    plt.legend(bbox_to_anchor=(1, 1))
    plt.xticks(rotation=90)
    plt.yticks(result)
    plt.savefig(f'{firstName}_{lastName}.png', bbox_inches='tight')


# firstName = 'Dustin'
# lastName = 'Poirier'

# individualStatsFig(firstName, lastName)

# cur.close()
# conn.close()