#!/usr/bin/env python3
"""
Test client for the Agentic AI Server
Demonstrates API usage and functionality
"""

import requests
import json
import time

class AgenticAIClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    def register(self, username, password, role="user"):
        """Register a new user"""
        url = f"{self.base_url}/register"
        data = {
            "username": username,
            "password": password,
            "role": role
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json(), response.status_code
    
    def login(self, username, password):
        """Login and get JWT token"""
        url = f"{self.base_url}/login"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data, headers=self.headers)
        result = response.json()
        
        if response.status_code == 200:
            self.token = result.get("access_token")
            self.headers["Authorization"] = f"Bearer {self.token}"
        
        return result, response.status_code
    
    def execute_code(self, code, language="python", analyze=False):
        """Execute code with optional AI analysis"""
        if not self.token:
            return {"error": "Not authenticated"}, 401
        
        url = f"{self.base_url}/execute"
        data = {
            "code": code,
            "language": language,
            "analyze": analyze
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json(), response.status_code
    
    def ai_explain(self, topic):
        """Get AI explanation of a topic"""
        if not self.token:
            return {"error": "Not authenticated"}, 401
        
        url = f"{self.base_url}/ai/explain"
        data = {"topic": topic}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json(), response.status_code
    
    def ai_analyze(self, code, language="python"):
        """Get AI analysis of code"""
        if not self.token:
            return {"error": "Not authenticated"}, 401
        
        url = f"{self.base_url}/ai/analyze"
        data = {
            "code": code,
            "language": language
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json(), response.status_code
    
    def ai_chat(self, message, context=None):
        """Chat with AI assistant"""
        if not self.token:
            return {"error": "Not authenticated"}, 401
        
        url = f"{self.base_url}/ai/chat"
        data = {
            "message": message,
            "context": context or []
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json(), response.status_code
    
    def get_stats(self):
        """Get execution statistics (admin only)"""
        if not self.token:
            return {"error": "Not authenticated"}, 401
        
        url = f"{self.base_url}/stats"
        response = requests.get(url, headers=self.headers)
        return response.json(), response.status_code
    
    def health_check(self):
        """Check server health"""
        url = f"{self.base_url}/health"
        response = requests.get(url)
        return response.json(), response.status_code

def demo():
    """Demonstrate API functionality"""
    print("🤖 Agentic AI Server - Demo Client")
    print("=" * 50)
    
    client = AgenticAIClient()
    
    # Health check
    print("\n1. Health Check")
    result, status = client.health_check()
    print(f"Status: {status}")
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Register user
    print("\n2. User Registration")
    username = f"testuser_{int(time.time())}"
    result, status = client.register(username, "password123")
    print(f"Status: {status}")
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Login
    print("\n3. User Login")
    result, status = client.login(username, "password123")
    print(f"Status: {status}")
    print(f"Result: {json.dumps(result, indent=2)}")
    
    if status != 200:
        print("❌ Login failed, stopping demo")
        return
    
    # Execute Python code
    print("\n4. Code Execution - Python")
    python_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"Fibonacci({i}) = {fibonacci(i)}")
"""
    result, status = client.execute_code(python_code, "python", analyze=True)
    print(f"Status: {status}")
    print(f"Output: {result.get('output', 'No output')}")
    print(f"Success: {result.get('success', False)}")
    print(f"Execution Time: {result.get('execution_time', 0)}s")
    
    # Execute JavaScript code
    print("\n5. Code Execution - JavaScript")
    js_code = """
function isPrime(num) {
    if (num <= 1) return false;
    if (num <= 3) return true;
    if (num % 2 === 0 || num % 3 === 0) return false;
    
    for (let i = 5; i * i <= num; i += 6) {
        if (num % i === 0 || num % (i + 2) === 0) return false;
    }
    return true;
}

console.log("First 10 prime numbers:");
let count = 0;
let num = 2;
while (count < 10) {
    if (isPrime(num)) {
        console.log(num);
        count++;
    }
    num++;
}
"""
    result, status = client.execute_code(js_code, "javascript")
    print(f"Status: {status}")
    print(f"Output: {result.get('output', 'No output')}")
    
    # AI Explanation
    print("\n6. AI Topic Explanation")
    result, status = client.ai_explain("binary search algorithm")
    print(f"Status: {status}")
    print(f"Explanation: {result.get('explanation', 'No explanation')[:200]}...")
    
    # AI Code Analysis
    print("\n7. AI Code Analysis")
    analysis_code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
"""
    result, status = client.ai_analyze(analysis_code, "python")
    print(f"Status: {status}")
    print(f"Analysis: {json.dumps(result.get('analysis', {}), indent=2)}")
    
    # AI Chat
    print("\n8. AI Chat")
    result, status = client.ai_chat("What is the time complexity of quicksort?")
    print(f"Status: {status}")
    print(f"Response: {result.get('response', 'No response')}")
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    try:
        demo()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server. Make sure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")