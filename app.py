from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
students = [
    {'id': 1, 'name': 'Memoona', 'grade': 'A'},
    {'id': 2, 'name': 'Sara', 'grade': 'B'},
]

next_id = 3  # Tracks the next available ID

@app.route('/')
def home():
    return "Welcome to the Student API! Visit /api/students to see all students."

@app.route('/api/health')

def health():
    return jsonify({"status": "ok" , "message":"flask is running"})

@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(students), 200


# READ ONE
@app.route('/api/students/<int:sid>', methods=['GET'])
def get_student(sid):
    s = next((s for s in students if s['id'] == sid), None)
    if s:
        return jsonify(s), 200
    else:
        return jsonify({'error': 'Not found'}), 404


# CREATE
@app.route('/api/students', methods=['POST'])
def add_student():
    global next_id

    data = request.get_json()
    if not data or 'name' not in data or 'grade' not in data:
        return jsonify({'error': 'name and grade are required'}), 400

    new_student = {
        'id': next_id,
        'name': data['name'],
        'grade': data['grade']
    }

    students.append(new_student)
    next_id += 1

    return jsonify(new_student), 201


# UPDATE
@app.route('/api/students/<int:sid>', methods=['PUT'])
def update_student(sid):
    s = next((s for s in students if s['id'] == sid), None)

    if not s:
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json()

    s['name'] = data.get('name', s['name'])
    s['grade'] = data.get('grade', s['grade'])

    return jsonify(s), 200


# DELETE
@app.route('/api/students/<int:sid>', methods=['DELETE'])
def delete_student(sid):
    global students

    original_len = len(students)
    students = [s for s in students if s['id'] != sid]

    if len(students) == original_len:
        return jsonify({'error': 'Not found'}), 404

    return jsonify({'message': 'Deleted successfully'}), 200


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=5001)