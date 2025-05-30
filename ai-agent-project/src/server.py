import os
import subprocess
import sqlite3
import bcrypt
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "supersecretkey"  # Change this in production
jwt = JWTManager(app)

def init_db():
    """Create a SQLite database with a users table if it doesn't exist."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password BLOB,
            role TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]
    role = data.get("role", "user")
    
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, hashed_password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"message": "User already exists"}), 400
    conn.close()
    return jsonify({"message": "User registered successfully!"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode(), user[0]):
        access_token = create_access_token(identity={"username": username, "role": user[1]})
        return jsonify({"access_token": access_token})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

def execute_code_in_docker(code, language):
    """
    Save the user-submitted code to a file and execute it inside a Docker container.
    Returns output or error messages (debug info) from the sandboxed execution.
    """
    # Determine filename based on language.
    filename = None
    docker_image = None
    run_command = None

    if language == "python":
        filename = "code.py"
        docker_image = "python:3.9-slim"
        # Mount the file into /app and run it
        run_command = ["python", "/app/code.py"]
    elif language == "cpp":
        filename = "code.cpp"
        docker_image = "gcc:latest"
        # Compile and run via bash command in docker
        run_command = ["bash", "-c", "g++ /app/code.cpp -o /app/code.out && /app/code.out"]
    elif language == "java":
        filename = "Main.java"
        docker_image = "openjdk:11-jdk-slim"
        run_command = ["bash", "-c", "javac /app/Main.java && java -cp /app Main"]
    else:
        return "Unsupported language."
    
    # Write the code into the file
    with open(filename, "w") as f:
        f.write(code)
    
    # Get the full absolute path so Docker can mount it
    abs_path = os.path.abspath(filename)
    mount_arg = f"{abs_path}:/app/{filename}"
    
    # Build the Docker run command
    command = ["docker", "run", "--rm", "-v", mount_arg, docker_image] + run_command

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout if result.stdout.strip() != "" else "Execution completed successfully."
        else:
            return f"Error:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "Execution timed out!"

@app.route("/execute", methods=["POST"])
@jwt_required()
def execute():
    data = request.json
    code = data.get("code")
    language = data.get("language", "python")
    
    output = execute_code_in_docker(code, language)
    return jsonify({"output": output})

if __name__ == "__main__":
    init_db()
    app.run(port=5000)
