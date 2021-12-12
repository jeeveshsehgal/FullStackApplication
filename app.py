from flask import Flask,render_template, request
from datetime import date
import sqlite3 as sql

app = Flask(__name__)

# Today's date
today = date.today()

# index page or search page
@app.route("/")
def index():
    return render_template('index.html')

# add page
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # fetching data from form
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        address = request.form.get("address")
        date = request.form.get("date")
        cell = request.form.get("cell")
        work = request.form.get("work")
        home = request.form.get("home")

        # set connection
        with sql.connect("database.db") as connection:
            # Insert new employee details
            curr =  connection.cursor()
            curr.execute("INSERT INTO Employee (Firstname,Lastname,Address,Joining_date) VALUES (?,?,?,?)",(firstname,lastname,address,date))
            connection.commit()
        
            curr =  connection.cursor()
            query = f"SELECT ID FROM Employee WHERE Firstname = '{firstname}' AND Lastname = '{lastname}' AND Address = '{address}'"
            curr.execute(query)
            id = curr.fetchone()
            id = id[0]

            # Insert new employee contact details
            curr =  connection.cursor()
            curr.execute("INSERT INTO ContactDetail (EmployeeID,Cell,Work,Home) VALUES (?,?,?,?)",(id,cell,work,home))  
            connection.commit()

        connection.close()
    return render_template('add.html', today=today)

# display page
@app.route("/display", methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        # fetching data from form
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")

        # set connection
        with sql.connect("database.db") as connection:

            # Fetch the details of searched employee
            curr =  connection.cursor()
            query = f"SELECT e.ID, e.Firstname, e.Lastname, e.Address, e.Joining_date, c.Cell, c.Work, c.Home FROM Employee AS e INNER JOIN ContactDetail AS c WHERE e.ID = c.EmployeeID AND e.Firstname = '{firstname}' AND e.Lastname = '{lastname}'"
            data = curr.execute(query)
            data = curr.fetchone()
        connection.close()
    return render_template('display.html', data = data)
    
if __name__ == "__main__":
    app.run(debug=True)