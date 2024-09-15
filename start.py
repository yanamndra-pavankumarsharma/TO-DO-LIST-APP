from waitress import serve
from app import app  # Adjust the import based on your module and app name

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8080)
