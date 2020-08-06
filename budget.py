from flask import Flask, render_template, request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import MySQLdb

app=Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/budget'
db = SQLAlchemy(app)

class Account(db.Model):
    serial = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(80), primary_key=True)
    budget = db.Column(db.Integer, primary_key=True)



@app.route('/')
def front():
    return render_template('front.html')

@app.route('/form.html')
def form():
    return render_template('form.html')

'''@app.route('/login.html')
def login():
    return render_template('login.html')'''

@app.route('/login.html', methods=['POST', 'GET'])
def sign():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        budget=request.form['bud']

        entry=Account(name=name, email=email, budget=budget)
        db.session.add(entry)
        db.session.commit()

        return render_template('login.html')

    else:
        return render_template('login.html')



@app.route('/account.html', methods=['POST', 'GET'])
def account():
    if 'user' in session:
        var=Account.query.filter_by(name=session['user']).first()
        return render_template('account.html', account=var)
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
    accounts=Account.query.filter_by(name=name).first()
    acc=Account.query.filter_by(name=name).all()
    if len(acc):
        if(accounts.name==name and accounts.email==email):
            session['user']=name
            return render_template('account.html', account=accounts)
        else:
            return 'galti se mistake'
    else:
        return 'galti se mistake'

@app.route('/account.html', methods=['POST', 'GET'])
def updated():
    if 'user' in session:
        if request.method=='POST':
            name=request.form.get('name')
            amount=request.form.get('amount')
        reciever=Account.query.filter_by(name=name).first()
        rec=Account.query.filter_by(name=name).all()
        if len(rec):
            if(reciever.name==name):
                var=Account.query.filter_by(name=session['user']).first()
                reciever.budget=reciever.budget+int(amount)
                var.budget=var.budget-int(amount)
                db.session.commit()
                return redirect('/account')




if __name__=="__main__":
    app.run(debug=True)

#action="{{url_for('budget.html')}}"
#redirect(url_for('/account.html'))