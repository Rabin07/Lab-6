from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Student
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify(student.to_dict())

@app.route('/api/students', methods=['POST'])
@app.route('/api/students/<int:student_id>', methods=['POST'])
def handle_student(student_id=None):
    data = request.form
    try:
        if student_id:
            # Update existing student
            student = Student.query.get_or_404(student_id)
            student.first_name = data['first_name']
            student.last_name = data['last_name']
            student.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            student.amount_due = float(data['amount_due'])
        else:
            # Create new student
            student = Student(
                first_name=data['first_name'],
                last_name=data['last_name'],
                dob=datetime.strptime(data['dob'], '%Y-%m-%d').date(),
                amount_due=float(data['amount_due'])
            )
            db.session.add(student)
        
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)