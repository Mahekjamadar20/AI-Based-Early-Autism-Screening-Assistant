# Quick Start Guide

## Fast Deployment (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Files
Make sure these files exist:
- ✅ `best_model.pkl`
- ✅ `encoders.pkl`
- ✅ `app.py`
- ✅ `static/style.css`
- ✅ `templates/` folder with all HTML files

### Step 3: Run the App
```bash
python app.py
```

**Done!** Open your browser at: `http://127.0.0.1:5000`

---

## Troubleshooting Quick Fixes

### ❌ Module not found
**Fix**: `pip install -r requirements.txt`

### ❌ Model files not found
**Fix**: Place `best_model.pkl` and `encoders.pkl` in the project root

### ❌ Port 5000 already in use
**Fix**: Change port in `app.py` line 257: `app.run(debug=True, host="0.0.0.0", port=5001)`

### ❌ CSS not loading
**Fix**: Clear browser cache (Ctrl+F5)

---

## Production Deployment (Optional)

### Windows
```bash
pip install waitress
python -c "from waitress import serve; from app import app; serve(app, host='0.0.0.0', port=5000)"
```

### Linux/Mac
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

**Need more help?** Check `README.md` for detailed documentation.
