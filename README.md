🎙️ Tung Tung Tung Sahur – AI Voice Assistant 🚀

A Python-based voice assistant that understands natural speech and performs real-world tasks like searching Wikipedia, opening apps/websites, sending emails, searching local files, and reading documents aloud — built with modular, extensible design ideal for STEP-level coding standards.


---

✨ Key Features

🎤 Voice Command Recognition via speech_recognition

🗣️ Text-to-Speech feedback using pyttsx3

📚 Wikipedia Integration – Summarized results via speech

🌐 Smart Web Launcher – YouTube, Google, Stack Overflow

🎵 Local Music Player – Plays from your music folder

📧 Secure Email Sender

Sends voice-generated emails using Gmail’s SMTP

Uses Google App Passwords for security


🕒 Time Reporter – Tells current time via voice

💬 Command History Tracker – Saved to JSON for reuse

📁 File System Search

Search local files by keyword

Indexed with os.walk


📖 Text File Reader

Reads .txt and .md files aloud via voice


🧠 Modular Code Structure – Easy to expand (AI features, GUI, contacts, etc.)



---

💻 Setup Instructions

✅ Prerequisites

Python 3.8+

Gmail App Password setup (if using email feature)
👉 Set up Gmail App Password


🔧 Install Dependencies

pip install pyttsx3 speechRecognition wikipedia


---

▶ How to Run

python ai.py

Say commands like:

"Search Wikipedia for Python"

"Play music"

"Email to someone@gmail.com"

"Search file"

"Read file"

"What’s the time?"

"Exit"



---

🛡 Security Notes

App passwords used for email (never store raw Gmail credentials)

All commands stored in a local command_history.json file



---

🌱 Future Enhancements

🌐 Web scraping support

🔐 Voice authentication

🌍 Multi-language support

🧠 AI-based contextual Q&A (ChatGPT or LLMs)

🖥 GUI version (Tkinter or PyQt)



---

📁 Folder Structure

📂 Project/
├── ai.py                  # Main assistant script
├── command_history.json   # Stores recent commands
├── README.md


---

📜 License

MIT – Free to use and modify.
