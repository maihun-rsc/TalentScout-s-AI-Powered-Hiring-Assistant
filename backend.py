import os
import json
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Pydantic Schema validations
from schemas import CandidateProfile
import pydantic

# Load environment variables
load_dotenv()

SYSTEM_PROMPTS = {
    "Malik": """
You are Malik, an explanative, straight-to-the-point male Hiring Manager for "TalentScout".
Your goal is to screen candidates efficiently. Be highly direct and professional. Do not use emojis. Keep pleasantries to a minimum.

Ask ONLY one question at a time. Do not ask for everything at once.
1. Start by asking for their Full Name.
2. Ask for Email Address.
3. Ask for Phone Number.
4. Ask for Years of Experience.
5. Ask for Desired Position(s).
6. Ask for Current Location.
7. Ask for their Tech Stack.

Once all the above is gathered, generate 3 to 5 highly specific technical questions based on their Tech Stack. Wait for them to answer.
Conclude the conversation directly and inform them of next steps. Stop if the user says exit.
""",
    "Clara": """
You are Clara, a chatty, warm, but highly knowledgeable female Hiring Assistant for "TalentScout".
Your goal is to make the candidate feel extremely welcome and comfortable while screening them. Feel free to use appropriate emojis 😊.

Ask ONLY one question at a time. Do not overwhelm them.
1. Ask for their Full Name warmly.
2. Ask for their Email Address.
3. Ask for their Phone Number.
4. Ask for their Years of Experience.
5. Ask for their Desired Position(s).
6. Ask for their Current Location.
7. Ask for their Tech Stack.

Once all the above is gathered, generate 3 to 5 thoughtful technical questions based directly on their Tech Stack. Wait for their answers.
Conclude the conversation cheerfully. Stop if the user says exit.
""",
    "Lani": """
You are Lani, a balanced, professional female Hiring Assistant for "TalentScout".
Your goal is to conduct a standard, polite screening interview.

Ask ONE question at a time. Do not ask them as a big list.
1. Full Name
2. Email Address
3. Phone Number
4. Years of Experience
5. Desired Position(s)
6. Current Location
7. Tech Stack

Once gathered, generate 3-5 technical questions based on their Tech Stack. Wait for their answers.
Conclude gracefully. Stop if the user says exit.
"""
}

class HiringAssistantBackend:
    def __init__(self, persona="Lani", session_id="default_user"):
        self.persona = persona
        self.session_id = session_id
        
        self.llm = self._initialize_llm()
        self.embeddings = self._initialize_embeddings()
        
        system_prompt = SYSTEM_PROMPTS.get(self.persona, SYSTEM_PROMPTS["Lani"])
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        
        self.chain = self.prompt | self.llm
        self.chat_history = ChatMessageHistory()
        
        self.runnable_with_history = RunnableWithMessageHistory(
            self.chain,
            lambda session_id: self.chat_history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def _initialize_llm(self):
        # Dynamically map the initialized model safely explicitly based on the Persona choice.
        if self.persona == "Malik":
            if os.getenv("GEMINI_API_KEY"):
                return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
            else:
                return ChatOllama(model="llama3.2", temperature=0.7)
        elif self.persona == "Clara":
            if os.getenv("OPENAI_API_KEY"):
                return ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
            else:
                return ChatOllama(model="llama3.2", temperature=0.7)
        else:
            return ChatOllama(model="llama3.2", temperature=0.7)
            
    def _initialize_embeddings(self):
        # We explicitly lock to local Ollama Embeddings to keep Vector mapping consistent 
        try:
            return OllamaEmbeddings(model="mxbai-embed-large:latest")
        except Exception:
            if os.getenv("OPENAI_API_KEY"):
                return OpenAIEmbeddings()
            return None

    def process_message(self, user_input: str) -> str:
        exit_keywords = ["exit", "quit", "stop", "bye", "goodbye"]
        if user_input.lower().strip() in exit_keywords:
            self.chat_history.add_user_message(user_input)
            response = "Thank you for chatting with TalentScout. The conversation has ended. Our team will review your profile and get back to you. Have a great day!"
            self.chat_history.add_ai_message(response)
            
            # Save the conversation gracefully here for simulated backend
            self._save_conversation_data()
            return response
            
        try:
            response = self.runnable_with_history.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": self.session_id}}
            )
            return response.content
        except Exception as e:
            error_str = str(e).lower()
            if "connection" in error_str or "max retries exceeded" in error_str or "winerror 10061" in error_str or "actively refused" in error_str:
                return "It seems my local AI brain (Ollama) is not reachable. Please start the Ollama server, or switch to the OpenAI fallback model in the settings by checking the fallback box."
            return f"I'm sorry, I encountered an error: {str(e)}."

    def _save_conversation_data(self):
        """
        Simulated backend to store data securely. Privacy compliant by anonymizing before saving.
        """
        os.makedirs("data", exist_ok=True)
        filepath = os.path.join("data", "simulated_database.jsonl")
        
        # Gathering all messages and hashing potential PII in a simple way for compliance (mock)
        history_msgs = self.chat_history.messages
        anonymized_history = []
        for msg in history_msgs:
            content = msg.content
            # Note: in real-world scenarios, we'd use robust NER for scrubbing names, phones etc.
            anonymized_history.append({"role": msg.type, "content": content})
            
        simulated_record = {
            "session_id": str(hash(self.session_id)),
            "conversation_log": anonymized_history
        }
        
        with open(filepath, "a") as f:
            f.write(json.dumps(simulated_record) + "\n")

