from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

contacts = []  

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

        new_contact = {
            'name': name,
            'email': email,
            'message': message
        }

        contacts.append(new_contact)
        return redirect(url_for('display_all_contacts'))
    
    elif request.method == 'GET':
        return jsonify({'message': 'GET method is not supported on this endpoint'}), 405  
    
    
    return jsonify({'error': 'Method not allowed for the requested URL'}), 405  

@app.route('/contacts/all', methods=['GET'])
def display_all_contacts():
    return render_template('all_contacts.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)
