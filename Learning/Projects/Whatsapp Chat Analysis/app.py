import streamlit as st
import preprocessor, helper

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):

        num_messages, total_words, media_message = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(len(total_words))

        with col3:
            st.header('Total Media')
            st.title(media_message)