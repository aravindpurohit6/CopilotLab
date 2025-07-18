# /workspaces/CopilotLab/app.py

from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
db = SQLAlchemy(app)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.String(10))
    fee_amount = db.Column(db.Float)
    memo = db.Column(db.String(100))

def calculate_fee(amount):
    if amount <= 99:
        return 10
    elif amount <= 999:
        return 25
    elif amount <= 9999:
        return 50
    elif amount <= 99999:
        return 100
    else:
        return 500

@app.route('/api/payment', methods=['POST'])
def create_payment():
    data = request.json
    fee = calculate_fee(data['amount'])
    payment = Payment(
        name=data['name'],
        card_number=data['card_number'],
        amount=data['amount'],
        payment_date=data.get('payment_date'),
        fee_amount=fee,
        memo=data.get('memo')
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({'message': 'Payment created', 'id': payment.id}), 201

@app.route('/api/payment', methods=['GET'])
def list_payments():
    payments = Payment.query.all()
    result = [
        {
            'id': p.id,
            'name': p.name,
            'card_number': p.card_number,
            'amount': p.amount,
            'payment_date': p.payment_date,
            'fee_amount': p.fee_amount,
            'memo': p.memo
        } for p in payments
    ]
    return jsonify(result)

@app.route('/api/<int:payment_id>/payment', methods=['GET'])
def payment_detail(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        abort(404)
    return jsonify({
        'id': payment.id,
        'name': payment.name,
        'card_number': payment.card_number,
        'amount': payment.amount,
        'payment_date': payment.payment_date,
        'fee_amount': payment.fee_amount,
        'memo': payment.memo
    })

@app.route('/api/payment', methods=['PUT'])
def update_payment():
    data = request.json
    payment = Payment.query.get(data['id'])
    if not payment:
        abort(404)
    payment.name = data.get('name', payment.name)
    payment.card_number = data.get('card_number', payment.card_number)
    payment.amount = data.get('amount', payment.amount)
    payment.payment_date = data.get('payment_date', payment.payment_date)
    payment.fee_amount = calculate_fee(payment.amount)
    payment.memo = data.get('memo', payment.memo)
    db.session.commit()
    return jsonify({'message': 'Payment updated'})

@app.route('/api/payment', methods=['DELETE'])
def delete_payment():
    data = request.json
    payment = Payment.query.get(data['id'])
    if not payment:
        abort(404)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)