
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

async function populateSummary(){
    const summary = document.querySelector('.summary');
    const numFightsEle = document.createElement('li');
    const numFightersEle = document.createElement('li');

    const request = new Request('http://localhost:50000?summaryStats');
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
    numFights = summaryStats.slice(0, summaryStats.indexOf('/'));
    numFighters = summaryStats.slice(summaryStats.indexOf('/') + 1,);

    numFightsEle.textContent=`colected data on ${numFights} fights`;
    numFightersEle.textContent=`for ${numFighters} individual fighters`;
    
    summary.appendChild(numFightsEle);
    summary.appendChild(numFightersEle);


    fig = document.createElement('figure');
    figcap = document.createElement('figcaption');
    figcap.innerText='an interesting finding';
    
    console.log('the response from my server for summaryStats: ', numFights, numFighters);
    
    const requestImage = new Request('http://localhost:50000?summaryStatsImage');
    const respImage = await fetch(requestImage).catch((e)=>{
        console.log('error in fetching respImage');
        console.error(e);
    });
    const summaryStatsImage=document.createElement('img');
    const im = await respImage.blob();
    summaryStatsImage.setAttribute('src', URL.createObjectURL(im));

    fig.appendChild(summaryStatsImage);
    fig.appendChild(figcap);

    summary.appendChild(fig)
    populateFightersList();
}


async function populateFightersList(){
    const fightersList = document.querySelector('.fightersList');

    const request = new Request('http://localhost:50000?fiftyFighters');
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
        const firstName = fighter[0];
        const lastName = fighter[1];
        const matches = fighter[2];
        const wins = fighter[3];
        const losses = fighter[4];
        const knockoutWins = fighter[5];
        const knockoutLosses = fighter[6];
        const submissionWins = fighter[7];
        const submissionLosses = fighter[8];
        const decisionWins = fighter[9];
        const decisionLosses = fighter[10];
        const fighterId = fighter[11];


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

    console.log(fighterEle, 'e');

    const url = `http://localhost:50000?individualStatsFig=${fighterId}`;
    const req = new Request(url)
    const resp = await fetch(req).catch((e)=>{
        console.log('error in getting individual stats');
        console.error(e);
    })
    const binImg = await resp.blob();
    console.log('resp from server for individual stats is ', binImg);


    const individualStatsFig = document.createElement('img');
    individualStatsFig.setAttribute('src', URL.createObjectURL(binImg));

    fighterEle.appendChild(individualStatsFig);

    const urlData = `http://localhost:50000?individualStatsData=${fighterId}`;
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

    console.log('parentnode of fig', fig.parentNode);
    fig.parentNode.removeChild(fig);
    tb.parentNode.removeChild(tb);
    return;

}

populateSummary();

