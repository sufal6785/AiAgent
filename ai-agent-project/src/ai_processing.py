from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import fitz  # PyMuPDF for PDF text extraction

openai_api_key = "YOUR_API_KEY"  # Replace with your OpenAI API key

# Initialize the language model and embeddings.
llm = OpenAI(model="gpt-4", openai_api_key=openai_api_key)
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

def ai_explain_dsa(topic):
    """
    Use GPT-4 via LangChain to explain a DSA topic in detail with practical examples.
    """
    response = llm(f"Explain {topic} in detail with practical examples.")
    return response

def extract_pdf_text(pdf_path):
    """Extract full text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])
    return text

def create_vector_store(pdf_path):
    """
    Create a FAISS vector store from the text of a PDF.
    This supports fast semantic retrieval.
    """
    text = extract_pdf_text(pdf_path)
    vector_store = FAISS.from_texts([text], embeddings)
    return vector_store

def query_pdf(pdf_path, question):
    """
    Query a PDF document semantically using vector search.
    Return the most relevant passage.
    """
    vector_store = create_vector_store(pdf_path)
    results = vector_store.similarity_search(question)
    if results:
        return results[0].page_content
    else:
        return "No relevant information found."

# Example usage:
if __name__ == "__main__":
    # AI-powered explanation example:
    explanation = ai_explain_dsa("Binary Search Trees")
    print("AI Explanation of Binary Search Trees:\n", explanation)
    
    # Vector-based search example (ensure 'ds_book.pdf' exists):
    query_result = query_pdf("ds_book.pdf", "Explain recursion with an example.")
    print("\nQuery Result from PDF:\n", query_result)
