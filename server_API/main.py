
import matplotlib.pyplot as plt
import io

from individualStats import individualStatsFig, individualStatsData
import json
import pandas as pd
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from fastapi import Depends, FastAPI, HTTPException, Query, Response, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

from models import MMA_record, visited_links, profesional_record_data

summaryStats = open('summaryStats.json', 'r')
summaryStats = json.load(summaryStats)
summaryStatsData = pd.read_csv('summaryStats.csv', index_col=False)
'''
    CREATE TABLE IF NOT EXISTS MMA_record (firstName TEXT, lastName TEXT, result TEXT, record NUMERIC, opponent TEXT, method TEXT, event TEXT,
                date DATE, round INT, time NUMERIC, location TEXT, notes TEXT, fighterID INT)
    '''



db = '../data/fighters.sqlite'
dbURL = f'sqlite:///{db}'
args = {'check_same_thread': False}
engine = create_engine(dbURL, connect_args=args)


def db_and_tables():
    SQLModel.metadata.create_all(engine)

def start_session():
    with Session(engine) as session:
        yield session

sessionDep = Annotated[Session, Depends(start_session)]        

def lifespan(app:FastAPI):
    db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:50000", 
    'http://127.0.0.1:8080',
    'http://172.20.10.2:8080'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Or specify: ["GET", "POST", ...]
    allow_headers=["*"],  # Or specify: ["Content-Type", "Authorization"]
)

@app.get('/summaryStats')
def handle_summaryStats():
    numFights = str(summaryStats['numFights'])
    numFighters = str(summaryStats['numFighters'])
    val = numFights+'/'+numFighters
    return val


@app.get('/summaryStatsImage')
def handle_summaryStatsImage():
    return FileResponse('summaryStats.png', media_type='image/jpeg')


@app.get('/fiftyFighters')
def handle_fifityFighters(session: sessionDep, 
                          limit: int = 50)-> JSONResponse:
    fiftyFighters = session.exec(
        select(profesional_record_data).limit(limit)).all()
    print(fiftyFighters)
    return fiftyFighters


@app.get('/individualStatsFig')
def handle_individualStatsFig(fighterId: int, session: sessionDep):
    print('ind stats fig handler')

    img = individualStatsFig(fighterId, session)

    
    return Response(content = img, media_type='image/jpeg')


@app.get('/individualStatsData')
def handle_individualStatsFig(fighterId: int, session: sessionDep):
    print('ind stats data handler')

    data = individualStatsData(fighterId, summaryStatsData)
    print(data, 'dattaaaaaaaaaa')
    return data

    # return Response(data, 'json/application')

@app.get('/search')
def handle_search(fighterName: str, session: sessionDep)->dict:
    nameInd = fighterName.find(',')+1
    fname = fighterName[0:nameInd-1]
    lname = fighterName[nameInd:]

    fighterID = session.exec(select(visited_links.fighterID).where(visited_links.firstName==fname).where(visited_links.lastName==lname)).all()

    
    if len(fighterID) > 0:
        print(fname, lname,
              fighterID[0], '===========================================================================')
        data = individualStatsData(fighterID[0], summaryStatsData)
        return data
    else:
        raise HTTPException(status_code=404, detail='fighter not found')
    

@app.get('/searchImage')
def handle_searchImage(fighterImage: str, session: sessionDep):
    nameInd = fighterImage.find(',')+1
    fname = fighterImage[0:nameInd-1]
    lname = fighterImage[nameInd:]

    fighterID = session.exec(select(visited_links.fighterID).where(
        visited_links.firstName == fname).where(visited_links.lastName == lname)).all()
  
    
    if len(fighterID) > 0:
        print(fname, lname,
              fighterID[0], '===========================================================================')
        img = individualStatsFig(fighterID[0], session)
        return Response(img, media_type = 'img/jpeg')
    else:
        raise HTTPException(status_code=404, detail='fighter not found')


