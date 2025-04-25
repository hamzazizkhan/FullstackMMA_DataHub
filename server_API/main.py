from flask import Flask,  send_file, request, abort, jsonify
import sqlite3
from contextlib import contextmanager
import json
from flask_cors import CORS, cross_origin
import pandas as pd

from .individualStats import individualStatsFig, individualStatsData

summaryStats = open('./summaryStats.json', 'r')
summaryStats = json.load(summaryStats)
summaryStatsData = pd.read_csv('summaryStats.csv', index_col=False)
# print(summaryStatsData, 'summmary here ====================================')


app = Flask(__name__)
CORS(app)

dburl = '../../data/fighters.sqlite'


@contextmanager
def db_connect():
    db = sqlite3.connect(dburl)
    cur = db.cursor()

    try:
        yield cur
    finally:
        cur.close()
        db.close()


@app.route('/')
def start():
    return 'hello MMA Data Hub'


@app.route('/api/summaryStats')
def handle_summaryStats():
    numFights = str(summaryStats['numFights'])
    numFighters = str(summaryStats['numFighters'])

    val = numFights+'/'+numFighters

    print('summaryStats')
    print(numFighters, 'num fighters', numFights, 'num fights')
    print('val', val)

    return val


@app.route('/summaryStatsImage')
def handle_summaryStatsImage():
    return send_file('summaryStats.png', mimetype='image/jpeg')


@app.route('/fiftyFighters')
def handle_fifityFighters():
    print('fiftyFIGHTERs========')
    with db_connect() as cur:
        cur.execute('SELECT firstName, lastName, fighterId FROM profesional_record_data LIMIT 50')
        data = cur.fetchall()
        print(data)
    
    return jsonify(data)


@app.route('/individualStatsFig')
def handle_individualStatsFig():
    fighterId = request.args.get('fighterId')
    with db_connect() as cur:        
        img = individualStatsFig(fighterId, cur)
    return img , {'Content-Type': 'image/jpeg'}

@app.route('/individualStatsData')
def handle_individualStatsData():
    fighterId = request.args.get('fighterId')
    print(summaryStatsData, 'summmary here ====================================')

    fighterId = int(fighterId)
    data = individualStatsData(fighterId, summaryStatsData)
    return data



@app.route('/search')
def handle_search():
    fighterName = request.args.get('fighterName')

    nameInd = fighterName.find(',')+1
    fname = fighterName[0:nameInd-1]
    lname = fighterName[nameInd:]

    with db_connect() as cur:
        cur.execute('SELECT fighterID FROM visited_links WHERE (firstName, lastName) =(?,?)', (fname, lname) )
        fighterId=cur.fetchone()

    if fighterId:
        print(fname, lname,
              fighterId[0], '===========================================================================')
        data = individualStatsData(fighterId[0], summaryStatsData)
        return data
    else:
        raise abort(404, 'fighter not found')


@app.route('/searchImage')
def handle_searchImage():
    fighterImage = request.args.get('fighterImage')

    
    nameInd = fighterImage.find(',')+1
    fname = fighterImage[0:nameInd-1]
    lname = fighterImage[nameInd:]

    with db_connect() as cur:
        cur.execute(
            'SELECT fighterID FROM visited_links WHERE (firstName, lastName) =(?,?)', (fname, lname))
        fighterId = cur.fetchone()

        if fighterId:
            print(fname, lname,
                fighterId[0], '===========================================================================')
            img = individualStatsFig(fighterId[0], cur)
            return img, {'Content-Type': 'image/jpeg'}
        else:
            raise abort(404, 'fighter not found')


# @app.route('/searchImage')
# def handle_searchImage(fighterImage: str, session: sessionDep):
