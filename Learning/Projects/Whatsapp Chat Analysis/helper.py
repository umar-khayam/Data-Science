def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        num_messages = df.shape[0]

        words = []
        for message in df['message']:
            words.extend(message.split())

        pattern = r'image|video|document omitted'

        # Use the `str.contains` method to apply the regex pattern, setting `na=False` to treat NaNs as False
        mask = df['message'].str.contains(pattern, na=False)
        media_message = len(df[mask])

        return num_messages, words, media_message

    else:
        new_df = df[df['user'] == selected_user]
        num_messages = new_df.shape[0]

        pattern = r'image|video|document omitted'

        # Use the `str.contains` method to apply the regex pattern, setting `na=False` to treat NaNs as False
        mask = new_df['message'].str.contains(pattern, na=False)
        media_message = len(new_df[mask])

        words = []
        for message in new_df['message']:
            words.extend(message.split())

        return num_messages, words, media_message