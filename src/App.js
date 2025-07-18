// /workspaces/CopilotLab/src/App.js

import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [payments, setPayments] = useState([]);
  const [form, setForm] = useState({
    name: '',
    card_number: '',
    amount: '',
    payment_date: '',
    memo: ''
  });
  const [step, setStep] = useState('form'); // form, review, confirm
  const [transactionId, setTransactionId] = useState(null);
  const [fee, setFee] = useState(0);

  useEffect(() => {
    fetch('/api/payment')
      .then(res => res.json())
      .then(setPayments);
  }, []);

  useEffect(() => {
    // Calculate fee whenever amount changes
    const amt = parseFloat(form.amount);
    let f = 0;
    if (!isNaN(amt)) {
      if (amt <= 99) f = 10;
      else if (amt <= 999) f = 25;
      else if (amt <= 9999) f = 50;
      else if (amt <= 99999) f = 100;
      else f = 500;
    }
    setFee(f);
  }, [form.amount]);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = e => {
    e.preventDefault();
    setStep('review');
  };

  const handleEdit = () => {
    setStep('form');
  };

  const handleContinue = () => {
    // Submit to backend
    fetch('/api/payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, fee_amount: fee })
    })
      .then(res => res.json())
      .then(data => {
        setTransactionId(data.id);
        setStep('confirm');
        fetch('/api/payment')
          .then(res => res.json())
          .then(setPayments);
      });
  };

  return (
    <div className="container">
      {step === 'form' && (
        <div className="form-section">
          <h2>Payment Info</h2>
          <form onSubmit={handleSubmit} className="payment-form">
            <input name="name" placeholder="Name" value={form.name} onChange={handleChange} required />
            <input name="card_number" placeholder="Card Number" value={form.card_number} onChange={handleChange} required />
            <input name="amount" type="number" placeholder="Amount (₹)" value={form.amount} onChange={handleChange} required />
            <input name="payment_date" type="text" placeholder="Payment Date (DD/MM/YYYY)" value={form.payment_date} onChange={handleChange} required />
            <input name="memo" placeholder="Memo (optional, max 100 chars)" value={form.memo} onChange={handleChange} maxLength={100} />
            <div className="fee-info">Fee: <span>₹{fee}</span></div>
            <button type="submit">Submit</button>
          </form>
        </div>
      )}
      {step === 'review' && (
        <div className="review-section">
          <h2>Review Payment</h2>
          <ul className="review-list">
            <li><strong>Name:</strong> {form.name}</li>
            <li><strong>Card Number:</strong> {form.card_number}</li>
            <li><strong>Amount:</strong> ₹{form.amount}</li>
            <li><strong>Payment Date:</strong> {form.payment_date}</li>
            <li><strong>Fee:</strong> ₹{fee}</li>
            {form.memo && <li><strong>Memo:</strong> {form.memo}</li>}
          </ul>
          <button onClick={handleEdit}>✏️ Edit</button>
          <button onClick={handleContinue}>✅ Continue</button>
        </div>
      )}
      {step === 'confirm' && (
        <div className="confirm-section">
          <h2>Payment Confirmed</h2>
          <p>Your transaction ID: <span className="tx-id">{transactionId}</span></p>
          <button onClick={() => { setStep('form'); setForm({ name: '', card_number: '', amount: '', payment_date: '', memo: '' }); setTransactionId(null); }}>New Payment</button>
        </div>
      )}
      <h2>Payment List</h2>
      <ul className="payment-list">
        {payments.map(p => (
          <li key={p.id}>
            {p.name} - {p.card_number} - ₹{p.amount} - {p.payment_date} - Fee: ₹{p.fee_amount} {p.memo && `- Memo: ${p.memo}`}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;