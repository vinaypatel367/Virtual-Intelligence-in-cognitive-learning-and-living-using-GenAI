# 🧠 Generative AI Smart Learning & Living System

![App Preview](capture.png)

## 🌍 Overview
This project integrates **Generative AI (GenAI)** to enhance both learning and smart living experiences. It combines Natural Language Processing, automation, and machine learning to deliver personalized, intelligent, and adaptive systems.

- In **learning environments**, it provides customized content and interactive AI tutoring.
- In **smart living**, it automates daily tasks, optimizes energy consumption, and integrates security and IoT systems.

The system adapts to user behavior using advanced AI models, enabling seamless interaction and continuous improvement over time.

---

## ⚙️ Features
- 🤖 Conversational AI Assistant (ChatGPT + Cohere APIs)
- 🏠 Home Automation & Smart Device Control
- 🔐 Security & Surveillance Integration
- 🗣️ Text-to-Speech (TTS) and Audio Processing
- 🧩 Auto-generated PowerPoint Presentations
- 🌐 Web-based Interface (HTML-based UI)

---

## 💻 Tech Stack
**Languages:** Python, HTML, CSS, JavaScript  
**Frameworks & Libraries:** Flask, TensorFlow, PyTorch, scikit-learn, pyttsx3, dotenv  
**APIs & AI Models:** OpenAI API, Cohere API  
**Tools & Platforms:** VS Code, Netlify, GitHub, Jupyter Notebook  
**Databases (optional):** SQLite / JSON-based storage

---

## 🧩 Folder Structure
```
8k/
├── main.py
├── .env
├── ChatLog.json
├── Backend/
│   ├── Automation.py
│   ├── ChatGpt.py
│   ├── TTS.py
│   ├── HomeAutomation.py
│   ├── Security.py
│   └── ...
├── web/
│   ├── home.html
│   ├── settings.html
│   └── spider.html
├── presentations/
│   ├── bright_modern.pptx
│   ├── dark_modern.pptx
│   └── simple.pptx
└── assets/
    └── capture.png
```

---

## 🧰 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/GenAI-SmartLiving.git
cd GenAI-SmartLiving
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
Make sure you have **Python 3.10+** installed. Then run:
```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, use:
```bash
pip install flask openai cohere tensorflow torch scikit-learn pyttsx3 python-dotenv
```

### 4️⃣ Set Environment Variables
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key
```

### 5️⃣ Run the Project
```bash
python main.py
```

### 6️⃣ Access the Web Interface
Open your browser and visit:
```
http://localhost:5000
```

---

## 🖼️ Screenshots
| Home | Settings | Smart Dashboard |
|------|-----------|----------------|
| ![Home](web/home.png) | ![Settings](web/settings.png) | ![Dashboard](capture.png) |

---

## 🔮 Future Enhancements
- Voice command integration
- Advanced emotion-based learning
- IoT sensor data analytics dashboard
- Cloud synchronization

---

## 🧑‍💻 Contributors
- **[Vinay Sanepara](https://vinaysanepara.netlify.app/)** – AI & Full-Stack Developer  
- **[Khushi Patel](https://fluffy-gecko-402a2e.netlify.app/)** – AI & Data Science Engineer

---

## 📜 License
This project is licensed under the **MIT License**.
