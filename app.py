from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)


@app.route('/')
def index():
    ex = list()
    return render_template('Home2.html', ex = ex)


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    print('called here.')
    if request.method == 'GET':
        return render_template('add_student.html')
    else:
        # name, sjsuid, hw, exam, year, email
        student = (request.form['name'],
                   request.form['sjsuid'],
                   request.form['hw'],
                   request.form['exam'],
                   request.form['year'],
                   request.form['email'],
                   )

        print('Student details', student)
        insert_student(student)
        return render_template('add_success.html')

def insert_student(student):
    '''
    SCHEMA
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sjsuid TEXT NOT NULL,
        hw TEXT NOT NULL,
        exam TEXT NOT NULL,
        year TEXT NOT NULL,
        email TEXT NOT NULL
    );
    '''
    con = sqlite3.connect("sjsu_cs122.db")
    cur = con.cursor()
    sql = 'INSERT INTO students (name, sjsuid, hw, exam, year, email) VALUES (?,?,?,?,?,?)'
    cur.execute(sql, student)
    con.commit()
    #res = cur.execute("select * from students where name={}".format(student['name']))
    #print("Result from the database:", res)
    con.close()

@app.route('/get_student', methods=['GET'])
def get_student():
    id = request.args.get('sjsuid')
    print('sjsuid is:', id)
    con = sqlite3.connect("sjsu_cs122.db")
    cur = con.cursor()
    q = "select * from students where sjsuid=\'{}\'".format(id)
    #print('query:', q)
    res = cur.execute(q)
    rows = res.fetchall()
    con.close()
    #print("Result from the database:", rows)
    return render_template("get_student.html", student = rows)

def list():
    con = sqlite3.connect("sjsu_cs122.db")
    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return (rows)

if __name__ == '__main__':
   app.run(debug = True)