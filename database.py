import mysql.connector

class Database:
    def __init__(self, host='localhost', user='root', password='', database='student_db'):
        self.conn = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def setup(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT,
                subject VARCHAR(100),
                marks INT,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            );
        """)
        self.conn.commit()

    def add_student(self, name):
        self.cursor.execute("INSERT INTO students (name) VALUES (%s)", (name,))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_result(self, student_id, subject, marks):
        self.cursor.execute(
            "INSERT INTO results (student_id, subject, marks) VALUES (%s, %s, %s)",
            (student_id, subject, marks)
        )
        self.conn.commit()

    def update_student(self, student_id, name):
        self.cursor.execute("UPDATE students SET name=%s WHERE id=%s", (name, student_id))
        self.conn.commit()

    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
        self.conn.commit()

    def get_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def get_results(self, student_id):
        self.cursor.execute("SELECT * FROM results WHERE student_id=%s", (student_id,))
        return self.cursor.fetchall()
