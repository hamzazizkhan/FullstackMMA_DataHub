// fetch(path).then((response)=>{
//     if (!response.ok){
//         throw new Error('http not ok', response.status);
        
//     }
//     return response.json();
// }).then((prof_rec_data)=>{
//     console.log(prof_rec_data.length);
// })

// async function collectProfRecData(){
//     const path = 'scripts/prof_rec_data.json';
//     const req = new Request(path);
//     const response = await fetch(req).catch((error)=>{
//         console.error(`error in response ${error}`);
//     });
//     const prof_rec_data = await response.json().catch((error) => {
//         console.error(`error in json response ${error}`);
//     });

//     console.log('succesfully collected prof_rec_Data');
//     populateSummary(prof_rec_data);
//     populateFightersList(prof_rec_data);
// }
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
    // populateFightersList();
}


async function populateFightersList(){
    // const fightersList = document.querySelector('.fightersList');
    // const tableList = document.querySelector('.tableList');
    // const fighterName = tableList.querySelector('.fighterName');
    // const fighterMatches = tableList.querySelector('.fighterMatches');
    // const knockoutWinsTable = tableList.querySelector('.knockoutWins');
    // const knockoutLossesTable = tableList.querySelector('.knockoutLosses');
    // const submissionWinsTable = tableList.querySelector('.submissionWins');
    // const submissionLossesTable = tableList.querySelector('.submissionLosses');
    const tableListCont = document.querySelector('.tableListCont');
    const tableListTemp = document.querySelector('.tableListTemp');


    const request = new Request('http://localhost:50000?fiftyFighters');
    const response = await fetch(request).catch((e)=>{
        console.log('error in getting fighter');
        console.error(e);
    })

    const allFighters = await response.json().catch((e)=>{
        console.log('error in parsing json from server for fighters')
        console.error(e);
    });
    console.log('response for fighterID',allFighters);

    for (fighter of allFighters){
        const tableList = tableListTemp.content.cloneNode(true);
        //console.log(tableList);
        

        const fighterName = tableList.querySelector('.fighterName');
        //console.log(fighterName);
        const fighterMatches = tableList.querySelector('.fighterMatches');
        const knockoutWinsTable = tableList.querySelector('.knockoutWins');
        const knockoutLossesTable = tableList.querySelector('.knockoutLosses');
        const submissionWinsTable = tableList.querySelector('.submissionWins');
        const submissionLossesTable = tableList.querySelector('.submissionLosses');

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

        fighterName.textContent = `${firstName},  ${lastName}`;
        fighterMatches.textContent = matches;
        knockoutWinsTable.textContent = knockoutWins;
        knockoutLossesTable.textContent = knockoutLosses;
        submissionWinsTable.textContent =submissionWins;
        submissionLossesTable.textContent =submissionLosses;
        console.log(fighterName);

        // tableList.appendChild(fighterName);
        // tableList.appendChild(fighterMatches);
        // tableList.appendChild(knockoutWinsTable);
        // tableList.appendChild(knockoutLossesTable);
        // tableList.appendChild(submissionWinsTable);
        // tableList.appendChild(submissionLossesTable);


        tableListCont.appendChild(tableList);


        // const fighterListElement = document.createElement('li');
        // fighterListElement.textContent = `fighter: ${firstName} ${lastName} matches: ${matches} wins: ${wins} losses: ${losses} knockoutWins: ${knockoutWins} knockoutLosses: ${knockoutLosses} submissionWins: ${submissionWins} submissionLosses: ${submissionLosses} decisionWins: ${decisionWins} decisionLosses: ${decisionLosses}`;
        // fightersList.appendChild(fighterListElement);
    }


}

populateSummary();






