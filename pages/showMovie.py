import streamlit as st
import requests
from annotated_text import annotated_text
import os


# from dotenv import load_dotenv  #to interact with .env file
# load_dotenv()                   #make .env variables as enviornment variable
API_KEY=st.secrets["API_KEY"]    #able to load file




st.set_page_config(layout='wide',page_title='Movies')

def extract_data(url):
    try:
        message=requests.get(url)
        return message.json()
    except Exception as e:
        st.error(e)


def count_col(col,data):
    sum=0
    columns=[]
    for i in col:
        if data.get(i,'N/A')!='N/A':
            columns.append(i)
    return columns





if st.session_state.get('imdb',False):
    #Gathering Data

    data=extract_data(f'http://www.omdbapi.com/?i={st.session_state['imdb']['imdb']}&apikey={API_KEY}&')
    if data.get("Response",False):
        #Title
        st.title(data['Title'])

        #Sub Title
        col=['Year','BoxOffice','Runtime','Rated','Type']
        col=count_col(col,data)
        for i,j in zip(st.columns(len(col)),col):
            i.metric(j,data.get(j))



        #Mid Section
        col1,col2= st.columns([0.6,0.4])
        if data.get('Poster','N/A')!='N/A':  #image
            resp=requests.get(data['Poster'])
            col1.image(resp.content)
        else:
            col1.info("Image is Not Available")

        col=['Language','Country']       #mid-side
        col=count_col(col,data)
        for i in col:
            col2.subheader(i)
            col2.write(f"{data[i]}")

        with col2.popover("Ratings"):
            if data.get('Ratings','N/A')!='N/A':
                for i in data['Ratings']:
                    st.metric(i['Source'],i['Value'])
            st.metric('IMDB Rating',data['imdbRating'])


        #Genre Tags
        tags=data['Genre'].split(',')
        tags_prep=[]
        for i in tags:
            tags_prep.append((i," "))
            tags_prep.append(" ")
        annotated_text(tags_prep)



        #Plot
        if data.get("Plot",'N/A')!='N/A':
            st.write(data['Plot'])



        #Details
        col=['Director','Writer','Actors']
        for i in col:
            st.markdown("-------")
            col1,col2 = st.columns(2,gap="small")
            col1.markdown(f"##### {i}")
            col2.write(data[f'{i}'])

        st.markdown("-------")

    else:
        st.error("Movie Not Found")

