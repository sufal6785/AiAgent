# =============================================================================
# ENHANCED AGENTIC AI SERVER - Complete Implementation
# =============================================================================

import os
import subprocess
import sqlite3
import bcrypt
import tempfile
import logging
import json
import time
from datetime import timedelta
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from ai_processing import AIProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey-change-in-production")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)

# Initialize AI processor
ai_processor = AIProcessor()

def init_db():
    """Create a SQLite database with users and execution_logs tables."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Execution logs table for monitoring
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            language TEXT,
            code_hash TEXT,
            execution_time REAL,
            success BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    """)
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

def log_execution(username, language, code_hash, execution_time, success):
    """Log code execution for monitoring and analytics."""
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO execution_logs (username, language, code_hash, execution_time, success) VALUES (?, ?, ?, ?, ?)",
            (username, language, code_hash, execution_time, success)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to log execution: {e}")

@app.route("/", methods=["GET"])
def home():
    """API health check endpoint."""
    return jsonify({
        "message": "Agentic AI API is running!",
        "version": "2.0",
        "endpoints": [
            "/register", "/login", "/execute", 
            "/ai/explain", "/ai/analyze", "/ai/chat",
            "/stats", "/health"
        ]
    })

@app.route("/health", methods=["GET"])
def health_check():
    """Detailed health check including Docker availability."""
    health_status = {"status": "healthy", "services": {}}
    
    # Check Docker availability
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True, timeout=5)
        health_status["services"]["docker"] = "available" if result.returncode == 0 else "unavailable"
    except Exception:
        health_status["services"]["docker"] = "unavailable"
    
    # Check database
    try:
        conn = sqlite3.connect("users.db")
        conn.execute("SELECT 1")
        conn.close()
        health_status["services"]["database"] = "available"
    except Exception:
        health_status["services"]["database"] = "unavailable"
    
    # Check AI processor
    health_status["services"]["ai_processor"] = "available" if ai_processor else "unavailable"
    
    return jsonify(health_status)

@app.route("/register", methods=["POST"])
def register():
    """Enhanced user registration with validation."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        username = data.get("username", "").strip()
        password = data.get("password", "")
        role = data.get("role", "user")
        
        # Validation
        if not username or len(username) < 3:
            return jsonify({"error": "Username must be at least 3 characters"}), 400
        
        if not password or len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        
        if role not in ["user", "admin"]:
            return jsonify({"error": "Invalid role"}), 400
        
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                (username, hashed_password, role)
            )
            conn.commit()
            logger.info(f"User {username} registered successfully")
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({"error": "Username already exists"}), 409
        finally:
            conn.close()
        
        return jsonify({"message": "User registered successfully!", "username": username})
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({"error": "Registration failed"}), 500

@app.route("/login", methods=["POST"])
def login():
    """Enhanced login with better error handling."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No credentials provided"}), 400
        
        username = data.get("username", "").strip()
        password = data.get("password", "")
        
        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400
        
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode(), user[0]):
            access_token = create_access_token(
                identity={"username": username, "role": user[1]}
            )
            logger.info(f"User {username} logged in successfully")
            return jsonify({
                "access_token": access_token,
                "username": username,
                "role": user[1],
                "message": "Login successful"
            })
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            return jsonify({"error": "Invalid credentials"}), 401
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"error": "Login failed"}), 500

def execute_code_in_docker(code, language, timeout=15):
    """
    Enhanced Docker-based code execution with better security and error handling.
    """
    import hashlib
    
    start_time = time.time()
    code_hash = hashlib.md5(code.encode()).hexdigest()[:8]
    
    # Language configurations
    language_configs = {
        "python": {
            "filename": "code.py",
            "docker_image": "python:3.9-slim",
            "run_command": ["python", "/app/code.py"]
        },
        "cpp": {
            "filename": "code.cpp",
            "docker_image": "gcc:latest",
            "run_command": ["bash", "-c", "cd /app && g++ -o code.out code.cpp && ./code.out"]
        },
        "java": {
            "filename": "Main.java",
            "docker_image": "openjdk:11-jdk-slim",
            "run_command": ["bash", "-c", "cd /app && javac Main.java && java Main"]
        },
        "javascript": {
            "filename": "code.js",
            "docker_image": "node:16-slim",
            "run_command": ["node", "/app/code.js"]
        },
        "go": {
            "filename": "main.go",
            "docker_image": "golang:1.19-alpine",
            "run_command": ["go", "run", "/app/main.go"]
        }
    }
    
    if language not in language_configs:
        return {
            "output": f"Unsupported language: {language}",
            "success": False,
            "execution_time": 0
        }
    
    config = language_configs[language]
    
    # Create temporary directory for better isolation
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, config["filename"])
        
        # Write code to temporary file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
        except Exception as e:
            return {
                "output": f"Failed to write code file: {str(e)}",
                "success": False,
                "execution_time": 0
            }
        
        # Docker security settings
        docker_command = [
            "docker", "run", "--rm",
            "--memory=128m",           # Limit memory
            "--memory-swap=128m",      # Disable swap
            "--cpus=0.5",             # Limit CPU
            "--network=none",         # No network access
            "--cap-drop=ALL",         # Drop all capabilities
            "--security-opt", "no-new-privileges",  # Security
            "-v", f"{temp_dir}:/app:ro",  # Read-only mount
            config["docker_image"]
        ] + config["run_command"]
        
        try:
            result = subprocess.run(
                docker_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir
            )
            
            execution_time = time.time() - start_time
            success = result.returncode == 0
            
            output = result.stdout if success else f"Error (Code {result.returncode}):\n{result.stderr}"
            
            return {
                "output": output.strip() if output.strip() else "Execution completed (no output)",
                "success": success,
                "execution_time": round(execution_time, 3),
                "code_hash": code_hash
            }
            
        except subprocess.TimeoutExpired:
            return {
                "output": f"Execution timed out after {timeout} seconds",
                "success": False,
                "execution_time": timeout
            }
        except FileNotFoundError:
            return {
                "output": "Docker not found. Please install Docker to execute code.",
                "success": False,
                "execution_time": 0
            }
        except Exception as e:
            return {
                "output": f"Execution error: {str(e)}",
                "success": False,
                "execution_time": time.time() - start_time
            }

