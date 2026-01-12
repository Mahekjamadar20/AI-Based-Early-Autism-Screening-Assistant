# AI-Based Early Autism Screening Assistant

A professional web application for early autism spectrum disorder (ASD) screening using machine learning. The app provides a user-friendly interface with login/registration, personal information collection, behavioral assessment, and an AI chatbot for support.

## Features

- 🔐 **Secure User Authentication** - Login/registration with password hashing
- 📋 **Step-by-Step Screening Flow** - Personal info → Behavioral questions → Results
- 🤖 **AI Chatbot Assistant** - Get answers to common autism-related questions
- 🎨 **Professional UI/UX** - Modern, responsive design with professional logo
- 📊 **ML-Based Prediction** - Uses trained model to provide screening results
- ✅ **Yes/No Results** - Clear, easy-to-understand screening outcomes with confidence scores

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **ML**: scikit-learn (1.6.1)
- **Data**: Pandas, NumPy

## Prerequisites

Before deploying, ensure you have:

1. **Python 3.8+** installed
2. **Required model files**:
   - `best_model.pkl` - Trained ML model
   - `encoders.pkl` - Label encoders for categorical features

## Installation & Deployment

### Option 1: Local Development

1. **Clone or download the project**
   ```bash
   cd autism_app
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify model files exist**
   - Check that `best_model.pkl` and `encoders.pkl` are in the project root
   - If missing, place your trained model files here

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the app**
   - Open your browser and go to: `http://127.0.0.1:5000`

### Option 2: Production Deployment (Windows/Linux)

#### Using Waitress (Recommended for Windows)

1. **Install Waitress**
   ```bash
   pip install waitress
   ```

2. **Create `run_production.py`**
   ```python
   from waitress import serve
   from app import app
   
   if __name__ == "__main__":
       serve(app, host="0.0.0.0", port=5000)
   ```

3. **Run**
   ```bash
   python run_production.py
   ```

#### Using Gunicorn (Linux/Mac)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Run**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Option 3: Docker Deployment

1. **Create `Dockerfile`** (if not exists)
   ```dockerfile
   FROM python:3.10-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   
   CMD ["python", "app.py"]
   ```

2. **Build and run**
   ```bash
   docker build -t autism-app .
   docker run -p 5000:5000 autism-app
   ```

## Project Structure

```
autism_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── best_model.pkl        # Trained ML model (required)
├── encoders.pkl          # Label encoders (required)
├── users.csv             # User database (auto-created)
├── static/
│   ├── style.css         # Stylesheet
│   ├── logo.svg          # App logo
│   ├── chatbot.js        # Chatbot functionality
├── templates/
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── personal_info.html # Personal info form
│   └── predict.html      # Prediction form & results
└── README.md             # This file
```

## Configuration

### Secret Key (Important for Production)

Change the secret key in `app.py`:

```python
app.secret_key = "your-secret-key-here-change-this"
```

Generate a secure key:
```python
import secrets
print(secrets.token_hex(32))
```

### Model Files

Ensure your model files match the expected format:
- `best_model.pkl` should be a scikit-learn model with `.predict()` and `.predict_proba()` methods
- `encoders.pkl` should be a dictionary with keys: `gender`, `ethnicity`, `jaundice`, `austim`, `contry_of_res`, `used_app_before`, `relation`

## Usage Flow

1. **Register/Login** - Create an account or log in
2. **Personal Information** - Fill in demographic and background details
3. **Behavioral Assessment** - Answer 10 Yes/No behavioral questions + AQ-10 score
4. **View Results** - Get screening result (Yes/No) with confidence percentage
5. **Chatbot** - Click the 💬 button to ask questions anytime

## Chatbot Features

The chatbot can answer questions about:
- What is autism?
- Early signs and symptoms
- When to see a doctor
- Treatment options
- Resources and support
- Diagnosis information

## Troubleshooting

### Issue: Model files not found
**Solution**: Ensure `best_model.pkl` and `encoders.pkl` are in the project root directory.

### Issue: Version mismatch warnings (scikit-learn)
**Solution**: The requirements.txt specifies `scikit-learn==1.6.1`. If you get warnings, re-train your model with the same version or update the version in requirements.txt.

### Issue: Port already in use
**Solution**: Change the port in `app.py`:
```python
app.run(debug=True, host="0.0.0.0", port=5001)
```

### Issue: CSS not loading
**Solution**: 
- Check that `static/style.css` exists
- Clear browser cache
- Verify Flask is serving static files correctly

### Issue: Chatbot not working
**Solution**: 
- Ensure JavaScript is enabled in the browser
- Check browser console for errors
- Verify `/chatbot` route is accessible

## Security Notes

- **Production Deployment**: 
  - Set `debug=False` in `app.py`
  - Use a strong secret key
  - Consider using HTTPS
  - Implement rate limiting
  - Use environment variables for sensitive data

- **Data Privacy**: 
  - User data is stored locally in `users.csv`
  - Passwords are hashed using SHA-256
  - Session data is stored server-side

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the code comments in `app.py`
3. Ensure all dependencies are correctly installed

## License

This project is provided as-is for educational and screening purposes. **This tool is a screening aid only and does not replace a clinical diagnosis.**

## Version

- **Current Version**: 2.0
- **Last Updated**: 2025

---

**Important**: Always consult qualified healthcare professionals for clinical diagnosis and treatment decisions.
