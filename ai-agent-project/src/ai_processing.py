# =============================================================================
# AI_PROCESSING.PY - Enhanced AI Processing Module
# =============================================================================

import openai
import os
import time
import json
from typing import Optional, List, Dict, Any

class AIProcessor:
    """Enhanced AI processing with multiple capabilities."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        
        # Chat context storage (in production, use Redis/database)
        self.chat_contexts = {}
    
    def explain_topic(self, topic: str) -> str:
        """Generate detailed explanation of programming topics."""
        try:
            if not self.api_key:
                return self._fallback_explanation(topic)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert programming tutor. Provide detailed, practical explanations with examples and use cases."
                    },
                    {
                        "role": "user", 
                        "content": f"Explain {topic} in detail with practical examples, implementation tips, and real-world applications."
                    }
                ],
                max_tokens=1200,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating explanation: {str(e)}"
    
    def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """Comprehensive code analysis."""
        try:
            if not self.api_key:
                return self._fallback_analysis(code, language)
            
            prompt = f"""
            Analyze this {language} code comprehensively:

            ```{language}
            {code}
            ```

            Provide analysis in JSON format with these keys:
            - "complexity": Time and space complexity analysis
            - "bugs": Array of potential bugs or issues
            - "suggestions": Array of improvement suggestions  
            - "performance": Performance optimization recommendations
            - "readability": Code readability assessment
            - "security": Security considerations (if applicable)
            - "best_practices": Best practices recommendations
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert code reviewer. Provide thorough, actionable analysis in valid JSON format."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                return {"analysis": response.choices[0].message.content}
                
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def chat_response(self, message: str, context: List[Dict] = None) -> str:
        """Generate conversational AI responses."""
        try:
            if not self.api_key:
                return self._fallback_chat(message)
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful programming assistant. Provide clear, practical answers to coding questions."
                }
            ]
            
            # Add context if provided
            if context:
                messages.extend(context[-5:])  # Keep last 5 exchanges
            
            messages.append({"role": "user", "content": message})
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=800,
                temperature=0.8
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Chat error: {str(e)}"
    
    def _fallback_explanation(self, topic: str) -> str:
        """Fallback explanations when AI is unavailable."""
        explanations = {
            "binary search": "Binary Search is an efficient algorithm for finding a target value in a sorted array. It works by repeatedly dividing the search interval in half. Time complexity: O(log n), Space complexity: O(1) for iterative version.",
            
            "recursion": "Recursion is a programming technique where a function calls itself to solve smaller instances of the same problem. Key components: base case (stopping condition) and recursive case (function calls itself). Common examples: factorial, fibonacci, tree traversal.",
            
            "dynamic programming": "Dynamic Programming solves complex problems by breaking them into simpler subproblems and storing solutions to avoid redundant calculations. Two approaches: top-down (memoization) and bottom-up (tabulation). Examples: knapsack, longest common subsequence.",
            
            "linked list": "A linear data structure where elements (nodes) are stored in sequence, each containing data and a reference to the next node. Types: singly, doubly, circular. Operations: insertion, deletion, traversal. Time complexity varies by operation and position.",
            
            "sorting algorithms": "Algorithms that arrange elements in a specific order. Common types: Bubble Sort O(n²), Quick Sort O(n log n) average, Merge Sort O(n log n), Heap Sort O(n log n). Each has different trade-offs for time, space, and stability."
        }
        
        topic_lower = topic.lower()
        for key, explanation in explanations.items():
            if key in topic_lower or topic_lower in key:
                return explanation
        
        return f"Explanation for '{topic}' is not available offline. Please configure OpenAI API for AI-powered explanations."
    
    def _fallback_analysis(self, code: str, language: str) -> Dict[str, Any]:
        """Basic code analysis without AI."""
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            "complexity": "Analysis requires AI configuration",
            "suggestions": [
                f"Code has {len(lines)} total lines, {len(non_empty_lines)} non-empty",
                "Consider adding comments for clarity",
                "Review variable naming conventions",
                "Consider breaking down large functions"
            ],
            "bugs": ["Manual code review recommended"],
            "performance": "Requires detailed AI analysis for optimization suggestions",
            "readability": f"Code structure appears {'simple' if len(non_empty_lines) < 20 else 'moderate' if len(non_empty_lines) < 50 else 'complex'}",
            "security": "Security analysis requires AI configuration",
            "best_practices": ["Follow language-specific style guides", "Add error handling", "Include unit tests"]
        }
    
    def _fallback_chat(self, message: str) -> str:
        """Simple chat responses without AI."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            return "Hello! I'm your programming assistant. I can help explain concepts, analyze code, and answer programming questions. (Note: Advanced AI features require OpenAI API configuration)"
        
        elif any(word in message_lower for word in ["help", "what can you do"]):
            return """I can help you with:
            • Code execution in multiple languages
            • Programming concept explanations  
            • Code analysis and optimization
            • Algorithm and data structure guidance
            • Debugging assistance
            
            Try commands like 'explain binary search' or 'analyze my code'!"""
        
        elif "time complexity" in message_lower:
            return "Time complexity measures how algorithm runtime grows with input size. Common complexities: O(1) constant, O(log n) logarithmic, O(n) linear, O(n²) quadratic, O(2ⁿ) exponential."
        
        else:
            return f"I understand you're asking about: '{message}'. For detailed AI-powered responses, please configure the OpenAI API key. I can still help with code execution and basic programming guidance!"