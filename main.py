import streamlit as st
import requests
from streamlit_lottie import st_lottie
#DB Management
import sqlite3
import pandas as pd
pd.set_option('display.max_colwidth', 1)
from IPython.display import display
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def create_userstable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password =?',(username,password))
    data = c.fetchall()
    return data

def check_userdata(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? OR password =?', (username, password))
    data = c.fetchall()
    return data


def create_soup(x):
    soup = ' '.join(x['text'])
    return soup

def get_recommendations(title, indices, cosine_sim, data):
    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    article_indices = [i[0] for i in sim_scores]

    return (data['title'].iloc[article_indices], data['url'].iloc[article_indices])


articles_df = pd.read_csv('C:/Users/ARCHANA/Downloads/Article Recommondation/shared_articles.csv')

articles_df = articles_df[articles_df['eventType'] == 'CONTENT SHARED']

articles_df = articles_df[articles_df['lang'] == 'en']

articles_df = pd.DataFrame(articles_df, columns=['contentId', 'authorPersonId', 'url', 'title', 'text'])

articles_df['soup'] = articles_df.apply(create_soup, axis=1)

tfidf = TfidfVectorizer(stop_words='english')

tfidf_matrix = tfidf.fit_transform(articles_df['text'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix, True)

metadata = articles_df.reset_index()

indices = pd.Series(metadata.index, index=metadata['title']).drop_duplicates()


conn = sqlite3.connect('data.db')
c = conn.cursor()

st.set_page_config(page_title="WorldOfArticles", page_icon=":tada:", layout="wide")

lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_kcxosgub.json")


with st.container():
    st.subheader("welcome!")
    st.title("Article Recommendation Engine")
    st.write("Let's Drive in!")
with st.container():
    st.write("---")
    left_column, right_column = st.columns((2, 1))
    with left_column:
        menu = ["Home", "Login", "SignUp"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Home":
            st.subheader("Home")
            """
              Hey there!
              This is a web page where one can find the pathway for exploring articles
              which are related to your previous read articles.This helps people to explore 
              more articles in the similar genre of the articles read previously.    
            """

        elif choice == "Login":

            st.sidebar.subheader("Login Section")
            username = st.sidebar.text_input("User Name")
            password = st.sidebar.text_input("Password", type='password')
            if st.sidebar.checkbox("login"):
                create_userstable()
                login_result = login_user(username, password)
                if login_result:
                    st.sidebar.success("Logged In as {}".format(username))
                    task = st.selectbox("Task", ["--", "Articles_List", "Recommendations"])
                    if task == "Articles_List":
                        st.subheader("ARTICLES")
                        st.dataframe(articles_df['title'])
                    elif task == "Recommendations":
                        st.subheader("RECOMMENDATIONS")
                        article_name = st.selectbox("pick an Article Title Name:",articles_df['title'].values,index=0)
                        recommondations = get_recommendations(article_name, indices, cosine_sim, metadata)
                        st.text(recommondations)
                        """
                        Tadaa!
                        Here are few related Articles!
                        Have Fun!!
                        """


                else:
                    st.sidebar.warning("Incorrect Username/Password")



        elif choice == "SignUp":
            st.sidebar.subheader("Create New Account")
            new_user = st.sidebar.text_input("Username")
            new_password = st.sidebar.text_input("Password", type='password')
            if st.sidebar.button("SignUp"):
                create_userstable()
                result=check_userdata(new_user, new_password)
                if result:
                    st.sidebar.warning("Username/Password already exists.")
                else:
                    add_userdata(new_user, new_password)
                    st.sidebar.success("You have successfully created a Valid Account.")
                    st.sidebar.info("Go to login Menu to login")

    with right_column:
        st_lottie(lottie_coding, height=400, key="coding")





