const express = require('express');
const router = express.Router();
const Payee = require('../models/payee');

// Add a new payee
router.post('/add', (req, res) => {
  const { name, account } = req.body;
  Payee.addPayee(name, account, function (err) {
    if (err) return res.status(500).send('Error adding payee');
    res.send('Payee added');
  });
});

// Get payee by account
router.get('/account/:account', (req, res) => {
  Payee.getPayeeByAccount(req.params.account, function (err, row) {
    if (err) return res.status(500).send('Error fetching payee');
    res.json(row);
  });
});

// Get payee by name
router.get('/name/:name', (req, res) => {
  Payee.getPayeeByName(req.params.name, function (err, row) {
    if (err) return res.status(500).send('Error fetching payee');
    res.json(row);
  });
});

// ...existing code...

module.exports = router;