from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Create a SQLite database and table for the flight log
conn = sqlite3.connect('flight_log.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aircraft TEXT NOT NULL,
        date TEXT NOT NULL,
        departure TEXT NOT NULL,
        arrival TEXT NOT NULL,
        time INTEGER NOT NULL,
        comments TEXT
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    longest_flight_stat = 'No Flights! Add Some'
    total_flight_hours = 0
    stat = ''
    conn = sqlite3.connect('flight_log.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flights')
    flights = cursor.fetchall()
    for flight in flights:
        try:
            if isinstance(flight[5], float):
                total_flight_hours += float(flight[5])
            elif isinstance(flight[5], int):
                total_flight_hours += int(flight[5])
        except ValueError:
            total_flight_hours = 0
        flight_times = [float(flight[5]) for flight in flights]
        if flight_times:
            longest_flight_hours = max(flight_times)

            cursor.execute('SELECT * FROM flights WHERE time = ?', (longest_flight_hours,))
            longest_flight_stat = cursor.fetchall()



    if total_flight_hours >= 1000:
        stat = 'Flight Enthusiast'
    elif total_flight_hours >= 500:
        stat = 'Master Aviator'
    elif total_flight_hours >= 100:
        stat = 'Dedicated Pilot'
    elif total_flight_hours >= 50:
        stat = 'Frequent Flyer'
    elif total_flight_hours >= 10:
        stat = 'Novice Flyer'
    elif total_flight_hours >= 5:
        stat = 'Airborne Adventurer'
    elif total_flight_hours >= 3:
        stat = 'Quick Learner'
    elif total_flight_hours >= 1:
        stat = 'Takeoff Rookie'
    else:
        stat = 'No Achievements Yet'

    conn.close()

    return render_template(
            'index.html', 
            flights=flights, 
            total_flight_hours=total_flight_hours, 
            stat=stat, 
            longest_flight_stat=longest_flight_stat
        )


@app.route('/add_flight', methods=['POST'])
def add_flight():
    if request.method == 'POST':
        aircraft = request.form['aircraft']
        date = request.form['date']
        departure = request.form['departure']
        arrival = request.form['arrival']
        time = request.form['time']
        comments = request.form['comments']
        
        conn = sqlite3.connect('flight_log.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO flights (date, departure, arrival, time, comments, aircraft)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date, departure, arrival, time, comments, aircraft))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
@app.route('/delete_flight', methods=['POST'])
def send_flight_data():
    flight_id = request.form.get('flight_id')

    conn = sqlite3.connect('flight_log.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM flights WHERE id = ?', (flight_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
