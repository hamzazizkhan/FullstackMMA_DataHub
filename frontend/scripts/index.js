// fetch(path).then((response)=>{
//     if (!response.ok){
//         throw new Error('http not ok', response.status);
        
//     }
//     return response.json();
// }).then((prof_rec_data)=>{
//     console.log(prof_rec_data.length);
// })

async function collectProfRecData(){
    const path = 'scripts/prof_rec_data.json';
    const req = new Request(path);
    const response = await fetch(req).catch((error)=>{
        console.error(`error in response ${error}`);
    });
    const prof_rec_data = await response.json().catch((error) => {
        console.error(`error in json response ${error}`);
    });

    console.log('succesfully collected prof_rec_Data');
    populateSummary(prof_rec_data);
    populateFightersList(prof_rec_data);
}


function populateSummary(prof_rec_data){

    const summary = document.querySelector('.summary');
    const numFighters = document.createElement('li');
    numFighters.textContent = `collected data on ${prof_rec_data.length} fighters`;

    summary.appendChild(numFighters);

}

function populateFightersList(prof_rec_data){
    const fightersList = document.querySelector('.fightersList');

    let cnt =0;
    for (row of prof_rec_data){
        const firstName = row.firstName;
        const lastName = row.lastName;
        const text = `${firstName} ${lastName}`;

        const fighter = document.createElement('li');
        fighter.setAttribute('id', cnt);
        
        
        const dataButton = document.createElement('button');
        

        dataButton.textContent = 'show professional record';

        fighter.textContent = text;
        fightersList.appendChild(fighter);

        fighter.addEventListener('click', showData);
        
        
        fighter.appendChild(dataButton);
        cnt++;
    }

    function showData(e) {

        const fighterListElement = e.currentTarget;
        const fighterId = fighterListElement.id;
        const fighter = prof_rec_data[fighterId];

        const matches = fighter.matches;
        const wins = fighter.wins;
        const losses = fighter.losses;
        const knockoutWins = fighter.knockoutWins;
        const knockoutLosses = fighter.knockoutLosses;
        const submissionWins = fighter.submissionWins;
        const submissionLosses = fighter.submissionLosses;
        const decisionWins = fighter.decisionWins;
        const decisionLosses = fighter.decisionLosses;

        const data = document.createElement('p');

        data.textContent = `fights: ${matches}, wins:${wins} losses:${losses} knockoutWins: ${knockoutWins}
        knockoutLosses:${knockoutLosses} submissionWins:${submissionWins} submissionLosses:${submissionLosses} 
        decisionWins:${decisionWins} decisionLosses:${decisionLosses}`;

        fighterListElement.appendChild(data);

        const clearProfBtn = document.createElement('button');
        clearProfBtn.textContent = 'hide';
        data.addEventListener('click', clearRecord);
        data.appendChild(clearProfBtn);
    }

    function clearRecord(e){
        e.stopPropagation();
        e.currentTarget.remove();
    }
}





collectProfRecData();


