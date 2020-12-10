//NodeJS application for BLOCKCHAIN FDS MINI PROJECT

//Filestream module imported
const fs = require('fs')

//Datafile location
const datafile = ('./document.txt')

//Data read from document.txt
const dataBuffer = fs.readFileSync('document.txt')

//Data buffer data converted to string
const dataJSON = dataBuffer.toString()

//Converted to JSON 
const data = JSON.parse(dataJSON)

//Converted to JSON formatted string
const stringdata = JSON.stringify(data)

//DATA APPENDED TO DATA.JSON FILE
fs.appendFileSync('data.json', stringdata)
