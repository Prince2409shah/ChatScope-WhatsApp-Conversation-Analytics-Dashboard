import streamlit as st
import preprocessor,helper  
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")
# go and search streamlit documentation and there go in api refrence and search for file_uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # convert data to string
    data = bytes_data.decode("utf-8")
    # st.text(data)
    # preprocess data
    df=preprocessor.preprocess(data)
    # st.dataframe(df)  # display dataframe in streamlit app
    #fetch unique user 
    user_list=df['user'].unique().tolist()
    #there are other non user like group notification and Meta AI
    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    if 'Meta AI' in user_list:
        user_list.remove('Meta AI')

    user_list.sort()
    #keeping overall first
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    #adding Show analysis button if someone click then something will happen
    if st.sidebar.button("Show Analysis"):
        num_message,words,num_media_message,links_shared=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
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
        #finding the busiest user in the group(Group level)
        if selected_user=='Overall':
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                #displaying bar chart
                st.title("Most Busy User")
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                #displaying percentage bargraph
                st.title("Contribution")
                st.dataframe(new_df)
        #word clouds
        df_wordcloud=helper.create_wordcloud(selected_user,df)
        st.title("Word Cloud")
        fig,ax=plt.subplots()

        ax.imshow(df_wordcloud)
        st.pyplot(fig)
        #most common words
        most_common_df=helper.most_common_words(selected_user,df)
        st.title("Most Common Words")
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        st.pyplot(fig)
        plt.xticks(rotation='vertical')
        #emojie analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            # Use Unicode emojis as labels, set font to support emojis
            ax.pie(
                emoji_df[1].head(),     # values
                labels=[str(e) for e in emoji_df[0].head()],  # ensure emojis are strings
                autopct="%0.2f%%",
                textprops={'fontsize': 16, 'fontname': 'Segoe UI Emoji'}  # font supporting emojis
            )
            st.pyplot(fig)


        #monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()

        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #daily timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #Activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        #heatmap
        st.title("Weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)
        plt.xticks(rotation='vertical')

        

        






        


