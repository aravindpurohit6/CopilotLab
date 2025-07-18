// /workspaces/CopilotLab/app.js

const express = require('express');
const app = express();
app.use(express.json());

const payeeRoutes = require('./routes/payee');
app.use('/payee', payeeRoutes);

// ...existing code...

app.listen(3000, () => {
  console.log('Server running on port 3000');
});