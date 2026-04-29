from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        item_name = request.form['item']
        item_amount = request.form['amount']
        item_category = request.form['category']
        
        new_expense = Expense(item=item_name, amount=float(item_amount), category=item_category)
        db.session.add(new_expense)
        db.session.commit()
        return redirect('/')

    expenses = Expense.query.order_by(Expense.date_added.desc()).all()
    total = sum(exp.amount for exp in expenses)
    return render_template('index.html', expenses=expenses, total=total)

if __name__ == "__main__":
    app.run(debug=True)
