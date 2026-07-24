from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'reactions.db'

def init_db():
    """Create the database and table if they don't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS reactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                color TEXT NOT NULL,
                time_ms INTEGER NOT NULL
            )
        ''')
        conn.commit()

# Initialize the database on startup
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    """API endpoint to receive and save reaction times."""
    data = request.json
    color = data.get('color')
    time_ms = data.get('time_ms')
    
    if color and time_ms:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO reactions (color, time_ms) VALUES (?, ?)', (color, time_ms))
            conn.commit()
        return jsonify({"status": "success"}), 200
    
    return jsonify({"status": "error"}), 400

@app.route('/results')
def results():
    """Display the average reaction times ordered fastest to slowest."""
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT color, CAST(AVG(time_ms) AS INTEGER) as avg_time
            FROM reactions
            GROUP BY color
            ORDER BY avg_time ASC
        ''')
        results = c.fetchall()
    return render_template('results.html', results=results)

if __name__ == '__main__':
    # host='0.0.0.0' allows you to access it from your mobile device on the same Wi-Fi
    app.run(debug=True, host='0.0.0.0', port=8080)