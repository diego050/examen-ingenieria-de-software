# src/infrastructure/adapters/api.py
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from src.application.services import PersonajeService, ComentarioService
from src.infrastructure.adapters.database import SQLAlchemyPersonajeRepository, SQLAlchemyComentarioRepository
from src.infrastructure.config import SessionLocal

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key-for-dev") # Una clave por defecto para desarrollo
jwt = JWTManager(app)

# --- Composition Root ---
# Aquí es donde "unimos" las piezas: creamos instancias concretas y las inyectamos.
def get_personaje_service():
    session = SessionLocal()
    repository = SQLAlchemyPersonajeRepository(session)
    return PersonajeService(repository)

def get_comentario_service():
    session = SessionLocal()
    personaje_repo = SQLAlchemyPersonajeRepository(session)
    comentario_repo = SQLAlchemyComentarioRepository(session)
    return ComentarioService(comentario_repo, personaje_repo)
# --- Fin Composition Root ---


# --- Endpoints de Personajes ---
@app.route('/api/personajes', methods=['GET'])
@jwt_required()
def listar_personajes_endpoint():
    service = get_personaje_service()
    personajes = service.listar_personajes()
    return jsonify([p.__dict__ for p in personajes])

@app.route('/api/personajes', methods=['POST'])
@jwt_required() 
def crear_personaje_endpoint():
    datos = request.json
    service = get_personaje_service()
    try:
        nuevo_personaje = service.crear_personaje(
            nombre=datos['nombre'],
            aldea=datos['aldea'],
            jutsu_principal=datos['jutsu_principal']
        )
        return jsonify(nuevo_personaje.__dict__), 201
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400

# --- Endpoints de Comentarios ---
@app.route('/api/comentario', methods=['POST'])
def agregar_comentario_endpoint():
    datos = request.json
    service = get_comentario_service()
    try:
        nuevo_comentario = service.agregar_comentario(
            personaje_id=int(datos['personaje_id']),
            autor=datos['autor'],
            texto=datos['texto']
        )
        return jsonify(nuevo_comentario.__dict__), 201
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/comentario/<int:personaje_id>', methods=['GET'])
def ver_comentarios_endpoint(personaje_id):
    service = get_comentario_service()
    comentarios = service.ver_comentarios_por_personaje(personaje_id)
    return jsonify([c.__dict__ for c in comentarios])

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



if __name__ == '__main__':
    # Creación de tablas al iniciar (solo para desarrollo, en producción se usan migraciones)
    from src.infrastructure.adapters.database import metadata
    from src.infrastructure.config import engine
    metadata.create_all(bind=engine)
    
    app.run(host='0.0.0.0', port=5000)