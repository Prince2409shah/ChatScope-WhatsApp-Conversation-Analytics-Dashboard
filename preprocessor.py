import re
import pandas as pd

def preprocess(data):
    # Regex that handles:
    # - 12h / 24h
    # - am/pm
    # - 2 or 4 digit years
    pattern = (
        r'(\d{1,2}/\d{1,2}/\d{2,4},\s'
        r'\d{1,2}:\d{2}'
        r'(?:\s?[apAP][mM])?)\s-\s'
    )

    messages = re.split(pattern, data)
    
    dates = []
    texts = []

    for i in range(1, len(messages), 2):
        dates.append(messages[i])
        texts.append(messages[i + 1])

    df = pd.DataFrame({
        'message_date': dates,
        'user_message': texts
    })

    # Convert to datetime safely
    df['message_date'] = (
        df['message_date']
        .astype(str)
        .str.replace('\u202f', ' ', regex=False)  # narrow no-break space fix
    )

    df['date'] = pd.to_datetime(
        df['message_date'],
        errors='coerce',
        dayfirst=True
    )

    # Separate user and message
    users = []
    messages_clean = []

    for msg in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', msg)
        if len(entry) >= 3:
            users.append(entry[1])
            messages_clean.append(entry[2])
        else:
            users.append('group_notification')
            messages_clean.append(entry[0])

    df['user'] = users
    df['message'] = messages_clean

    df.drop(columns=['user_message', 'message_date'], inplace=True)

    # Time features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    # Time period buckets
    df['period'] = df['hour'].apply(
        lambda h: f"{h:02d}-{(h+1)%24:02d}"
    )

    return df
