# 🤖 Enhanced Agentic AI Server

A powerful, secure, and feature-rich AI-powered code execution server with multi-language support, user authentication, and intelligent code analysis.

## ✨ Features

### 🔐 Security & Authentication
- JWT-based authentication system
- Role-based access control (user/admin)
- Secure password hashing with bcrypt
- Docker-based code isolation

### 💻 Code Execution
- **Multi-language support**: Python, C++, Java, JavaScript, Go
- **Docker-based isolation** for secure execution
- **Resource limits**: Memory, CPU, and time constraints
- **Real-time execution logging** and monitoring

### 🧠 AI-Powered Features
- **Code Analysis**: Comprehensive code review with AI
- **Topic Explanations**: Detailed programming concept explanations
- **Chat Assistant**: Interactive AI programming help
- **Performance Optimization**: AI-driven code improvement suggestions
- **Bug Detection**: Automated code issue identification

### 📊 Analytics & Monitoring
- Execution statistics and success rates
- Language usage analytics
- User activity monitoring
- Health check endpoints

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- OpenAI API key (optional, for enhanced AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sufal6785/AiAgent.git
   cd AiAgent
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Or run locally**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

## 🔧 Configuration

### Environment Variables

```bash
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-here

# OpenAI Configuration (optional)
OPENAI_API_KEY=your-openai-api-key

# Flask Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
```

### Docker Security Settings
The server uses Docker with strict security constraints:
- Memory limit: 128MB
- CPU limit: 0.5 cores
- No network access
- Read-only file system
- Dropped capabilities

## 📡 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User authentication

### Code Execution
- `POST /execute` - Execute code with optional AI analysis

### AI Features
- `POST /ai/explain` - Get AI explanations of programming topics
- `POST /ai/analyze` - Analyze code with AI
- `POST /ai/chat` - Interactive AI chat

### Monitoring
- `GET /health` - Health check and service status
- `GET /stats` - Execution statistics (admin only)

## 🔒 API Usage Examples

### 1. User Registration
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "developer",
    "password": "secure123",
    "role": "user"
  }'
```

### 2. User Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "developer",
    "password": "secure123"
  }'
```

### 3. Execute Python Code
```bash
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "code": "print(\"Hello, AI Agent!\")\nfor i in range(5):\n    print(f\"Count: {i}\")",
    "language": "python",
    "analyze": true
  }'
```

### 4. Get AI Explanation
```bash
curl -X POST http://localhost:5000/ai/explain \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "topic": "binary search algorithm"
  }'
```

### 5. AI Code Analysis
```bash
curl -X POST http://localhost:5000/ai/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)",
    "language": "python"
  }'
```

## 🗂️ Project Structure

```
AiAgent/
├── app.py                 # Main Flask application
├── ai_processing.py       # AI processing module
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env.example          # Environment variables template
├── README.md             # This file
└── data/                 # SQLite database storage
    └── users.db          # User and execution logs
```

## 🛡️ Security Features

### Code Execution Security
- **Docker Isolation**: Each code execution runs in a separate container
- **Resource Limits**: Strict memory, CPU, and time constraints
- **Network Isolation**: No external network access during execution
- **File System Protection**: Read-only mounts and temporary directories
- **Capability Dropping**: Minimal container privileges

### Authentication Security
- **JWT Tokens**: Secure token-based authentication
- **Password Hashing**: bcrypt with salt for password storage
- **Role-Based Access**: Admin and user role separation
- **Request Validation**: Input sanitization and validation

## 🔧 Advanced Configuration

### Custom Language Support
Add new programming languages by extending the `language_configs` in `execute_code_in_docker()`:

```python
"rust": {
    "filename": "main.rs",
    "docker_image": "rust:latest",
    "run_command": ["bash", "-c", "cd /app && rustc main.rs && ./main"]
}
```

### AI Model Configuration
Configure different AI models in `ai_processing.py`:

```python
# For OpenAI GPT-4
model="gpt-4"

# For Claude or other models
# Extend the AIProcessor class with your preferred AI service
```

## 📈 Monitoring and Analytics

### Health Check
```bash
curl http://localhost:5000/health
```

### Execution Statistics (Admin)
```bash
curl -H "Authorization: Bearer ADMIN_JWT_TOKEN" \
     http://localhost:5000/stats
```

## 🐛 Troubleshooting

### Common Issues

1. **Docker not found**
   - Ensure Docker is installed and running
   - Check Docker permissions for the user

2. **OpenAI API errors**
   - Verify API key is correct
   - Check API quota and billing

3. **Memory/timeout errors**
   - Adjust resource limits in Docker configuration
   - Increase timeout values for complex code

### Debug Mode
```bash
export FLASK_DEBUG=True
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask framework for the web server
- Docker for secure code execution
- OpenAI for AI-powered features
- The open-source community for inspiration

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/sufal6785/AiAgent/issues) section
2. Create a new issue with detailed information
3. Join our community discussions

---

**Built with ❤️ for the developer community**