from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
from db import Base, engine, SessionLocal
import os
import models
import PyPDF2
import docx
import json
from ai import analyze_resume


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

Base.metadata.create_all(bind=engine)

#HOME
@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

#------SIGNUP
@app.route("/signup",methods=["GET", "POST"])
def signup():
    db = SessionLocal()
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        existing_user = db.query(models.User).filter_by(email=email).first()
        if existing_user:
            db.close()
            return "User already exists"
        
        user = models.User(email=email, password=password)
        db.add(user)
        db.commit()
        db.close()
        return redirect("/login")
    
    return render_template("signup.html")

#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    db = SessionLocal()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = db.query(models.User).filter_by(email=email, password=password).first()
        
        if user:
            session["user"] = user.email
            db.close()
            return redirect("/dashboard")
        else:
            db.close()
            return "Invalid Credentials"
        
    
    return render_template("login.html")

# Dashboard
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")
    result = None
    
    if request.method == "POST":
        user_goal = request.form.get("role")
        resume_text = request.form.get("resume")
        
        file = request.files.get("file")
        
        #file handling
        if file and file.filename != "":
            filename = file.filename.lower()
            if filename.endswith(".pdf"):
                try:
                    pdf_reader =PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""
                    resume_text = text
                except Exception as e:
                    result = {"error" : f"PDF error: {str(e)}"}
                    
            elif filename.endswith(".docx"):
                try:
                    doc = docx.Document(file)
                    text = ""
                    for para in doc.paragraphs:
                        text += para.text +"\n"
                    resume_text = text
                except Exception as e:
                    result = {"error": f"Docx error: {str(e)}"}
            else:
                result = {"error": "Only PDF and DOCX files are supported."}
        if not resume_text:
            result = {"error": "Please paste your resume or upload a PDF/DOCX file."}
            
        elif not user_goal:
            result = {"error" : "Please enter your target role."}
            
        else:
            try:
                result = analyze_resume(resume_text, user_goal)
                # Save to db
                db = SessionLocal()
                user = db.query(models.User).filter_by(email=session["user"]).first()
                
                report = models.Report(
                    user_id = user.id,
                    resume_text = resume_text,
                    result = json.dumps(result)
                )
                
                db.add(report)
                db.commit()
                db.close()
            except Exception as e:
                result = {"error" : f"Analysis error:{str(e)}"}
    return render_template(
        "dashboard.html",
        user=session["user"],
        result = result
    )
        
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")
    
    db = SessionLocal()
    user = db.query(models.User).filter_by(email=session["user"]).first()
    
    reports = db.query(models.Report).filter_by(user_id = user.id).all()
    
    #convert JSON string > dict
    past_reports =[]
    for r in reports:
        try:
            past_result = json.loads(r.result)
        except:
            past_result = []
        
        past_reports.append({
            "resume":r.resume_text,
            "result":past_result
        })
    db.close()
    return render_template("history.html", reports=past_reports)

#logout route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug= True)