from flaskAPI import app

@app.route("/test")

def Hello():
    return "Hello World"
