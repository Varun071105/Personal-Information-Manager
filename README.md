🧠 Personal Information Manager

A powerful yet lightweight Personal Information Manager (PIM) built with Python 🐍 to help you organize your tasks, notes, contacts, and important info — all in one place!


---

🚀 Features

✅ Add, view, update, and delete personal data
✅ Store and retrieve notes, contacts, passwords, or reminders
✅ 📂 Simple JSON-based file storage (no external DB required!)
✅ 🕒 Track history of saved entries
✅ 📜 Command-line interface for quick access
✅ 🔐 Local and offline – your data stays on your device


---

📁 Project Structure

📦 Personal-Information-Manager
├── main.py               # Main application file
├── data.json             # Stores all your personal information
├── utils.py              # Helper functions (load/save data)


---

🛠️ Tech Stack

Python 3.x 🐍

JSON for data persistence

CLI interface (console-based)

Easily extendable to GUI or web in the future!



---

💡 How It Works

# Load existing data from JSON
def load_data(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save updated data
def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

You interact with the manager using a menu-based console. Just follow the prompts to manage your info!


---

🔄 Future Upgrades (Coming Soon 💥)

[ ] Add AI-powered search and voice input

[ ] Integrate with Google Calendar or reminders

[ ] Add encryption for sensitive info

[ ] Build a GUI version using Tkinter or PyQt

[ ] Sync across devices via the cloud ☁️



---

🤖 Use Cases

Keep track of college assignments, passwords, and contacts

Store mini journal entries or notes

Save important links, checklists, or todo items

Great for students, devs, or anyone who loves staying organized!



---

🧑‍💻 Author
Arun Singh 
💼 Aspiring SWE | Passionate about AI/ML and productivity tools
📌 GitHub Profile


---

🌟 Star This Repo

If you find this useful or want to follow the journey, please ⭐ this repo. It helps a lot!