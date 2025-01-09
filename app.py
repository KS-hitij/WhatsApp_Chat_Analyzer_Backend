from flask import Flask, request, jsonify
import preporcessor  # Assuming this is your module containing the preprocess function
import helper      # file that will be containing various functions necessary for analysis

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from your frontend

df = None  # globally define df so that it can be used until the session is over


@app.route('/upload', methods=['POST'])
def upload_file():
    global df  # declaring it global so that it can be modified
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # Check if a file was actually uploaded
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Read the file data
    data = file.read().decode("utf-8")  # Decoding the file content to string

    # Process the data using your existing preprocessing function
    df = preporcessor.preprocess(data)

    # Extract unique users and prepare the response
    user_list = df["user"].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    # Return the user list as a JSON response
    return jsonify({"users": user_list})


@app.route('/analyze', methods=['POST'])
def analyze():
    global df  # declaring it global so that it can be accessed after uploading
    if df is None:
        return jsonify({"error": "Upload the File"})
    data = request.get_json()
    if not data or "selected_user" not in data:
        return jsonify({"error": "Selected user not provided"}), 400

    selected_user = data["selected_user"]
    # fetch number of messages
    num_messages = helper.count_messages(df, selected_user)

    # fetch number of words
    words = helper.count_words(df, selected_user)

    # fetch number of media messages
    media_messages = helper.count_media(df, selected_user)

    # fetch number of links shared
    links = helper.count_links(df, selected_user)

    most_active_users = []
    if selected_user == "Overall":
        # fetch top 5 active users
        most_active_users = helper.active_users(df)

    chat_percent = helper.count_chat_percentage(df, selected_user)

    most_used_words = helper.top_used_words(df, selected_user)

    most_used_emojis = helper.most_used_emojis(df, selected_user)

    monthly_timeline = helper.monthly_timeline(df, selected_user)

    return jsonify({"numberOfMessages": num_messages, "numberOfWords": words,
                    "numberOfMediaMessages": media_messages, "numberOfLinks": links,
                    "mostActiveUsers": most_active_users, "chatPercentage": chat_percent,
                    "mostUsedWords": most_used_words, "mostUsedEmojis": most_used_emojis,
                    "monthlyTimeline": monthly_timeline})
    

if __name__ == '__main__':
    app.run(port=5000)
