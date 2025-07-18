// /workspaces/CopilotLab/models/payee.js

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./payees.db');

db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS payees (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      account TEXT NOT NULL UNIQUE
    )
  `);
});

module.exports = {
  addPayee: (name, account, cb) => {
    db.run(
      'INSERT INTO payees (name, account) VALUES (?, ?)',
      [name, account],
      cb
    );
  },
  getPayeeByAccount: (account, cb) => {
    db.get('SELECT * FROM payees WHERE account = ?', [account], cb);
  },
  getPayeeByName: (name, cb) => {
    db.get('SELECT * FROM payees WHERE name = ?', [name], cb);
  },
  // ...existing code...
};