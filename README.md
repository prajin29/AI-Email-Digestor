# 📧 AI Email Digestor

An AI-powered tool that connects to your Gmail inbox, fetches the latest emails, and generates a concise daily digest using **Cohere AI**.

---

## 🚀 Features

* 🔑 Secure Gmail OAuth authentication
* 📬 Fetches latest emails from Gmail
* 🤖 Summarizes emails into short, clear digests using Cohere’s Chat API
* 📊 Outputs digest in terminal and can send it as an email report
* 🛡️ Keeps credentials safe using `.env`

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-email-digestor.git
cd ai-email-digestor
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Google API

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable **Gmail API**.
3. Create **OAuth Client ID credentials**.
4. Download `credentials.json` and place it inside the project folder.

### 5. Create `.env`

```ini
COHERE_API_KEY=your_cohere_api_key_here
SENDER_EMAIL=your_gmail@gmail.com
RECEIVER_EMAIL=recipient@gmail.com
APP_PASSWORD=your_app_password   # Generate from Gmail App Passwords
```

---

## ▶️ Run the Project

```bash
python digestor.py
```

---

## 📧 Sending Digest as Email

The script can also send the generated digest to your email inbox. Make sure `SENDER_EMAIL`, `RECEIVER_EMAIL`, and `APP_PASSWORD` are set in `.env`.

---

## 📌 Example Output

```
AI Email Digest:

1. Google account security alert...
2. LeetCode weekly digest highlights new feature...
3. Coursera promotes Content Creation Certificate...
4. Tata CLiQ announces 10/10 Sale...
```

