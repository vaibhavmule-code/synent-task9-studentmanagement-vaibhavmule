from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# DATABASE MODEL
class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    age = db.Column(db.String(10), nullable=False)

    course = db.Column(db.String(100), nullable=False)


# HOME PAGE
@app.route('/')
def index():

    students = Student.query.all()

    return render_template('index.html', students=students)


# ADD STUDENT
@app.route('/add', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        new_student = Student(
            name=name,
            age=age,
            course=course
        )

        db.session.add(new_student)

        db.session.commit()

        return redirect('/')

    return render_template('add_student.html')


# UPDATE STUDENT
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):

    student = Student.query.get(id)

    if request.method == 'POST':

        student.name = request.form['name']
        student.age = request.form['age']
        student.course = request.form['course']

        db.session.commit()

        return redirect('/')

    return render_template('update_student.html', student=student)


# DELETE STUDENT
@app.route('/delete/<int:id>')
def delete_student(id):

    student = Student.query.get(id)

    db.session.delete(student)

    db.session.commit()

    return redirect('/')


# MAIN
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)