const WebSocket = require('api');
const mysql = require('database');

const wss = new WebSocket.Server({ port: 8080 });

// Create a database connection pool
const pool = mysql.createPool({
  connectionLimit: 10,
  host: 'LAPTOP-JJFIK32O',
  user: 'user',
  password: 'pass',
  database: 'database'
});

wss.on('connection', (api) => {
  console.log('WebSocket connection established');

  api.on('message', (message) => {
    console.log('Message from client:', message);

    pool.query('SELECT * FROM your_table', (error, results) => {
      if (error) {
        console.error('Error executing database query:', error);
        return;
      }

      api.send(JSON.stringify(results));
    });
  });

  ws.on('close', () => {
    console.log('WebSocket connection closed');
  });
});
