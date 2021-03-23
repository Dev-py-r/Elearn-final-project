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

model = joblib.load(r'C:\Users\prasa\Desktop\Excelr\j_svm')

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
        if(Name==""):
            Name = 'Unknown'
        Gender = int(request.form['Gender'])
        if(Gender==""):
            Gender = 1
        Married = int(request.form['Married'])
        if (Married == ""):
            Married = 1
        Dependents = int(request.form['Dependents'])
        if (Dependents == ""):
            Dependents = 0
        Education = int(request.form['Education'])
        if (Education == ""):
            Education = 0
        Self_Employed = int(request.form['Self_Employed'])
        if (Self_Employed == ""):
            Self_Employed = 1
        Credit_History = int(request.form['Credit_History'])
        if (Credit_History == ""):
            Credit_History = 1
        Property_Area = int(request.form['Property_Area'])
        if (Property_Area == ""):
            Property_Area = 2
        Applicant_Income = int(request.form['Applicant_Income'])
        if (Applicant_Income == "" or Applicant_Income > 9357):
            Applicant_Income = 9357
        Coapplicant_Income = int(request.form['Coapplicant_Income'])
        if (Coapplicant_Income == "" or Coapplicant_Income > 3750):
            Coapplicant_Income = 3750
        Loan_Amount = int(request.form['Loan_Amount'])
        if (Loan_Amount == "" or Loan_Amount > 228):
            Loan_Amount = 228
        Loan_Amount_Term = int(request.form['Loan_Amount_Term'])
        if (Loan_Amount_Term == "" or Loan_Amount_Term > 360 or Loan_Amount_Term < 12):
            Loan_Amount_Term = 360

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
    app.run(debug=True, port=8000)


    #from main import db
    #db.create_all
    #exit()