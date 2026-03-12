import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit

# 1. LOAD CONFIGURATION
load_dotenv() # This pulls GROQ_API_KEY from your .env file

# 2. CONNECT TO DOCKER DATABASE
DB_URL = "postgresql://admin:password123@localhost:5432/frammer_analytics"
db = SQLDatabase.from_uri(DB_URL)

# 3. INITIALIZE LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 4. CUSTOM SYSTEM INSTRUCTIONS (The "Orchestrator" Brain)
# This prevents the AI from guessing wrong table names like it did before
CUSTOM_PREFIX = """
You are an expert data analyst for Frammer AI.
- Use 'monthly_chart' for time-related questions.
- Use 'client_1_combined_data' for high-level channel stats.
- If you encounter an error, reflect on the table schema and try a different query.
- Always provide a concise, human-readable summary of the data found.
"""

# 5. CREATE THE AGENT
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True, 
    agent_type="tool-calling",
    prefix=CUSTOM_PREFIX # Adding the brain instructions here
)

# 6. CHAT LOOP
print("\n🚀 Frammer AI Chatbot is ONLINE (Groq-Powered)")
print("Type 'exit' to stop.\n")

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    try:
        response = agent_executor.invoke({"input": user_input})
        print(f"\nAI: {response['output']}\n")
    except Exception as e:
        # This catch is good, but LangChain's internal loop 
        # usually handles SQL errors itself!
        print(f"\n❌ Error: {e}\n")