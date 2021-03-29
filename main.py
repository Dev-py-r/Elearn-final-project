from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import joblib
import numpy as np



app = Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///back.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

model = joblib.load(r'.\j_clf')

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Predict = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.Name}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method =='POST':
        Name = request.form['Name']
        Gender = int(request.form['Gender'])
        Married = int(request.form['Married'])
        Dependents = int(request.form['Dependents'])
        Education = int(request.form['Education'])
        Self_Employed = int(request.form['Self_Employed'])
        Credit_History = int(request.form['Credit_History'])
        Property_Area = int(request.form['Property_Area'])
        Applicant_Income = int(request.form['Applicant_Income'])
        if (Applicant_Income > 9357):
            Applicant_Income = 9357
        Coapplicant_Income = int(request.form['Coapplicant_Income'])
        if (Coapplicant_Income > 3750):
            Coapplicant_Income = 3750
        Loan_Amount = int(request.form['Loan_Amount'])
        if (Loan_Amount > 228):
            Loan_Amount = 228
        Loan_Amount_Term = int(request.form['Loan_Amount_Term'])
        if (Loan_Amount_Term > 360 or Loan_Amount_Term < 12):
            Loan_Amount_Term = int(360)

        scaler = StandardScaler()
        trans = scaler.fit_transform(np.array([[Gender, Married, Dependents, Education, Self_Employed, Credit_History, Property_Area, Applicant_Income,Coapplicant_Income, Loan_Amount, Loan_Amount_Term]]))
        predict  = model.predict(trans)
        if (predict == 'Y'):
            predict="Yes"
        else:
            predict="No"

        todo = Todo(Name=Name,Predict=predict)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=False, port=8000)


    #from main import db
    #db.create_all
    #exit()

    # pip install gunicorn
    #Heroku cli
    # pip freeze > requirement.txt

    # Probfile

    # web: gunicorn app: app
