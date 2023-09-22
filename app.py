import pickle
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import requests

# Set Streamlit to full screen mode
st.set_page_config(
    page_title="Books Recommender Web-App",
    page_icon="📖",
    layout="wide",  # You can adjust the layout as needed
    initial_sidebar_state="expanded",
)





# Create a container for the navigation buttons at the top
nav_container = st.container()

# Add navigation buttons to the container
with nav_container:
    #st.image("MoVies.png")
    selected = option_menu(
        menu_title=None,
        options=["Home","Top Books", "App", "Contact"],
        icons=["house", "book","person", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "25px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "green"},
        },
    )
############
# Main Home #
#############

popular_df = pickle.load(open('popular.pkl', 'rb'))
if selected == "Home":
    st.image("MoVies.png")


#############
# Top Books##
#############

elif selected == "Top Books":
    st.title("Top 50 Books")

    # Define the number of columns
    num_columns = 5  # You can adjust the number of columns as needed

    # Calculate the number of items per column
    items_per_column = len(popular_df) // num_columns

    # Create a custom layout with multiple columns
    columns = st.columns(num_columns)

    for i in range(num_columns):
        start_idx = i * items_per_column
        end_idx = start_idx + items_per_column

        with columns[i]:
            for j in range(start_idx, end_idx):
                st.image(popular_df['Image-URL-M'].iloc[j])
                st.write(popular_df['Book-Title'].iloc[j])
                st.write(popular_df['Book-Author'].iloc[j])
                st.write("Votes -", popular_df['num_rating'].iloc[j])  # Corrected column name
                st.write("Rating - {:.2f}".format(popular_df['avg_rating'].iloc[j]))  # Format rating to two decimal places


########
# App #
########

elif selected == "App":
    # Add content for the App page
    st.title("Book Recommender Web-App")

    # Load your data
    popular_df = pickle.load(open('popular.pkl', 'rb'))
    pt = pickle.load(open('pt.pkl', 'rb'))
    books = pickle.load(open('books.pkl', 'rb'))
    similarity_scores = pickle.load(open('similarity.pkl', 'rb'))

    # Create a list of all book titles
    all_book_titles = pt.index.tolist()

    # User input for book title
    user_input = st.selectbox("Select a book title:", all_book_titles)

    if st.button("Recommend"):
        try:
            index = np.where(pt.index == user_input)[0][0]
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

            data = []
            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

                data.append(item)

            # Calculate the number of columns for recommended books
            num_columns = 4  # You can adjust the number of columns as needed
            items_per_column = len(data) // num_columns

            # Create a custom layout with multiple columns for recommended books
            columns = st.columns(num_columns)

            for i in range(num_columns):
                start_idx = i * items_per_column
                end_idx = start_idx + items_per_column

                with columns[i]:
                    for j in range(start_idx, end_idx):
                        st.image(data[j][2])
                        st.write(data[j][0])
                        st.write(data[j][1])

        except IndexError:
            st.error("Book not found!")
                       




###############
# Contact Page#
###############
elif selected == "Contact":
    #st.title(f"You have selected {selected}")

    
    
    ### About the author
    st.write("##### About the author:")
    
    ### Author name
    st.write("<p style='color:blue; font-size: 50px; font-weight: bold;'>Usama Munawar</p>", unsafe_allow_html=True)
    
    ### Connect on social media
    st.write("##### Connect with me on social media")
    
    ### Add social media links
    ### URLs for images
    linkedin_url = "https://img.icons8.com/color/48/000000/linkedin.png"
    github_url = "https://img.icons8.com/fluent/48/000000/github.png"
    youtube_url = "https://img.icons8.com/?size=50&id=19318&format=png"
    twitter_url = "https://img.icons8.com/color/48/000000/twitter.png"
    facebook_url = "https://img.icons8.com/color/48/000000/facebook-new.png"
    
    ### Redirect URLs
    linkedin_redirect_url = "https://www.linkedin.com/in/abu--usama"
    github_redirect_url = "https://github.com/UsamaMunawarr"
    youtube_redirect_url ="https://www.youtube.com/@CodeBaseStats"
    twitter_redirect_url = "https://twitter.com/Usama__Munawar?t=Wk-zJ88ybkEhYJpWMbMheg&s=09"
    facebook_redirect_url = "https://www.facebook.com/profile.php?id=100005320726463&mibextid=9R9pXO"
    
    ### Add links to images
    st.markdown(f'<a href="{github_redirect_url}"><img src="{github_url}" width="60" height="60"></a>'
                f'<a href="{linkedin_redirect_url}"><img src="{linkedin_url}" width="60" height="60"></a>'
                f'<a href="{youtube_redirect_url}"><img src="{youtube_url}" width="60" height="60"></a>'
                f'<a href="{twitter_redirect_url}"><img src="{twitter_url}" width="60" height="60"></a>'
                f'<a href="{facebook_redirect_url}"><img src="{facebook_url}" width="60" height="60"></a>', unsafe_allow_html=True)
##########################################
# Display a message if no page is selected#
##############################################
else:
    st.title("Welcome to the Book Recommender App")
    st.write("Please select a page from the navigation menu on the left.")
####################
# Thank you message#
#####################
st.write("<p style='color:green; font-size: 30px; font-weight: bold;'>Thank you for using this app, share with your friends!😇</p>", unsafe_allow_html=True)