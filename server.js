// run mongosh in terminal to start database connection
require('dotenv').config();
const express = require('express');
const app = express();
const port = process.env.PORT;  //Sets the server to listen on the port defined by process.env.PORT.
console.log(process.env.MONGODB_URI);
const mongoose = require('mongoose');
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost/test', {useNewUrlParser: true, useUnifiedTopology: true});
// Connects to your MongoDB database using mongoose.connect.  with the database URL being retrieved from process.env.MONGODB_URI
// The MongoDB URI is retrieved from the environment variable MONGODB_URI. 
// The options {useNewUrlParser: true, useUnifiedTopology: true} are provided to avoid deprecation warnings.

// handle the connection events for mongoose to know whether the connection is successful or if there is any error while connecting.
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  console.log('Connected');
});

// sending a response to the browser at http://localhost:3000
app.get('/', (req, res) => {        // Defines a route handler for GET requests to the root URL (/) that sends 'Hello World' as the response.
    res.send('Hello World')
});

// upon execution this will print to the console
app.listen(port, () =>{
    console.log(`listening at http://localhost:${port}`)

})

// PORT 80 or 8080 is the default PORT