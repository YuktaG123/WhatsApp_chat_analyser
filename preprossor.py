import re
import pandas as pd

def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APMapm]{2}\s?-\s?"
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    cleaned_dates = [date.replace('\u202f', ' ') for date in dates]
    df = pd.DataFrame({'user_message': message, 'message_date': cleaned_dates})

    # Clean the date format and rename the column
    df['dates'] = pd.to_datetime(df['message_date'].str.replace('\u202f', ' '), format='%m/%d/%y, %I:%M %p - ')
    df.drop(columns=['message_date'], inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\s]+?):\s+', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notifications')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['dates'].dt.year
    df['month_num'] = df['dates'].dt.month
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute
    df["only_date"] = df['dates'].dt.date
    df['day_name'] = df['dates'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df