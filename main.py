from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.Name}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        Name = request.form['Name']
        # Gender = request.form['Gender']
        # Married = request.form['Married']
        # Dependents = request.form['Dependents']
        # Education = request.form['Education']
        # Self_Employed = request.form['Self_Employed']
        # Credit_History = request.form['Credit_History']
        # Property_Area = request.form['Property_Area']
        # Total_Income = request.form['Total_Income']
        # EMI = request.form['EMI']
        # Balance_Income = request.form['Balance_Income']
        todo = Todo(Name=Name)
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