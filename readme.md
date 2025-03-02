# 📝 AI-Based Document Classification System

This project is a **Flask-based web application** that allows users to:
✅ **Upload multiple PDF documents**  
✅ **Classify documents into predefined categories**  
✅ **Detect sensitive information (Confidential, Highly Confidential, Non-Sensitive)**  
✅ **Compute confidence scores (50-100%)**  
✅ **Generate a classification bar graph**  
✅ **Choose between different AI models (ChatGPT, Local ChatGPT, Local DeepSeek)**  

---

## 🚀 **1. Installation Guide**
Follow these steps to set up and run the project on your local machine.

### **1️⃣ Prerequisites**
Before running the project, ensure you have:
- **Python 3.x** installed
- **pip** (Python Package Manager)
- **Virtual Environment** (recommended)
- **OpenAI API Key** (for ChatGPT model)

---

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/KaushalRai12/Document-Classification-AI.git
cd Document-Classification-AI

3️⃣ Create & Activate a Virtual Environment

Windows: 

python -m venv env
env\Scripts\activate

MAC:
python3 -m venv env
source env/bin/activate


4️⃣ Install Required Dependencies


pip install -r requirements.txt


5️⃣ Set Up OpenAI API Key
Create a .env file in the project root and add:
OPENAI_API_KEY=your_api_key_here

6️⃣ Run the Flask Application
python app.py

Now, open your browser and go to:
http://127.0.0.1:5000/

🚀 Deploying Your Flask App to Heroku Using Heroku CLI

Heroku CLI is a command-line tool that allows you to manage your Heroku apps from the terminal.

📌 Step 1: Install Heroku CLI
If you haven’t already installed Heroku CLI, install it using:

Windows
Download and install from: Heroku CLI for Windows

macOS/Linux
Run the following command:

bash
Copy
Edit
curl https://cli-assets.heroku.com/install.sh | sh
📌 Step 2: Login to Heroku
After installation, login using:

bash
Copy
Edit
heroku login
This will open a browser and ask you to authenticate.

📌 Step 3: Create a New Heroku App
Run the following command to create a new Heroku app:

bash
Copy
Edit
heroku create your-heroku-app-name
Replace your-heroku-app-name with a unique name (e.g., doc-classify-ai).

📌 Step 4: Add a Procfile (For Deployment)
Inside your project directory, create a Procfile (without extension) and add:

makefile
Copy
Edit
web: gunicorn app:app
This tells Heroku to run your Flask app using Gunicorn, which is recommended for production.

📌 Step 5: Add Heroku as a Git Remote
Run:

bash
Copy
Edit
git remote add heroku https://git.heroku.com/your-heroku-app-name.git
Replace your-heroku-app-name with the actual app name.

📌 Step 6: Deploy Your App to Heroku
Run the following commands:

bash
Copy
Edit
git add .
git commit -m "Deploy Flask app to Heroku"
git push heroku main
This will:

Push your code to Heroku.
Install dependencies from requirements.txt.
Start the Flask app using gunicorn.
📌 Step 7: Set Up Environment Variables on Heroku
If you're using OpenAI API Key, run:

bash
Copy
Edit
heroku config:set OPENAI_API_KEY=your_api_key_here
To check environment variables:

bash
Copy
Edit
heroku config
📌 Step 8: Open Your Deployed App
Once deployment is successful, open your app in the browser:

bash
Copy
Edit
heroku open
or manually visit:

arduino
Copy
Edit
https://your-heroku-app-name.herokuapp.com/
📌 Step 9: Automate Deployment with GitHub Actions (CI/CD)
To enable automatic deployment when you push code to GitHub, set up GitHub Actions:

Create a new workflow file:
bash
Copy
Edit
📂 .github/workflows/deploy.yml
Add the following content to deploy.yml:
yaml
Copy
Edit
name: Deploy Flask App to Heroku

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Install Heroku CLI
        run: curl https://cli-assets.heroku.com/install.sh | sh

      - name: Deploy to Heroku
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
        run: |
          echo $HEROKU_API_KEY | heroku auth:token
          heroku git:remote -a your-heroku-app-name
          git push heroku main
📌 Step 10: Add Heroku API Key to GitHub Secrets
Go to GitHub Repo → Settings → Secrets and Variables → Actions
Click "New Repository Secret" and add:

Secret Name	Value (Replace with your credentials)
HEROKU_API_KEY	Run heroku auth:token to get it
📌 Step 11: Push Code & Verify Deployment
After adding the GitHub Action:

bash
Copy
Edit
git add .
git commit -m "Enable GitHub Actions CI/CD for Heroku"
git push origin main
Go to GitHub → Actions Tab and verify if the workflow runs successfully.
If everything is correct, your app will automatically deploy to Heroku on every commit! 🎉

🚀 Summary
✅ Installed Heroku CLI
✅ Created a Heroku App
✅ Configured Gunicorn via Procfile
✅ Manually deployed the Flask app to Heroku
✅ Set up GitHub Actions (CI/CD) for auto-deployment

Now, every time you push to GitHub, your app will automatically deploy to Heroku! 🚀🔥