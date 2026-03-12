import os
from flask import Flask, render_template, request, redirect, url_for
from google.cloud import firestore

app = Flask(__name__)
APP_VERSION = "1.0.0"

# Initialize Firestore DB client
# Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or running in a GCP environment with default credentials
db = firestore.Client()

@app.route('/')
def index():
    notes_ref = db.collection('notes')
    notes = notes_ref.stream()
    note_list = []
    for note in notes:
        note_data = note.to_dict()
        note_data['id'] = note.id
        note_list.append(note_data)
    return render_template('index.html', notes=note_list, app_version=APP_VERSION)

@app.route('/add', methods=['POST'])
def add_note():
    note_title = request.form['title']
    note_content = request.form['content']
    db.collection('notes').add({'title': note_title, 'content': note_content})
    return redirect(url_for('index'))

@app.route('/note/<id>')
def view_note(id):
    note_ref = db.collection('notes').document(id)
    note = note_ref.get()
    if note.exists:
        note_data = note.to_dict()
        note_data['id'] = note.id
        return render_template('view_note.html', note=note_data, app_version=APP_VERSION)
    return "Note not found", 404

@app.route('/note/delete/<id>', methods=['POST'])
def delete_note(id):
    db.collection('notes').document(id).delete()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
