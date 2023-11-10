from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        num_messages = df.shape[0]

        words = []
        for message in df['message']:
            words.extend(message.split())

        pattern = r'image|video|document|audio omitted'

        # Use the `str.contains` method to apply the regex pattern, setting `na=False` to treat NaNs as False
        mask = df['message'].str.contains(pattern, na=False)
        media_message = len(df[mask])

        return num_messages, len(words), media_message

    else:
        new_df = df[df['user'] == selected_user]
        num_messages = new_df.shape[0]

        pattern = r'image|video|document|audio omitted'

        # Use the `str.contains` method to apply the regex pattern, setting `na=False` to treat NaNs as False
        mask = new_df['message'].str.contains(pattern, na=False)
        media_message = len(new_df[mask])

        words = []
        for message in new_df['message']:
            words.extend(message.split())

        return num_messages, len(words), media_message


def most_busiest_users(df):
    x= df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df

def create_wordcloud(selected_user,df):
    pattern = r'image|video|audio|document omitted'

    # Use the `str.contains` method to apply the regex pattern, setting `na=False` to treat NaNs as False
    mask = df['message'].str.contains(pattern, na=False)
    df = df[~mask]

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    pattern = r'image|video|audio|document omitted'

    # Use the `str.contains` method to apply the regex pattern, setting `na=False` to treat NaNs as False
    mask = df['message'].str.contains(pattern, na=False)
    temp = df[~mask]

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap