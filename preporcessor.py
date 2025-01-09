import pandas as pd
import re
import calendar

def preprocess(data):
    pattern = "\d{2}\/\d{2}\/\d{2},\s\d{1,2}:\d{2}\s?(?:am|pm)\s-\s"  # pattern for converting date into 24hrs format
    messages = re.split(pattern, data)[2:]  # filters messages content and store it in messages
    dates = re.findall(pattern, data)  # filters date and time and stores it in dates
    # will clean the dates and remove unncessary things
    dates = [date.replace('\u202f', ' ').replace(' - ', '').replace('/', '-').replace(',', '') for date in dates]
    min_length = min(len(messages),len(dates))  # since length of dates is one more than messages we will truncate the shorter one
    messages = messages[:min_length]
    dates = dates[:min_length]
    df = pd.DataFrame({"user_message": messages, "dates": dates})  # store messages and user under user_message column
    df["dates"] = pd.to_datetime(df["dates"], format="%d-%m-%y %I:%M %p")  # change string dates to date datatype
    df["year"] = df["dates"].dt.year
    df["month"] = df["dates"].dt.month
    df["day"] = df["dates"].dt.day
    df["hour"] = df["dates"].dt.hour
    df["minutes"] = df["dates"].dt.minute
    df["am_pm"] = df["dates"].dt.strftime("%p")
    df.drop("dates", axis=1, inplace=True)  # remove dates column as it's no longer necesarry

    # separate user and messages
    users = []
    messages = []
    for message in df["user_message"]:
        entry = re.split(r"([\w\W]+?):\s", message)
        if entry[1:]:  # username
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])
    df["user"] = users
    df["message"] = messages
    df['month_name'] = df['month'].apply(lambda x: calendar.month_name[x])
    df.drop("user_message", axis=1, inplace=True)
    return df

