import requests
import gradio as gr
import openai

openai.api_key = "YOUR_API_KEY"  # Replace with your OpenAI API key

def chatbot_response(user_input):
    """
    If the user input starts with "RUN:", then treat it as a code execution command.
    Otherwise, send the query to OpenAI's GPT-4 for a standard conversational response.
    """
    # Check if this is a code execution request.
    if user_input.startswith("RUN:"):
        # Expected command format: RUN:language code...
        # e.g., "RUN:python print('Hello, world!')"
        parts = user_input.split(maxsplit=1)
        if len(parts) < 2:
            return "Please provide the code to execute."
        # Extract language specifier if provided
        prefix = parts[0].strip()  # e.g., "RUN:python"
        code = parts[1]
        language = "python"  # default language
        if ':' in prefix:
            try:
                language = prefix.split(':')[1].strip().lower()
            except IndexError:
                language = "python"
        payload = {"code": code, "language": language}
        # Insert your valid JWT token after login – for testing, replace with an actual token.
        headers = {"Authorization": "Bearer YOUR_JWT_TOKEN"}
        try:
            response = requests.post("http://localhost:5000/execute", json=payload, headers=headers)
            if response.ok:
                return response.json().get("output", "No output received.")
            else:
                return "Execution failed: " + response.text
        except Exception as e:
            return f"Error reaching execution server: {str(e)}"
    else:
        # For regular queries, use OpenAI's chat model.
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        return response["choices"][0]["message"]["content"]

# Launch the Gradio chatbot interface.
chatbot = gr.ChatInterface(chatbot_response)
chatbot.launch()
