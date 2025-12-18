import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # preprocess data
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].dropna().unique().tolist()

    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    if 'Meta AI' in user_list:
        user_list.remove('Meta AI')

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # ---------- STATS ----------
        num_message, words, num_media_message, links_shared = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_message)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_message)
        with col4:
            st.header("Links Shared")
            st.title(links_shared)

        # ---------- BUSY USERS ----------
        if selected_user == 'Overall':
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns(2)

            with col1:
                st.title("Most Busy Users")
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.title("Contribution")
                st.dataframe(new_df)

        # ---------- WORD CLOUD ----------
        st.title("Word Cloud")
        df_wordcloud = helper.create_wordcloud(selected_user, df)

        if df_wordcloud is not None:
            fig, ax = plt.subplots()
            ax.imshow(df_wordcloud)
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.info("Not enough text data to generate a word cloud.")

        # ---------- MOST COMMON WORDS ----------
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)

        if not most_common_df.empty:
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        else:
            st.info("No common words found.")

        # ---------- EMOJI ANALYSIS ----------
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)

        with col2:
            if not emoji_df.empty:
                fig, ax = plt.subplots()
                ax.pie(
                    emoji_df[1].head(),
                    labels=[str(e) for e in emoji_df[0].head()],
                    autopct="%0.2f%%",
                    textprops={'fontsize': 14}
                )
                st.pyplot(fig)
            else:
                st.info("No emojis found.")

        # ---------- MONTHLY TIMELINE ----------
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # ---------- DAILY TIMELINE ----------
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # ---------- ACTIVITY MAP ----------
        st.title("Activity Map")

        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # ---------- HEATMAP ----------
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)

        if not user_heatmap.empty:
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            st.pyplot(fig)
        else:
            st.info("Not enough data to generate heatmap.")
