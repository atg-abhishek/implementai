from flask import Flask 

app = Flask(__name__)

@app.route('/')
def hello():
    return "Welcome to the server for the Implement AI hackathon"

if __name__ == "__main__":
    app.run(debug=True)