from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudiantes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Estudiante
class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    carrera = db.Column(db.String(100), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'carrera': self.carrera,
            'semestre': self.semestre
        }

# Crear la base de datos (solo la primera vez)
with app.app_context():
    db.create_all()

# Endpoint para agregar un estudiante
@app.route('/estudiantes', methods=['POST'])
def agregar_estudiante():
    data = request.get_json()
    if not data or not all(k in data for k in ("nombre", "carrera", "semestre")):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    nuevo_estudiante = Estudiante(
        nombre=data['nombre'],
        carrera=data['carrera'],
        semestre=data['semestre']
    )
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return jsonify({'mensaje': 'Estudiante registrado', 'estudiante': nuevo_estudiante.to_dict()}), 201

# Endpoint para consultar todos los estudiantes
@app.route('/estudiantes', methods=['GET'])
def listar_estudiantes():
    estudiantes = Estudiante.query.all()
    return jsonify([e.to_dict() for e in estudiantes]), 200

if __name__ == '__main__':
    app.run(debug=True)