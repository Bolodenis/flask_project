from flask import Flask, render_template, url_for, redirect, request, flash
import sqlite3
from model import create_table

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Secret key for flash messages
create_table()

@app.route("/")
def home():
    print("Home page loaded")
    return render_template("layout.html")

@app.route('/projects')
def projects():
    print("Projects page loaded")
    return render_template('projects.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        surname = request.form['surname']
        email = request.form['email']
        street = request.form['street']
        apartment = request.form['apartment']
        city = request.form['city']
        
        conn = sqlite3.connect("mydata_db.db")
        cur = conn.cursor()
        cur.execute('INSERT INTO mydata (surname, email, street, apartment, city) VALUES (?, ?, ?, ?, ?)', 
                    (surname, email, street, apartment, city))
        conn.commit()
        conn.close()
        
        flash('Your details have been submitted successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('contact.html')

@app.route('/view')
def view():
    conn = sqlite3.connect("mydata_db.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM mydata")
    users = cur.fetchall()
    conn.close()
    return render_template('view.html', users=users)

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    conn = sqlite3.connect("mydata_db.db")
    cur = conn.cursor()

    # If the method is GET, show the current user details
    if request.method == 'GET':
        cur.execute("SELECT * FROM mydata WHERE id = ?", (user_id,))
        user = cur.fetchone()
        conn.close()
        return render_template('update.html', user=user)

    # If the method is POST, update the record with the new data
    if request.method == 'POST':
        surname = request.form['surname']
        email = request.form['email']
        street = request.form['street']
        apartment = request.form['apartment']
        city = request.form['city']
        
        cur.execute('UPDATE mydata SET surname = ?, email = ?, street = ?, apartment = ?, city = ? WHERE id = ?',
                    (surname, email, street, apartment, city, user_id))
        conn.commit()
        conn.close()
        
        flash('Your details have been updated successfully!', 'success')
        return redirect(url_for('view'))

    

@app.route('/delete/<int:user_id>')
def delete(user_id):
    conn = sqlite3.connect("mydata_db.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM mydata WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    flash('Record deleted successfully!', 'info')
    return redirect(url_for('view'))


if __name__ == "__main__":
    app.run(debug=True, port=5000)

