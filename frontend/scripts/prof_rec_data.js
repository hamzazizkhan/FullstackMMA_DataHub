const sqlite3 = require('sqlite3');
const fs = require('fs');

const db = new sqlite3.Database('/Users/hamzakhan/Desktop/web_crawler/fighters.sqlite');

db.all('SELECT * FROM profesional_record_data', (err,pro_rec_data)=>{
    if(err){
        console.log('err');
        return;
    }
    const num_fighters = pro_rec_data.length;
    console.log(pro_rec_data)
    fs.writeFile('prof_rec_data.json',JSON.stringify(pro_rec_data), (err)=>{
        if(err){
            console.error(err);
            throw err;
        }
    })

});

/**
 * number of fighters collected
 * display their names
 * be able to click them to see thir MMA record
 */


