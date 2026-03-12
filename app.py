import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit

# 1. Load API Key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("🔑 API Key Missing! Please check your .env file in D:/frammer")
    st.stop()

# 2. Page Styling
st.set_page_config(page_title="Chatbot", page_icon="🎬")
st.title("🎬 Data Chatbot")
st.markdown("Analyze video production, languages, and publishing trends in real-time.")

# 3. Backend Connection
@st.cache_resource
def initialize_agent():
    DB_URL = "postgresql://admin:password123@localhost:5432/frammer_analytics"
    db = SQLDatabase.from_uri(DB_URL)
    
    # Brain (Llama 3.3 70B - Best for complex SQL)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    
    # SYSTEM INSTRUCTIONS: The "Secret Sauce"
    CUSTOM_PREFIX = """
 You are the Senior Data Scientist at Frammer AI.
    
    1. For language popularity or counts, ALWAYS use the 'combined_data_by_language' table.
    2. For channel-specific publishing, use 'channel_wise_publishing'.
    3. For monthly trends, use 'monthly_chart'.
    4. If a result involves multiple rows, ALWAYS return a Markdown Table.
    5. If the AI finds 'Unknown', check if there is another table with better data before answering.
    6. Conclude with a 1-sentence business insight.
    """

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    return create_sql_agent(
        llm=llm, 
        toolkit=toolkit, 
        verbose=True, 
        agent_type="tool-calling",
        prefix=CUSTOM_PREFIX # Injects professional logic
    )

agent_executor = initialize_agent()

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. The "Action" Loop
if prompt := st.chat_input("Ex: Show me a table of uploads by language"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # We use a container to show "Thought Process" logs if you want to be fancy
        with st.spinner("🤖 Orchestrating Query..."):
            try:
                # Running the agent
                response = agent_executor.invoke({"input": prompt})
                full_response = response["output"]
                
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Agent Error: {e}")

# 6. Optional: Quick Visualization (Bonus for Selection)
if st.session_state.messages:
    if st.button("📊 Generate Quick Chart"):
        st.info("Tip: In a full production app, I would use Plotly to render this SQL result as a bar chart!")
        # For your demo, you can show the judges you know how to handle dataframes:
        # df = pd.read_sql(last_query, engine)
        # st.bar_chart(df)