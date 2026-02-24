# TalentBot: TalentScout AI Hiring Assistant

An intelligent, multi-persona AI chatbot designed to automate the initial HR screening process for technology candidates. Built with **Streamlit**, **LangChain**, and **Ollama**, it seamlessly handles conversational data gathering, dynamic technical assessments, and real-time sentiment tracking.

---

## Project Overview
The **TalentBot: TalentScout AI Hiring Assistant** is an intelligent chatbot designed to automate the initial screening process for candidates seeking technology placements. As "TalentBot", the hiring assistant gracefully guides candidates through a conversational flow to gather essential details (Name, Contact, Experience, Desired Position, Location, and Tech Stack). Once gathered, the assistant dynamically generates 3-5 technical questions tailored explicitly to the candidate's reported Tech Stack to assess their proficiency.

### Key Features

<img width="1846" height="1022" alt="image" src="https://github.com/user-attachments/assets/fffa0756-1417-42fd-9c35-2843ccdbd47c" />

- **Dynamic AI Personas:** Choose your interviewer from the main menu:
  - **Lani 🦙:** A balanced and professional Llama assistant.
<img width="1844" height="1022" alt="image" src="https://github.com/user-attachments/assets/ce855ece-c80f-45a3-8d21-19eed434fdcf" />

  - **Malik 👔:** An efficient, straight-to-the-point Google Gemini Hiring Manager.
<img width="1850" height="1023" alt="image" src="https://github.com/user-attachments/assets/b0a33055-69ad-4db0-bdf9-95be7a1021c2" />

  - **Clara 😊:** A warm, chatty, and knowledgeable OpenAI assistant.
<img width="1845" height="1022" alt="image" src="https://github.com/user-attachments/assets/bdd097d1-2983-4b2c-895f-dd487d9ea806" />

- **Strict Conversational Flow:** The AI gathers candidate details *one by one* to prevent overwhelming the user, retaining organic conversational elements via memory buffers.
<img width="1842" height="1022" alt="image" src="https://github.com/user-attachments/assets/127820e9-4bc7-40d5-9251-455ed66f3d61" />

- **Dynamic Technical Assessment:** Generates relevant technical questions based *only* on the candidate's reported tech stack.
<img width="1839" height="1019" alt="image" src="https://github.com/user-attachments/assets/3799807a-2dbf-46eb-bba8-d07e3c4f4fda" />

- **Graceful Failovers:** Natively supports routing API requests to Google Gemini, OpenAI, or a purely offline local Ollama instance.
- **Privacy & Anonymization:** Simulates GDPR compliance by automatically one-way hashing Candidate Session IDs and dumping the conversation safely to a `.jsonl` file when the user exits the chat.

---

## Installation & Setup

### Prerequisites
- **Python 3.9+**
- **[Ollama](https://ollama.com/)** (to run the Local Llama 3.2 models offline).
- **OpenAI API Key** (Optional, for the Clara persona).
- **Google Gemini API Key** (Optional, for the Malik persona).

### Running Locally
1. **Clone the repository:**
   ```bash
   git clone https://github.com/rananjaychauhan93/talent-scout-hiring-assistant.git
   cd talent-scout-hiring-assistant
   ```

2. **Set up a Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

3. **Set up API Keys (Optional but Recommended):**
   Copy the example environment file and add your keys:
   ```bash
   cp .env.example .env
   ```
   *Edit `.env` to include `OPENAI_API_KEY` and `GEMINI_API_KEY`.*

4. **Pull the Local Offline Models:**
   Ensure Ollama is running on your machine, then pull the necessary models:
   ```bash
   ollama pull llama3.2
   ollama pull mxbai-embed-large:latest
   ```

5. **Launch the Application:**
   ```bash
   streamlit run app.py
   ```
   *The application will launch in your default browser at `http://localhost:8501`.*

### Usage Guide
To launch the chatbot interface, simply run the following command in your terminal:
```bash
streamlit run app.py
```
This will open up a local web interface in your default browser (usually at `http://localhost:8501`).

---

## Technical Architecture

- **Frontend Navigation:** `Streamlit` provides the reactive UI. We removed explicit API sidebars for security, leveraging a pristine 3-button launcher to lock the user's chosen Persona securely into the session state.
- **Backend Orchestration:** `LangChain` manages the inference routing. The `HiringAssistantBackend` class dynamically maps to `ChatOllama`, `ChatOpenAI`, or `ChatGoogleGenerativeAI` depending on the active State.
- **Contextual Memory:** `RunnableWithMessageHistory` seamlessly ties the LLM logic to a `ChatMessageHistory` buffer. This prevents hallucinations and stops the AI from asking for details it has already collected.
- **Prompt Engineering:** Strict Persona logic loops were designed using mathematical enumerations (1 to 7) within the `SYSTEM_PROMPT`. This guarantees the LLM checks internal state requirements before pivoting to Technical Generation.

---

## Challenges & Solutions
1.
   - **Challenge:** Local LLMs (llama3) sometimes hallucinate states (e.g., asking for emails multiple times even if initially provided) due to smaller context windows compared to colossal frontier models.
   - **Solution:** Implemented `ConversationBufferMemory` combined with strict system instructions explicitly stating: *"Maintain context of the conversation. If you already have some information, don't ask for it again."*
3.
   - **Challenge:** Running offline inferences efficiently under restricted hardware can cause runtime timeouts, disrupting end-user evaluations.
   - **Solution:** Configured `with_fallbacks` leveraging OpenAI (`gpt-4o-mini`) automatically catching inference or connection timeouts and bouncing them to a high-speed cloud fallback avoiding disruptions.
4.
   - **Challenge:** Securing Personal Identifiable Information (PII) to comply with basic GDPR/Data Privacy protocols.
   - **Solution:** Implemented automatic one-way hashing of critical identifiers locally upon conversation termination when saving the interactions (`simulated_database.jsonl`).

---

## Author Details

**Rananjay Singh Chauhan**
- **Email:** rananjaychauhan93@gmail.com | rjchauhanbackup@gmail.com
- **Role:** Software & AI Developer

---
*Developed under the [MIT License](LICENSE).*

*If you find this repository useful, feel free to fork it and leave a star!* ⭐




