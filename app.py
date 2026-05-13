from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('database.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_ride():

    if request.method == 'POST':

        source = request.form['source']
        destination = request.form['destination']
        seats = request.form['seats']
        time = request.form['time']

        conn = connect_db()

        conn.execute(
            "INSERT INTO rides (source, destination, seats, time) VALUES (?, ?, ?, ?)",
            (source, destination, seats, time)
        )

        conn.commit()
        conn.close()

        return redirect('/rides')

    return render_template('add_ride.html')

@app.route('/rides')
def view_rides():
    conn = connect_db()
    rides = conn.execute("SELECT * FROM rides").fetchall()
    conn.close()

    return render_template('view_rides.html', rides=rides)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']

        conn = connect_db()
        rides = conn.execute(
            "SELECT * FROM rides WHERE source=? AND destination=?",
            (source, destination)
        ).fetchall()
        conn.close()

        return render_template('search.html', rides=rides)

    return render_template('search.html', rides=None)
@app.route('/book/<int:ride_id>', methods=['POST'])
def book_ride(ride_id):

    seats_needed = int(request.form['book_seats'])

    conn = connect_db()

    ride = conn.execute(
        "SELECT seats FROM rides WHERE id=?",
        (ride_id,)
    ).fetchone()

    available_seats = ride[0]

    if available_seats >= seats_needed:

        new_seats = available_seats - seats_needed

        conn.execute(
            "UPDATE rides SET seats=? WHERE id=?",
            (new_seats, ride_id)
        )

        conn.commit()

    conn.close()

    return redirect('/search')
app.run(debug=True)