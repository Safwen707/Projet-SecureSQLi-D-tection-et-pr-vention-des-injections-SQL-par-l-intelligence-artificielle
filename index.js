const express = require('express');
const mysql = require('mysql');
const path = require('path');

const app = express();
const port = 3000;
const fetch = require('node-fetch');
app.use(express.json()); // pour lire les JSON

// Database connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'azerty',
  database: 'vlnerable_app',
  multipleStatements: true
});

db.connect(err => {
  if (err) throw err;
  console.log('Connected to MySQL Database!');
});

// Middlewares
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'views'))); // Serve static files (HTML/CSS)

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'home.html'));
});

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'login.html'));
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  console.log(username, password);

  // 🚨 VULNERABLE to SQL Injection
 // const query = `SELECT   user(), database(), version()`;
 const query = `SELECT username, password, email FROM users WHERE username = '${username}' AND password = '${password}'`;
  db.query(query, (err, results) => {
    if (err) throw err;
    console.log(query);
    if (results.length > 0) {
       //console.log(results)
       const users = results
      console.log(users);
      const user =users[0];

      // Redirect to profile with query parameters
      res.redirect(`/profile.html?username=${encodeURIComponent(user.username)}&email=${encodeURIComponent(user.email)}`);
    } else {
      res.send('Login failed. <a href="/login">Try again</a>');
    }
  });
});

app.get('/logout', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'logout.html'));
});

app.post('/predict', async (req, res) => {
  const { query } = req.body;

  if (!query || typeof query !== 'string') {
    return res.status(400).json({ error: 'Invalid input. Expected a SQL query string.' });
  }

  try {
    // Appeler le backend Flask (app.py) qui tourne sur http://localhost:5000
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });

    if (!response.ok) {
      const errorText = await response.text();
      return res.status(500).json({ error: 'Flask API error', detail: errorText });
    }

    const predictionData = await response.json();
    res.json(predictionData);

  } catch (error) {
    console.error('Error calling Flask API:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});
// Vérifiez que cette route est correctement définie dans votre index.js
// Elle doit se trouver avant app.listen() et après les autres routes

// Route pour servir api.js comme un module ES
app.get('/api.js', (req, res) => {
  res.setHeader('Content-Type', 'application/javascript');
  res.sendFile(path.join(__dirname, 'api.js'));
});

// Assurez-vous que vos middlewares static sont correctement configurés
app.use(express.static(path.join(__dirname))); // Pour accéder à tous les fichiers statiques dans le répertoire racine
app.use(express.static(path.join(__dirname, 'views'))); // Pour les fichiers dans le répertoire views

// Endpoint pour vérifier le statut du serveur (utile pour le débogage)
app.get('/status', (req, res) => {
  res.json({ status: 'Server is running', timestamp: new Date() });
});

// Test direct du proxy vers Flask
app.get('/test-flask', async (req, res) => {
  try {
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: "SELECT * FROM users" })
    });
    
    if (!response.ok) {
      return res.status(500).json({ error: 'Flask test failed', status: response.status });
    }
    
    const result = await response.json();
    res.json({ message: 'Flask test successful', result });
  } catch (error) {
    res.status(500).json({ error: 'Flask test error', message: error.message });
  }
});
// Start server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
