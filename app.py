from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route("/")
def home():
    # Local path: project/data/text.txt
    local_path = os.path.join(os.getcwd(), "data", "text.txt")

    # Docker path: /data/text.txt (volume mount)
    docker_path = "/data/text.txt"

    # Determine which path to use
    if os.path.exists(local_path):
        text_path = local_path
    else:
        text_path = docker_path

    print("Using file:", text_path)

    # Read the file
    with open(text_path, "r") as f:
        file_text = f.read()

    return render_template("index.html", file_text=file_text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
