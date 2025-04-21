
class tableList extends HTMLLIElement{
    constructor(){
        super();
    }
}
customElements.define(
    'table-list',
    tableList,
    {extends:'li'}
);
let api = 'https://mmadatahub.co.ke:8000';

async function populateSummary(){
    const summary = document.querySelector('.summary');
    const interestingFindEle = document.querySelector('.interestingFind');
    const interestingFind = document.createElement('p');
    const numFightsEle = document.createElement('li');
    const numFightersEle = document.createElement('li');

    let route = '/summaryStats'
    let url = api+route;

    const request = new Request(url);
    const response = await fetch(request).catch((e)=>{
        console.log('error in fetching summaryStats');
        console.error(e);
    });

    const summaryStats = await response.text().catch((e)=>{
        console.log('error in getting summaryStats text')
        console.error(e)
    })
    // numFighters.textContent = `collected data on ${lengthOfData} fighters`;

    // summary.appendChild(numFighters);
    numFights = summaryStats.slice(1, summaryStats.indexOf('/'));
    numFighters = summaryStats.slice(summaryStats.indexOf('/') + 1,-1);

    numFightsEle.textContent=`colected data on ${numFights} fights`;
    numFightersEle.textContent=`for ${numFighters} individual fighters`;
    
    interestingFind.textContent = 'upon analysing the rest times of fighters, it was found that those who take 138-167 days between fights (four and a half to five and a half months) have a higher median win percentage'

    summary.appendChild(numFightsEle);
    summary.appendChild(numFightersEle);
    interestingFindEle.appendChild(interestingFind);

    fig = document.createElement('figure');
    // figcap = document.createElement('figcaption');
    // figcap.innerText='an interesting finding';
    
    console.log('the response from my server for summaryStats: ', numFights, numFighters);
    
    let route2 = '/summaryStatsImage';
    url = api+route2;

    const requestImage = new Request(url);
    const respImage = await fetch(requestImage).catch((e)=>{
        console.log('error in fetching respImage');
        console.error(e);
    });
    const summaryStatsImage=document.createElement('img');
    const im = await respImage.blob();
    summaryStatsImage.setAttribute('src', URL.createObjectURL(im));

    fig.appendChild(summaryStatsImage);
    // fig.appendChild(figcap);

    interestingFindEle.appendChild(fig)
    populateFightersList();
}


async function populateFightersList(){
    const fightersList = document.querySelector('.fightersList');

    let route = '/fiftyFighter';
    let url = api+route;

    const request = new Request('url');
    const response = await fetch(request).catch((e)=>{
        console.log('error in getting fighter');
        console.error(e);
    })

    const allFighters = await response.json().catch((e)=>{
        console.log('error in parsing json from server for fighters')
        console.error(e);
    });
    console.log('response for allFighters',allFighters);

    for (fighter of allFighters){
        const firstName = fighter['firstName'];
        const lastName = fighter['lastName'];
        // const matches = fighter['matches'];
        // const wins = fighter['wins'];
        // const losses = fighter['losses'];
        // const knockoutWins = fighter['knockoutWins'];
        // const knockoutLosses = fighter['knockoutLosses'];
        // const submissionWins = fighter['submissionWins'];
        // const submissionLosses = fighter['submissionLosses'];
        // const decisionWins = fighter['decisionWins'];
        // const decisionLosses = fighter['decisionLosses'];
        const fighterId = fighter['fighterID'];


        const fighterEle = document.createElement('li');
        const fighterElePara = document.createElement('p');


        fighterElePara.setAttribute('class', 'hyperlink');       
        fighterEle.setAttribute('id', fighterId);
        fighterEle.setAttribute('clicked', 0);

        
        fighterElePara.textContent = `${firstName} ${lastName} `;
        fighterEle.addEventListener('click', individualStatsClick);

        fighterEle.appendChild(fighterElePara);
        fightersList.appendChild(fighterEle);
        
    }
    search();
}

function search(){
    const searchStruct = document.querySelector('.search');
    const butSearch = searchStruct.querySelector('button');
    butSearch.addEventListener('click', searchClick);
    butSearch.setAttribute('clicked', 0);
   
}

