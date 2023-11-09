import re
import pandas as pd

def preprocess(data):
    # Define the pattern to split the date and message parts
    pattern = r'\[\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}:\d{2}\s[apAP][mM]\]'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime and format it correctly
    df['message_date'] = df['message_date'].str.replace('[', '').str.replace(']', '').str.replace('‎', '')
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M:%S %p')

    # Extract user and message
    df[['user', 'message']] = df['user_message'].str.extract(r'([^:]+):\s?(.*)', expand=True)

    # Drop the original user_message column
    df.drop(columns=['user_message'], inplace=True)

    # Rename columns for clarity
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract date components
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Define the period of the day
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df
