
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import pickle
import os
import hashlib

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

USERS_FILE = "users.csv"
MODEL_PATH = "best_model.pkl"
ENCODERS_PATH = "encoders.pkl"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> pd.DataFrame:
    if os.path.exists(USERS_FILE):
        try:
            return pd.read_csv(USERS_FILE)
        except Exception:
            return pd.DataFrame(columns=["username", "password"])
    return pd.DataFrame(columns=["username", "password"])


def save_users(df: pd.DataFrame) -> None:
    df.to_csv(USERS_FILE, index=False)


def register_user(username: str, password: str) -> bool:
    users = load_users()
    if username in users["username"].values:
        return False
    hashed = hash_password(password)
    users = pd.concat(
        [users, pd.DataFrame([[username, hashed]], columns=["username", "password"])],
        ignore_index=True,
    )
    save_users(users)
    return True


def login_user(username: str, password: str) -> bool:
    users = load_users()
    hashed = hash_password(password)
    match = users[(users["username"] == username) & (users["password"] == hashed)]
    return not match.empty


try:
    model = pickle.load(open(MODEL_PATH, "rb"))
    encoders = pickle.load(open(ENCODERS_PATH, "rb"))
except Exception as e:
    model = None
    encoders = None
    print(f"Error loading model or encoders: {e}")


def yes_no_to_binary(value: str) -> int:
    return 1 if value.lower() == "yes" else 0


@app.route("/")
def index():
    return "Autism Screening App is running successfully"



@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if login_user(username, password):
            session["username"] = username
            return redirect(url_for("personal_info"))
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    success = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            error = "Please fill in all fields."
        elif not register_user(username, password):
            error = "Username already exists. Please choose another."
        else:
            success = "Registration successful. Please login."
    return render_template("register.html", error=error, success=success)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/personal-info", methods=["GET", "POST"])
def personal_info():
    if "username" not in session:
        return redirect(url_for("login"))

    if encoders is None:
        return "Model files missing. Please place 'best_model.pkl' and 'encoders.pkl' next to app.py."

    if request.method == "POST":
        personal = {
            "age": request.form.get("age", "").strip(),
            "gender": request.form.get("gender"),
            "ethnicity": request.form.get("ethnicity"),
            "jaundice": request.form.get("jaundice"),
            "austim": request.form.get("austim"),
            "contry_of_res": request.form.get("contry_of_res"),
            "used_app_before": request.form.get("used_app_before"),
            "relation": request.form.get("relation"),
        }
        session["personal_info"] = personal
        return redirect(url_for("predict"))

    return render_template(
        "personal_info.html",
        gender_options=encoders["gender"].classes_ if encoders else [],
        ethnicity_options=encoders["ethnicity"].classes_ if encoders else [],
        jaundice_options=encoders["jaundice"].classes_ if encoders else [],
        austim_options=encoders["austim"].classes_ if encoders else [],
        country_options=encoders["contry_of_res"].classes_ if encoders else [],
        used_app_options=encoders["used_app_before"].classes_ if encoders else [],
        relation_options=encoders["relation"].classes_ if encoders else [],
    )


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "username" not in session:
        return redirect(url_for("login"))

    if encoders is None or model is None:
        return "Model files missing. Please place 'best_model.pkl' and 'encoders.pkl' next to app.py."

    personal = session.get("personal_info")
    if not personal:
        return redirect(url_for("personal_info"))

    prediction_label = None
    probability = None

    if request.method == "POST":
        behaviors = {}
        for i in range(1, 11):
            key = f"A{i}_Score"
            val = request.form.get(key, "no")
            behaviors[key] = yes_no_to_binary(val)

        try:
            age_val = float(personal.get("age", 0))
        except ValueError:
            age_val = 0

        try:
            score_val = float(request.form.get("result", 5))
        except ValueError:
            score_val = 5

        input_data = {
            **behaviors,
            "age": age_val,
            "gender": encoders["gender"].transform([personal["gender"]])[0],
            "ethnicity": encoders["ethnicity"].transform([personal["ethnicity"]])[0],
            "jaundice": encoders["jaundice"].transform([personal["jaundice"]])[0],
            "austim": encoders["austim"].transform([personal["austim"]])[0],
            "contry_of_res": encoders["contry_of_res"].transform([personal["contry_of_res"]])[0],
            "used_app_before": encoders["used_app_before"].transform([personal["used_app_before"]])[0],
            "result": score_val,
            "relation": encoders["relation"].transform([personal["relation"]])[0],
        }

        df_input = pd.DataFrame([input_data])
        pred = model.predict(df_input)[0]
        proba = model.predict_proba(df_input)[0][1] if hasattr(model, "predict_proba") else None

        if int(pred) == 1:
            prediction_label = "Yes – high likelihood of Autism Spectrum Disorder (screening result)"
        else:
            prediction_label = "No – low likelihood of Autism Spectrum Disorder (screening result)"
        probability = round(float(proba) * 100, 1) if proba is not None else None

    return render_template(
        "predict.html",
        prediction=prediction_label,
        confidence=probability,
    )


@app.route("/result")
def result():
    return redirect(url_for("predict"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



