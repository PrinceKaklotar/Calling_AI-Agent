# PR Gym Voice Agent
A local, terminal-based voice conversational AI assistant for PR Gym, built using LangChain. 
This application processes spoken queries via a microphone (when enabled), processes them to provide general gym information using a Retrieval-Augmented Generation (RAG) pipeline, and can execute booking-related actions via tool-calling. It reads responses aloud using text-to-speech.
**⚠️ IMPORTANT NOTE:** This is currently a **local application**. It operates entirely on your computer through the terminal and local audio devices. **In a future update, this agent will be upgraded to call users directly on their mobile phones and hold real-time voice conversations as a fully functioning telephony AI.**
## Key Features
- **Voice Input/Output:** Transcribes user speech to text using Google's speech recognition and speaks responses out loud using a local TTS engine (`pyttsx3`).
- **RAG-based Q&A:** Answers general questions about the gym (facilities, timings, pricing, etc.) using a local knowledge base of Markdown files, embedded via HuggingFace `sentence-transformers` and searched via a FAISS vector store.
- **Tool-based Actions:** Uses LangChain's `bind_tools` to execute gym-related operations such as checking trial slot availability, booking a free trial, and cancelling an existing booking.
- **Conversation Memory:** Maintains an ongoing chat history so the assistant remembers context during the interaction.
## Tech Stack
- **Python Framework:** LangChain (`langchain-core`, `langchain-community`, `langchain-huggingface`, `langchain-text-splitters`)
- **LLM / Inference:** HuggingFace Serverless Inference API (`ChatHuggingFace`, `HuggingFaceEndpoint`)
- **Embeddings:** HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Store:** FAISS
- **Speech-to-Text:** `SpeechRecognition`
- **Text-to-Speech:** `pyttsx3`
- **Environment Management:** `python-dotenv`
## Project Structure
```text
.
├── .env                  # Environment variables (API keys and model configs)
├── calling_agent.py      # Main entry point containing voice I/O, RAG chain, and tool execution logic
├── database/
│   ├── database.py       # Functions interacting with the SQLite database
│   └── gym.db            # SQLite database file storing trial bookings
├── knowledge_base/       # Markdown files containing PR Gym's business data for the RAG pipeline
│   ├── business_profile.md
│   ├── cancellation_policy.md
│   ├── facilities.md
│   ├── faq.md
│   ├── membership_plans.md
│   ├── pricing.md
│   ├── timings.md
│   ├── trainers.md
│   └── trial_policy.md
├── tools/
│   └── gym_tools.py      # LangChain @tool definitions (availability check, add booking, cancel booking)
└── VectorStore/          # Automatically generated local FAISS vector store database
```
## How It Works
1. **Listen & Transcribe:** The `speech_recognition` library listens to your microphone and converts the audio into text using Google's STT service.
2. **Retrieve Context (RAG):** The system takes the transcribed text and fetches the top 3 most relevant chunks from the FAISS vector database (created from `knowledge_base/*.md`).
3. **Decide Action:** The LLM receives the user's prompt, the retrieved context, and the conversation history. It decides whether to formulate a general answer or invoke a tool (e.g., booking a trial).
4. **Execute Tools (If Needed):** If the LLM requests a tool call, the appropriate function in `tools/gym_tools.py` runs, queries the SQLite database, and returns the result to the LLM.
5. **Respond & Speak:** The LLM formulates the final textual response, which is printed to the terminal and spoken aloud via the `pyttsx3` text-to-speech engine.
## Setup & Installation
1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
2. **Install dependencies:**
   There is currently no `requirements.txt` file in the project. You can install the required packages manually:
   ```bash
   pip install langchain langchain-core langchain-community langchain-huggingface langchain-text-splitters python-dotenv faiss-cpu pyttsx3 SpeechRecognition sentence-transformers
   ```
3. **System-level dependencies:**
   - **PyAudio:** The `SpeechRecognition` library requires PyAudio for microphone access. You may need to install it based on your OS:
     - **Windows:** `pip install PyAudio`
     - **macOS:** `brew install portaudio` then `pip install PyAudio`
     - **Linux:** `sudo apt-get install python3-pyaudio portaudio19-dev` then `pip install PyAudio`
## Environment Variables
Create a `.env` file in the root directory. The following variables were found to be referenced in the project:
- `HUGGINGFACEHUB_API_TOKEN` - Your HuggingFace API key required for accessing inference endpoints and downloading embedding models.
- `MODEL_NAME` - The HuggingFace repository ID of the LLM to use (e.g., `deepseek-ai/DeepSeek-V4-Pro-0813`).
*(Optional/Unused in main agent yet but present in .env)*
- `ELEVENLABS_API_KEY`
- `FISH_AUDIO_API`
- `SARVAM_API_KEY`
## How to Run
Run the main agent script from the project root:
```bash
python calling_agent.py
```
Wait a moment while the system loads the local vector store (or creates it if running for the first time) and initializes the model. When prompted with `💬 Tell me your doubt here:`, you can type your query in the terminal. *(Note: To use voice input, you must uncomment the `litsen_to_user()` line in `calling_agent.py`)*. Type `quit`, `exit`, or `bye` to stop the agent.
## Known Limitations
- **No Real Telephony (Yet):** The app currently does not answer or make real phone calls. (This is planned for a future update).
- **Internet Dependency:** Relies on an active internet connection for Google Speech Recognition and HuggingFace API endpoints.
- **Single Language:** The agent primarily operates in English and relies on Google STT which defaults to the system's language without explicit configuration.
- **Microphone Required:** For voice inputs, the app requires a working microphone connected to the machine.
## Future Improvements
- **Real Mobile Phone Calls (Upcoming):** The core vision for the future is to upgrade this agent so it can actively call you on your mobile phone and hold a real-time conversation. This will involve integrating with telephony systems to bridge the AI with real cellular networks.
- **Voice Upgrades:** Replace local `pyttsx3` with higher quality TTS providers (like ElevenLabs or Fish Audio, which already have keys mapped in `.env`).
- **Multilingual Support:** Update the system prompt, STT recognizer, and TTS engine to handle regional languages seamlessly.
