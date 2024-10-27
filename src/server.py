from flask import Flask, request, send_from_directory, render_template, jsonify
import os
import json
import logging
import main  # Import the main.py script

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("web_app.log"),  # Separate log file for web app
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    logs = []
    try:
        with open("app.log", "r") as f:  # Read the main.py log file
            logs = f.readlines()
    except FileNotFoundError:
        logs = ["Log file not found."]

    novels = []
    if os.path.exists(main.config['save_path']): # Modified to use save_path from config
        for filename in os.listdir(main.config['save_path']): # Modified to use save_path from config
            if os.path.isfile(os.path.join(main.config['save_path'], filename)): # Modified to use save_path from config
                novels.append(filename)

    if request.method == "POST":
        book_id = request.form.get("book_id")
        if book_id:
            result = main.book2down(book_id) # Call book2down from main.py
            if result == "s":
                return render_template("index.html", message=f"Book {book_id} downloaded successfully!", logs=logs, novels = novels)
            else:
                return render_template("index.html", message=f"Error downloading book {book_id}.", logs=logs, novels = novels)

        search_query = request.form.get("search_query")
        if search_query:
            book_id = main.search(search_query)
            if book_id:
                return jsonify({"book_id": book_id}) # return the ID for handling on client side
            else:
                return jsonify({"error": "Book not found"})

    return render_template("index.html", logs=logs, novels=novels) # Pass novels to the template


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(main.config['save_path'], filename, as_attachment=True) # Modified to use save_path from config


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12930)