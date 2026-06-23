# 🤖 AI Agent App

A modern AI-powered assistant built with **Streamlit**, **Ollama**, and **Python** that can answer general questions, provide weather updates, and fetch real-time stock market information.

# 🚀 Features

### 🤖 AI Chat Assistant
* Powered by Ollama local LLMs
* Supports Qwen3 and Llama models
* Natural language conversations

### 🌦 Weather Information
* Real-time weather data
* City-based weather search
* Fast response using wttr.in

### 📈 Stock Market Information
* Real-time stock prices
* Company name to ticker conversion
* Supports popular companies:
  * Tesla
  * Apple
  * Microsoft
  * Google
  * Amazon
  * Nvidia
  * Meta
  * IBM
  * Netflix

### 🎨 Modern UI
* Vibrant gradient design
* Glassmorphism effects
* Responsive layout
* Dark theme

### 🧠 Agent Reasoning
* Displays internal reasoning process
* Shows tool usage
* Improves transparency


# 🛠 Tech Stack

| Technology | Purpose               |
| ---------- | --------------------- |
| Python     | Backend Logic         |
| Streamlit  | Web Interface         |
| Ollama     | Local LLM Runtime     |
| OpenAI SDK | Ollama Integration    |
| Requests   | API Requests          |
| yFinance   | Stock Data            |
| dotenv     | Environment Variables |

# 📂 Project Structure

```text
ai-agent-app/
│
├── app.py
├── agent.py
├── requirements.txt
├── .gitignore
├── README.md
├── .env
│
├── assets/
│   ├── screenshot.png
│   └── logo.png
│
├── __pycache__/
└── venv/

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/saicharan393/AI-AGENT

cd ai-agent-app

## Create Virtual Environment
### Windows

```bash
python -m venv venv
venv\Scripts\activate
```
### Linux / Mac
python3 -m venv venv
source venv/bin/activate


## Install Dependencies

pip install -r requirements.txt

# 🦙 Install Ollama
Download Ollama:
https://ollama.com
Verify installation:
          ollama --version

# 📥 Download Model
## Qwen 2.5-coder:14b

ollama pull qwen2.5-coder:14b

Recommended for this project.

### Alternative

```bash
ollama pull ollama2.5-coder:14b
```

# ▶️ Start Ollama

```bash
ollama serve
```

Keep this terminal running.


# 🚀 Run Application

```bash
streamlit run app.py
```

Application will be available at:

http://localhost:8501
---

# 💬 Example Queries

## Weather

```text
Weather in Hyderabad

Weather in London

Current weather in New York
```

---

## Stocks

```text
What is stock price of Tesla?

Apple stock price

Current stock price of Nvidia

IBM share price
```

# 📈 Supported Stocks

| Company   | Symbol |
| --------- | ------ |
| Tesla     | TSLA   |
| Apple     | AAPL   |
| Microsoft | MSFT   |
| Google    | GOOGL  |
| Amazon    | AMZN   |
| Nvidia    | NVDA   |
| Meta      | META   |
| IBM       | IBM    |
| Netflix   | NFLX   |

---

# 🔒 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_key_if_using_groq
```

If using Ollama only, no API key is required.

---

# 🎨 UI Features

* Modern gradient background
* Vibrant colors
* Glassmorphism cards
* Responsive design
* Animated chat interface
* Sidebar navigation
* Agent reasoning panel

---


# 🔮 Future Improvements

* Voice Assistant
* PDF Chat
* Image Analysis
* Multi-Agent Architecture
* News Search Tool
* Cryptocurrency Prices
* Database Integration
* Authentication System
* User Profiles
* Chat History Storage


# 🐛 Known Issues

* Weather API depends on wttr.in availability.
* Some stock information may vary depending on market hours.
* Ollama must be running before starting the application.

---


# 👨‍💻 Author

**saicharan**

GitHub:
https://github.com/saicharan393

---

Made with ❤️ using Python, Streamlit, and Ollama.
