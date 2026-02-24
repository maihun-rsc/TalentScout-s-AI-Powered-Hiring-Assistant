# TalentScout Hiring Assistant 🤖

## 📋 Project Overview
The **TalentScout Hiring Assistant** is an intelligent chatbot designed to automate the initial screening process for candidates seeking technology placements. As "TalentBot", it gracefully guides candidates through a conversational flow to gather essential details (Name, Contact, Experience, Desired Position, Location, and Tech Stack). Once gathered, the assistant dynamically generates 3-5 technical questions tailored explicitly to the candidate's reported robust Tech Stack to assess proficiency.

## 🚀 Installation Instructions

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.com/) (to run the Local Llama 3.2 model offline).
- An OpenAI API Key (Optional) for fallback operations.

### Setup
1. **Clone the project** or extract it into your desired directory.
2. **Navigate** into the project directory:
   ```bash
   cd talent_scout
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up Secrets:**
   Rename `.env.example` to `.env` and fill in your OPENAI_API_KEY if you plan to use the fallback capabilities.
   ```bash
   cp .env.example .env
   ```
5. **Start Local Models via Ollama (Important for default behavior):**
   ```bash
   ollama run llama3.2
   ollama pull mxbai-embed-large:latest
   ```

## 🎮 Usage Guide
To launch the chatbot interface, simply run the following command in your terminal:
```bash
streamlit run app.py
```
This will open up a local web interface in your default browser (usually at `http://localhost:8501`).

1. **Settings**: Use the sidebar to toggle "OpenAI Fallback" if your local model fails to generate responses.
2. **Chatting**: Say "Hello" or respond to the initial greeting to begin the sequence. The bot will automatically orchestrate the data collection and pose relevant technical questions.
3. **End Conversation**: Say "exit", "quit", "bye", or "stop" to conclude the interview securely. The application will trigger an automated anonymization pipeline that saves your record locally.

## 🛠️ Technical Details
- **Frontend**: `Streamlit` allows for a reactive, intuitive UI with built-in state management customized slightly via HTML/CSS injections for improved conversational UX. 
- **Backend LLM Management**: `LangChain` dynamically maps input parameters, manages conversational histories (`ChatMessageHistory`), and supports sophisticated prompt engineering. 
- **Models**:
  - Offline primary model: `llama3.2` hosted via Ollama.
  - Offline primary embeddings: `mxbai-embed-large:latest` hosted via Ollama.
  - Fallback model: `gpt-4o-mini` (via OpenAI APIs) integrated seamlessly using LangChain `.with_fallbacks()` mechanics.
- **Architectural Decisions**: 
  We utilized `RunnableWithMessageHistory` to bind the core conversation logic without relying on explicit step-by-step state graphs. The model behaves autonomously by referencing the `System Prompt` rules, avoiding strict sequential hardcoding, retaining organic conversational elements. Simulated anonymized datasets are captured securely upon detecting the "exit" command.

## ✍️ Prompt Design
The core engine driving the application is strictly enforced via an engineered system prompt.
1. **Persona & Goal Constraints**: Defined the character ("TalentBot") and its persona ("empathetic", "professional"). Restricting the model from answering unrelated general-purpose questions.
2. **Sequential Flow Guardrails**: We employed enumerated lists (1 to 4) mapping out precise life cycles: Information Gathering $\rightarrow$ Condition $\rightarrow$ Technical Testing $\rightarrow$ Graceful Exit. 
3. **Condition Handling**: Emphasizing "Once ALL the above information is gathered" guarantees the model will act as a state-checker. It validates the presence of Name, Location, Stack, etc., acting iteratively. When conditions are entirely met, it logically shifts towards generating 3-5 technical challenges tailored explicitly to the listed technologies.

## ⚠️ Challenges & Solutions
1. **Challenge:** Local LLMs (llama3) sometimes hallucinate states (e.g., asking for emails multiple times even if initially provided) due to smaller context windows compared to colossal frontier models.
   - **Solution:** Implemented `ConversationBufferMemory` combined with strict system instructions explicitly stating: *"Maintain context of the conversation. If you already have some information, don't ask for it again."*
2. **Challenge:** Running offline inferences efficiently under restricted hardware can cause runtime timeouts, disrupting end-user evaluations.
   - **Solution:** Configured `with_fallbacks` leveraging OpenAI (`gpt-4o-mini`) automatically catching inference or connection timeouts and bouncing them to a high-speed cloud fallback avoiding disruptions.
3. **Challenge:** Securing Personal Identifiable Information (PII) to comply with basic GDPR/Data Privacy protocols.
   - **Solution:** Implemented automatic one-way hashing of critical identifiers locally upon conversation termination when saving the interactions (`simulated_database.jsonl`).
