import streamlit as st
import requests
import pandas as pd
import os

from dotenv import load_dotenv  #to interact with .env file
load_dotenv()                   #make .env variables as enviornment variable
API_KEY=os.getenv("API_KEY")    #able to load file




with st.form("my_form"):
    name=st.text_input("Name")
    year=st.text_input("Year")
    type = st.selectbox(
        "How would you like to be contacted?",
        ("","movie", "series", "episode"),
        placeholder=" fdg"
    )
    st.form_submit_button('Submit')

if name:
    with st.spinner('Wait for it...'):
        t=True
        details=[]
        sum=1
        while(t!=False):
            try:
                message=requests.get(f'http://www.omdbapi.com/?s={name}&apikey={API_KEY}&y={year}&type={type}&page={sum}')
                x=message.json()
                details.extend(x.get("Search"))
                sum+=1
            except TypeError as e:
                t=False

        try:
            df=pd.DataFrame(details)
            df=df[['Poster','Title','Year','Type','imdbID']]
        except Exception as e:
            st.error(f"Movie Not Found with Error {e}")

        event=st.dataframe(df,
                         hide_index=True,
                         on_select='rerun',
                         selection_mode='single-row',
                        column_config = {
                        "Poster": st.column_config.ImageColumn(
                     "Image", help="Image Preview"
                        )
                        })

    if len(event.selection['rows']):
        try:
            selected_row = event.selection['rows'][0]
            imdb = df.iloc[selected_row]['imdbID']
            title = df.iloc[selected_row]['Title']

            st.session_state['imdb'] = {'imdb': imdb}
            st.page_link('pages\showMovie.py', label=f'Goto {title} Page', icon='🗺️')
        except Exception as e:
            st.error(e)


