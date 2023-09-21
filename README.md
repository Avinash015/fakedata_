# fakedata_
project directory structure

my_project/
    app.py                 # Your Flask application
    static/
        style.css           # Common CSS for both student and teacher registration
    templates/
        main.html           # Common layout template
        student_registration.html  # Student registration template
        teacher_registration.html  # Teacher registration template
        student_details.html      # Student details template
        teacher_details.html      # Teacher details template
    venv/                   # Virtual environment (optional, but recommended)
    student.db              # SQLite database for student data
    teacher.db              # SQLite database for teacher data



install Flask==2.1.0
