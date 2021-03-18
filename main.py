from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Gender = db.Column(db.String(500), nullable=False)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True,port=8000)