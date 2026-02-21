# 🤖 AI Code Tutor

AI-powered coding tutor built with Flask and HuggingFace.

AI Code Tutor is a web-based application that helps programmers understand and improve their code using AI.

It provides step-by-step explanations, improvements, optimizations, and security analysis for code written in multiple programming languages.

---

## 🚀 Features

✅ Explain code step-by-step  
✅ Improve code quality  
✅ Optimize performance  
✅ Detect security issues  
✅ Difficulty level detection  
✅ Multiple AI models  
✅ Code history tracking  
✅ Dark / Light theme  
✅ Copy code easily

---

## 🧠 Supported Languages

- Python
- JavaScript
- C
- Java

---

## 🤖 AI Models

The application supports multiple AI models:

- Qwen (Fast)
- Llama
- Mistral
- Falcon

---

## 🏗 Project Structure

ai-code-tutor/
│
├── routes/
│ ├── auth_routes.py
│ ├── editor_routes.py
│
├── services/
│ ├── ai_service.py
│ ├── difficulty_service.py
│ ├── formatter_service.py
│ ├── prompt_service.py
│
├── templates/
│ ├── editor.html
│ ├── login.html
│ ├── register.html
│ ├── history.html
│
├── static/
│ ├── style.css
│
├── app.py
├── config.py
├── database.py
├── requirements.txt
├── .env


---

## ⚙️ Installation

### 1️⃣ Clone Repository



git clone https://github.com/prabhhhuu/ai-code-tutor.git

cd ai-code-tutor


---

### 2️⃣ Install Requirements



pip install -r requirements.txt


---

### 3️⃣ Create .env File

Create a file called `.env`

Example:



HF_TOKEN=your_huggingface_token
SECRET_KEY=your_secret_key


Get token from:

https://huggingface.co/settings/tokens

---

### 4️⃣ Run Application



python app.py


Open browser:



http://127.0.0.1:5000


---

## 🗄 Database

SQLite database is used.

Tables:

### Users

- id
- username
- email
- password_hash

### Code History

- id
- user_id
- code
- language
- mode
- result
- difficulty
- created_at

---

## 🔐 Security

- Password hashing
- Environment variables
- Session authentication

---

## 🛠 Technologies Used

- Python
- Flask
- SQLite
- HuggingFace API
- HTML
- CSS
- JavaScript

---

## 📊 Difficulty Detection

Code difficulty is automatically classified as:

- Beginner
- Intermediate
- Advanced

---

## 🧑‍💻 Author

Prabhu Raja

---

## 📜 License

This project is for educational purposes.
