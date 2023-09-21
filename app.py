from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentdb.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    education = db.Column(db.String(255), nullable=False)
    preferences = db.Column(db.String(255))

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    qualifications = db.Column(db.String(255), nullable=False)
    experience = db.Column(db.String(255), nullable=False)
    expertise = db.Column(db.String(255), nullable=False)
    teaching_style = db.Column(db.String(255), nullable=False)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

def insert_data(data, user_type):
    try:
        if user_type == 'student':
            student = Student(**data)
            db.session.add(student)
        elif user_type == 'teacher':
            teacher = Teacher(**data)
            db.session.add(teacher)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error while inserting data. Please try again.', 'danger')
        return False
    flash('Registration successful', 'success')
    return True

@app.route('/student_registration', methods=['GET', 'POST'])
def student_registration():
    user_type = 'student'

    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'age': request.form['age'],
            'gender': request.form['gender'],
            'location': request.form['location'],
            'education': request.form['education'],
            'preferences': request.form['preferences']
        }

        age = data['age']
        if not age.isdigit() or int(age) <= 0:
            flash('Invalid age. Please enter a positive integer.', 'danger')
            return render_template('student_registration.html', user_type=user_type)

        student = Student(**data)
        # Set the user_type attribute for the student object
        student.user_type = 'student'
        db.session.add(student)
        db.session.commit()

        flash('Registration successful', 'success')
        return redirect(url_for('success', user_type=user_type))

    return render_template('student_registration.html', user_type=user_type)

@app.route('/teacher_registration', methods=['GET', 'POST'])
def teacher_registration():
    user_type = 'teacher'

    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'qualifications': request.form['qualifications'],
            'experience': request.form['experience'],
            'expertise': request.form['expertise'],
            'teaching_style': request.form['teaching_style']
        }

        teacher = Teacher(**data)
        # Set the user_type attribute for the teacher object
        teacher.user_type = 'teacher'
        db.session.add(teacher)
        db.session.commit()

        flash('Registration successful', 'success')
        return redirect(url_for('success', user_type=user_type))

    return render_template('teacher_registration.html', user_type=user_type)




@app.route('/success')
def success():
    user_type = request.args.get('user_type')
    return f'Registration successful for {user_type}!'

@app.route('/student_details')
def student_details():
    query = request.args.get('query', '')

    print(f"Search Query: {query}")  # Debugging output

    students = Student.query.filter(
        (Student.name.ilike(f"%{query}%")) |
        (Student.age.ilike(f"%{query}%")) |
        (Student.gender.ilike(f"%{query}%")) |
        (Student.location.ilike(f"%{query}%")) |
        (Student.education.ilike(f"%{query}%")) |
        (Student.preferences.ilike(f"%{query}%"))
    ).all()

    print(f"Matching Students: {students}")  # Debugging output

    return render_template('student_details.html', title='Student Details', students=students)



@app.route('/teacher_details')
def teacher_details():
    query = request.args.get('query', '')

    print(f"Search Query: {query}")  # Debugging output

    teachers = Teacher.query.filter(
        (Teacher.name.ilike(f"%{query}%")) |
        (Teacher.qualifications.ilike(f"%{query}%")) |
        (Teacher.expertise.ilike(f"%{query}%"))
    ).all()

    print(f"Matching Teachers: {teachers}")  # Debugging output

    return render_template('teacher_details.html', title='Teacher Details', teachers=teachers)


@app.route('/')
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.secret_key = '*9K),)Z^zPe7}DEh8(%mu`k3'
    app.run(debug=True)