@app.route("/execute", methods=["POST"])
@jwt_required()
def execute():
    """Enhanced code execution endpoint with logging and analysis."""
    try:
        current_user = get_jwt_identity()
        username = current_user["username"]
        
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        code = data.get("code", "").strip()
        language = data.get("language", "python").lower()
        
        if not code:
            return jsonify({"error": "No code provided"}), 400
        
        # Security check: basic code validation
        if len(code) > 10000:  # 10KB limit
            return jsonify({"error": "Code too large (max 10KB)"}), 400
        
        # Execute code
        result = execute_code_in_docker(code, language)
        
        # Log execution
        log_execution(
            username, 
            language, 
            result.get("code_hash", ""), 
            result.get("execution_time", 0), 
            result.get("success", False)
        )
        
        # Add AI analysis if requested
        if data.get("analyze", False):
            try:
                analysis = ai_processor.analyze_code(code, language)
                result["analysis"] = analysis
            except Exception as e:
                result["analysis_error"] = str(e)
        
        logger.info(f"Code execution by {username}: {language}, success: {result.get('success')}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Execution endpoint error: {e}")
        return jsonify({"error": "Execution failed"}), 500

@app.route("/ai/explain", methods=["POST"])
@jwt_required()
def ai_explain():
    """AI-powered topic explanation."""
    try:
        data = request.json
        topic = data.get("topic", "").strip()
        
        if not topic:
            return jsonify({"error": "No topic provided"}), 400
        
        explanation = ai_processor.explain_topic(topic)
        
        return jsonify({
            "topic": topic,
            "explanation": explanation,
            "source": "AI-generated"
        })
        
    except Exception as e:
        logger.error(f"AI explanation error: {e}")
        return jsonify({"error": "Failed to generate explanation"}), 500

@app.route("/ai/analyze", methods=["POST"])
@jwt_required()
def ai_analyze():
    """AI-powered code analysis."""
    try:
        data = request.json
        code = data.get("code", "").strip()
        language = data.get("language", "python")
        
        if not code:
            return jsonify({"error": "No code provided"}), 400
        
        analysis = ai_processor.analyze_code(code, language)
        
        return jsonify({
            "code_length": len(code),
            "language": language,
            "analysis": analysis
        })
        
    except Exception as e:
        logger.error(f"AI analysis error: {e}")
        return jsonify({"error": "Failed to analyze code"}), 500

@app.route("/ai/chat", methods=["POST"])
@jwt_required()
def ai_chat():
    """General AI chat endpoint."""
    try:
        data = request.json
        message = data.get("message", "").strip()
        context = data.get("context", [])
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Simple chat responses (extend with your preferred LLM)
        response = ai_processor.chat_response(message, context)
        
        return jsonify({
            "message": message,
            "response": response,
            "timestamp": str(time.time())
        })
        
    except Exception as e:
        logger.error(f"AI chat error: {e}")
        return jsonify({"error": "Chat failed"}), 500

@app.route("/stats", methods=["GET"])
@jwt_required()
def get_stats():
    """Get execution statistics (admin only)."""
    try:
        current_user = get_jwt_identity()
        if current_user["role"] != "admin":
            return jsonify({"error": "Admin access required"}), 403
        
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Get basic stats
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM execution_logs")
        total_executions = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM execution_logs WHERE success = 1")
        successful_executions = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT language, COUNT(*) as count 
            FROM execution_logs 
            GROUP BY language 
            ORDER BY count DESC
        """)
        language_stats = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            "total_users": total_users,
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "success_rate": round((successful_executions / total_executions * 100), 2) if total_executions > 0 else 0,
            "language_usage": dict(language_stats)
        })
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({"error": "Failed to get statistics"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Get configuration from environment
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5000))
    
    logger.info(f"Starting Agentic AI Server on {host}:{port} (debug={debug})")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )