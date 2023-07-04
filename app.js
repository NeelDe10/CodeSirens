// Example app.js file

const express = require('express');
const app = express();

// Middleware
app.use(express.json());

// Routes
const api=require('./routes/api');

app.use("/api/v1",api);

module.exports=app