async function individualStatsClick(e){
    const fighterEle = e.currentTarget;
    let clicks = fighterEle.getAttribute('clicked');
    console.log('intinal clicks', clicks);
    console.log('curr targ', fighterEle);
    const fighterId = fighterEle.id;

   
    if(clicks==='1'){
       
        return removeIndStats(fighterEle);
    }


    const fighead = document.createElement('h3');
    fighead.textContent = 'fighter record'
    fighterEle.appendChild(fighead);

    console.log(fighterEle, 'e');

    const url = `${api}/individualStatsFig?fighterId=${fighterId}`;
    const req = new Request(url)
    const resp = await fetch(req).catch((e)=>{
        console.log('error in getting individual stats');
        console.error(e);
    })
    const binImg = await resp.blob();
    console.log('resp from server for individual stats is ', binImg);
    console.log('req sent for individualStatsFig with fighterId:',fighterId);


    const individualStatsFig = document.createElement('img');
    individualStatsFig.setAttribute('src', URL.createObjectURL(binImg));

    fighterEle.appendChild(individualStatsFig);

    const urlData = `${api}/individualStatsData?fighterId=${fighterId}`;
    const reqData = new Request(urlData);
    const respData = await fetch(reqData).catch((e)=>{
        console.log('error in getting individual stats Data');
        console.error(e);
    });

    const data= await respData.json();
    console.log(respData, data, '===========> server')
    const aveTime = data.aveTime;
    const success = data.winPercentage;
    
    const tableTemp = document.querySelector('.tableListTemp');
    const tableTempContent = tableTemp.content;
    console.log(tableTempContent);
    const tableAveTime = tableTempContent.querySelector('.aveTime');
    console.log(tableAveTime);
    const tableWinP = tableTempContent.querySelector('.winPercentage');
    console.log(tableWinP);
    tableAveTime.textContent=aveTime;
    tableWinP.textContent=success;

    fighterEle.appendChild(tableTempContent.cloneNode(true));

    clicks=1;
    console.log(clicks, 'clicks');
    fighterEle.setAttribute('clicked', clicks);
}

function removeIndStats(fighterEle){
    console.log('more than 1 click');
    let clicks = 0;
    fighterEle.setAttribute('clicked', clicks);
    console.log(fighterEle.getAttribute('clicked'), '-clicks after setting to 0');
    const fig = fighterEle.querySelector('img');
    const tb = fighterEle.querySelector('table');
    const tbHead = fighterEle.querySelector('h3');


    console.log('parentnode of fig', fig.parentNode);
    fig.parentNode.removeChild(fig);
    tb.parentNode.removeChild(tb);
    tbHead.parentNode.removeChild(tbHead);
    return;

}

async function searchClick(e){
    console.log(e.target, 'but click');
    const searchEle = document.querySelector('.search');
    const but = searchEle.querySelector('.searchBut');
    let clicks = but.getAttribute('clicked');
    console.log('num clicks on search but', clicks);

    const inputEle = document.getElementById('search');
    let name = inputEle.value; 
    let inputValue = name.replace(' ', ',');
    console.log(inputValue, 'input vale');

    if (clicks==='0'){
        console.log('run hereeee')
        const clearBut = document.createElement('button');
        clearBut.textContent = 'clear all results';
        clearBut.addEventListener('click', clearButClick);
        searchEle.appendChild(clearBut);
        but.setAttribute('clicked', 1);
    }

    const req = new Request(`${api}/search?fighterName=${inputValue}`);
    
    const resp = await fetch(req).catch((e)=>{
        console.log('error in getting fighter', inputValue);
        console.error(e);
    });

    console.log(resp.status, 'response');
    if (resp.status===404){
        const errorText = document.createElement('p');
        errorText.textContent = `sorry! ${inputValue} cannot be found in the database`;
        searchEle.appendChild(errorText);
        inputEle.value = '';
        return;
    }

    const data = await resp.json()
    console.log('fighter found', data);

    const reqImage = new Request(`${api}/searchImage?fighterImage=${inputValue}`);
    let respImage = await fetch(reqImage).catch((e)=>{
        console.log('error in getting image for fighter', inputValue);
        console.error(e);
    })

    respImage = await respImage.blob();
    console.log('fighter image', respImage);

    const fighead = document.createElement('h3');
    fighead.textContent = `fighter record for ${name}`;
    searchEle.appendChild(fighead);
    
    const individualStatsFig = document.createElement('img');
    individualStatsFig.setAttribute('src', URL.createObjectURL(respImage));

    searchEle.appendChild(individualStatsFig);

    const aveTime = data.aveTime;
    const success = data.winPercentage;

    const tableTemp = document.querySelector('.tableListTemp');
    const tableTempContent = tableTemp.content;
    console.log(tableTempContent);
    const tableAveTime = tableTempContent.querySelector('.aveTime');
    console.log(tableAveTime);
    const tableWinP = tableTempContent.querySelector('.winPercentage');
    console.log(tableWinP);
    tableAveTime.textContent = aveTime;
    tableWinP.textContent = success;

    searchEle.appendChild(tableTempContent.cloneNode(true));

}

function clearButClick(e){
    const but = e.target;
    const searchEle = but.parentNode;
    console.log(searchEle,'search elel here');
    const h3 = searchEle.querySelectorAll('h3');
    const fig = searchEle.querySelectorAll('img');
    const table = searchEle.querySelectorAll('table');
    const para = searchEle.querySelectorAll('p');

    const searchBut = document.querySelector('.searchBut');
    searchBut.setAttribute('clicked', 0);

    console.log('h3', h3);

    for (ele of h3.values()){
        console.log(ele);
        searchEle.removeChild(ele);

    }
    for (ele of fig.values()) {
        console.log(ele);
        searchEle.removeChild(ele);
    }
    for (ele of table.values()) {
        console.log(ele);
        searchEle.removeChild(ele);
    }
    for (ele of para.values()) {
        console.log(ele);
        searchEle.removeChild(ele);
    }

    searchEle.removeChild(but);
    console.log(searchEle, '====================search ele');
}

populateSummary();

