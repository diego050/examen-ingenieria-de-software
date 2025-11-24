# src/infrastructure/adapters/api.py
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from src.application.services import StudentService
from src.application.mappers import StudentMapper, EvaluationMapper
from src.infrastructure.adapters.database import SQLAlchemyStudentRepository, SQLAlchemyEvaluationRepository
from src.infrastructure.config import SessionLocal

app = Flask(__name__)
# Allow CORS for API endpoints and include Authorization header for JWT
CORS(app, resources={r"/api/*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization"]) 

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key-for-dev") # Una clave por defecto para desarrollo
jwt = JWTManager(app)

# --- Composition Root ---
# Aquí es donde "unimos" las piezas: creamos instancias concretas y las inyectamos.
def get_student_service():
    session = SessionLocal()
    student_repo = SQLAlchemyStudentRepository(session)
    evaluation_repo = SQLAlchemyEvaluationRepository(session)
    return StudentService(student_repo, evaluation_repo)
# --- Fin Composition Root ---


@app.route('/api/students', methods=['GET'])
@jwt_required()
def listar_students_endpoint():
    service = get_student_service()
    students = service.listar_estudiantes()
    return jsonify(StudentMapper.to_list(students))


@app.route('/api/students', methods=['POST'])
@jwt_required()
def crear_student_endpoint():
    datos = request.json
    service = get_student_service()
    try:
        nuevo = service.crear_estudiante(
            code=datos['code'],
            nombre=datos['nombre'],
            attendance=datos.get('attendance', True)
        )
        return jsonify(StudentMapper.to_dict(nuevo)), 201
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/evaluations', methods=['POST'])
def agregar_evaluation_endpoint():
    datos = request.json
    service = get_student_service()
    try:
        nuevo = service.agregar_evaluacion(
            student_id=int(datos['student_id']),
            score=float(datos['score']),
            weight=float(datos['weight'])
        )
        return jsonify(EvaluationMapper.to_dict(nuevo)), 201
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/students/<int:student_id>/evaluations', methods=['GET'])
def ver_evaluaciones_endpoint(student_id):
    service = get_student_service()
    evaluations = service.evaluation_repo.find_by_student_id(student_id)
    return jsonify(EvaluationMapper.to_list(evaluations))


@app.route('/api/students/<int:student_id>/attendance', methods=['POST'])
def set_attendance_endpoint(student_id):
    datos = request.json
    service = get_student_service()
    try:
        student = service.set_attendance(student_id, bool(datos.get('attendance')))
        return jsonify(StudentMapper.to_dict(student)), 200
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/students/<int:student_id>/grade', methods=['GET'])
def ver_nota_final_endpoint(student_id):
    service = get_student_service()
    try:
        result = service.calcular_nota_final(student_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # Para el examen, usamos credenciales fijas. En un proyecto real, consultarías la base de datos.
    if username != "admin" or password != "admin":
        return jsonify({"msg": "Bad username or password"}), 401

    # Si las credenciales son correctas, creamos el token.
    # La "identidad" puede ser cualquier cosa que identifique al usuario (ID, username, etc.).
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/api/seed', methods=['POST'])
def seed_data():
    """Seed the database with example students and evaluations (development only).

    If students already exist, this returns a 200 and does nothing.
    """
    service = get_student_service()
    existing = service.listar_estudiantes()
    if existing:
        return jsonify({"message": "Already seeded", "students": len(existing)}), 200

    # Create example students
    s1 = service.crear_estudiante(code='S001', nombre='Juan Perez', attendance=True)
    s2 = service.crear_estudiante(code='S002', nombre='María García', attendance=True)
    s3 = service.crear_estudiante(code='S003', nombre='Luis Rodríguez', attendance=False)

    # Add evaluations
    service.agregar_evaluacion(student_id=s1.id, score=14, weight=50)
    service.agregar_evaluacion(student_id=s1.id, score=16, weight=50)
    service.agregar_evaluacion(student_id=s2.id, score=18, weight=100)

    return jsonify({"message": "Seeded", "students": 3}), 201



if __name__ == '__main__':
    # Creación de tablas al iniciar (solo para desarrollo, en producción se usan migraciones)
    from src.infrastructure.adapters.database import metadata
    from src.infrastructure.config import engine
    metadata.create_all(bind=engine)
    
    app.run(host='0.0.0.0', port=5000)