from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(host = "localhost", dbname = "postgres", user = "postgres", password ="admin123", port = 5432)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )
""")

conn.commit()

cursor.execute('''
    ALTER TABLE contacts
    DROP COLUMN IF EXISTS id;
''')
conn.commit()

cursor.execute('''
    ALTER TABLE contacts
    ADD COLUMN id SERIAL PRIMARY KEY;
''')
conn.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts', methods=['POST', 'GET'])
def handle_contacts():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            return jsonify({'error': 'Please provide name, email, and message'}), 400

        try:
            cursor.execute('''
                INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)
            ''', (name, email, message))
            conn.commit()
            return redirect(url_for('display_all_contacts'))

        except psycopg2.Error as e:
            conn.rollback()  # Rollback the transaction in case of an error
            return jsonify({'error': f'Database error: {e}'}), 500  # Return an error response
    
    elif request.method == 'GET':
        return jsonify({'message': 'GET method is not supported on this endpoint'}), 405  
    
    
    return jsonify({'error': 'Method not allowed for the requested URL'}), 405  

@app.route('/contacts/all', methods=['GET'])
def display_all_contacts():
    cursor.execute('''SELECT * FROM contacts''')
    contacts = cursor.fetchall()
    return render_template('all_contacts.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)
