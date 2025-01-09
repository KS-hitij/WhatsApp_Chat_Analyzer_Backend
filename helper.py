from urlextract import URLExtract  # for extracting links
from collections import Counter  # for getting top used words
import re
import emoji  # for emojis


def count_messages(df, selected_user):
    if selected_user == "Overall":
        return df.shape[0]
    else:
        return df[df["user"] == selected_user].shape[0]


def count_words(df, selected_user):
    words = []
    if selected_user == "Overall":
        for message in df["message"]:
            words.extend(message.split())
    else:
        temp = df[df["user"] == selected_user]
        for message in temp["message"]:
            words.extend(message.split())
    return len(words)


def count_media(df, selected_user):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    media_messages = df[df["message"] == "<Media omitted>\n"].shape[0]
    return media_messages


def count_links(df, selected_user):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    extractor = URLExtract()
    links = []
    for message in df["message"]:
        links.extend(extractor.find_urls(message))
    return len(links)


def active_users(df):
    most_active_users = df["user"].value_counts().head().index.tolist()
    return most_active_users


def count_chat_percentage(df, selected_user):
    total_message = df.shape[0]
    chat_percent = []
    if selected_user == "Overall":
        for user in df["user"].unique():
            user_msg = count_messages(df, user)
            percent = round((user_msg/total_message)*100, 2)
            chat_percent.append([user, percent])
    else:
        user_msg = count_messages(df, selected_user)
        percent = round((user_msg / total_message) * 100, 2)
        chat_percent.append([selected_user, percent])
    return chat_percent


def top_used_words(df, selected_user):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    # cleaning group notification
    df = df[df["user"] != "group_notification"]
    # cleaning media omitted message
    df = df[df["message"] != "<Media omitted>\n"]
    words = []
    for message in df['message']:
        # Clean the message (convert to lowercase, remove punctuation)
        cleaned_message = re.sub(r'[^a-zA-Z0-9\s]', '', message.lower())
        words.extend(cleaned_message.split())
    word_count = Counter(words)
    if len(word_count) >= 100:
        top_100_words = word_count.most_common(100)
    else:
        top_100_words = word_count.most_common(len(word_count))
    return top_100_words


def most_used_emojis(df, selected_user):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    emojis = []
    for message in df["message"]:
        for c in message:
            if emoji.is_emoji(c):
                emojis.extend(c)
    emoji_count = Counter(emojis)
    most_used_emoji = emoji_count.most_common(5)
    return most_used_emoji


def monthly_timeline(df, selected_user):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    timeline = df.groupby(["year", "month_name"]).count()["message"].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month_name"][i] + "-" + str(timeline["year"][i]))
    new_timeline=[]
    for i in range(timeline.shape[0]):
        new_timeline.append([time[0], timeline["message"][i].tolist()])

    return new_timeline
