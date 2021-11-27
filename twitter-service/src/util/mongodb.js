var mongoose = require('mongoose');

var dbURL = 'mongodb://twitter-db:27017/moai'
exports.dbsetting = function(){
    mongoose.connect(dbURL);
    var db = mongoose.connection;
    db.on('error', function(){
    console.log('Connection Failed!');
    });

    db.once('open', function() {
        console.log('Connected!');
    });
    return db;
}

exports.data = new mongoose.Schema({
    'content' : 'string',
    'sns' : 'string',
    'date':'string',
    'link' : 'string',
    'keyword' : 'string',
    'service': 'string'
});

