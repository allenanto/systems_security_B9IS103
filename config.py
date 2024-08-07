from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET="SECRET"
    DATABASE_NAME="Chatapp"
    MONGODB_HOST="mongodb+srv://allenantony26:allenanto@cluster0.anlxuzy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    MAIL_SERVER='smtp.example.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')