from flask import Flask, jsonify

app = Flask(__name__)

# Manually configure CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

# Example route
@app.route('/api/data')
def get_data():
    data = {"message": "Hello from Flask!"}
    print("Hello, world!")
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

