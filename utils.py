import os
from dotenv import load_dotenv
from few_shots import few_shots
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma
# Load API Key
load_dotenv("config.env")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize LLM
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash-latest', temperature=0.2)

# Example Prompt Template
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="InputQuery: {MySQL Query}\nOutputQuery: {DuckDB Query}"
)

# Conversion rules and formatting
conversion_prompt = """
    You are a SQL expert. Convert the input query into DuckDB following these rules:
    1. Use CTEs for transformations.
    2. Avoid Subqueries.
    3. Use COALESCE for handling NULL values.
    4. Use CAST(col AS DATE) instead of DATE().
    5. Use `DATEDIFF` in `DATEDIFF('day'/'month'/'year', start_date, end_date)` format.
    6. Replace `{{USERID}}` and `{{PVDATE}}` with `{{user_id}}` and `{{pv_date}}`.
    Example: 
    Input MySQL Query:
    Converted DuckDB Query:
"""

# Function to set up embeddings
def setup_embeddings():
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# Function to initialize vector store
def setup_vector_store(embeddings, few_shots):
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    return Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)

# Main function to convert MySQL query to DuckDB query with response formatting
def convert_query(query):
    embeddings = setup_embeddings()
    vector_store = setup_vector_store(embeddings, few_shots)

    example_selector = SemanticSimilarityExampleSelector(vectorstore=vector_store, k=2)
    prompt_template = FewShotPromptTemplate(
        examples=few_shots,
        example_prompt=example_prompt,
        prefix=conversion_prompt,
        suffix="InputQuery: {query}\nOutputQuery:",
        input_variables=["query"]
    )
    prompt = prompt_template.format(query=query)

    # Invoke model with prompt
    response = llm.invoke(prompt)
    
    # Format and clean the response
    query_output = response.content
    if query_output.startswith("```sql") and query_output.endswith("```"):
        return query_output[6:-3].strip()
    return query_output
