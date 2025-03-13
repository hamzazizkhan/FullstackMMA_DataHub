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


async function populateSummary(){
    const summary = document.querySelector('.summary');
    const numFighters = document.createElement('li');

    const request = new Request('http://localhost:50000?dataLength');
    const response = await fetch(request).catch((e)=>{
        console.log('error in fetching data length');
        console.error(e);
    });

    const lengthOfData = await response.text()
    numFighters.textContent = `collected data on ${lengthOfData} fighters`;

    summary.appendChild(numFighters);
    console.log('the response from my server for data length should be 102', lengthOfData);

    populateFightersList();
}


async function populateFightersList(){
    const fightersList = document.querySelector('.fightersList');
    
    const request = new Request('http://localhost:50000?fighterID=1');
    const response = await fetch(request).catch((e)=>{
        console.log('error in getting fighter');
        console.error(e);
    })

    const allFighters = await response.json();
    console.log('response for fighterID',allFighters);

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

        const fighterListElement = document.createElement('li');
        fighterListElement.textContent = `fighter: ${firstName} ${lastName} matches: ${matches} wins: ${wins} losses: ${losses} knockoutWins: ${knockoutWins} knockoutLosses: ${knockoutLosses} submissionWins: ${submissionWins} submissionLosses: ${submissionLosses} decisionWins: ${decisionWins} decisionLosses: ${decisionLosses}`;
        fightersList.appendChild(fighterListElement);
    }


}

populateSummary();






