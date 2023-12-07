import streamlit as st
import pickle
from sklearn.compose import make_column_transformer
import pandas as pd
import datetime
from PIL import Image, ImageDraw
import time
import base64
import sklearn
from sklearn.ensemble import RandomForestClassifier
import nltk
import sklearn
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler



st.set_page_config(page_title="EC", page_icon="logo.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_background = get_img_as_base64("Picture1.png")

# css section
page_bg_img = f"""
<style>

[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img_background}");
background-size: 100%;
background-repeat: no-repeat;
background-position: center;
background-position: top left; /*center*/
background-repeat: no-repeat;
background-attachment: local;  /*fixed*/
}}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

#open css style file
with open('style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

#load model and transformer data
model = pickle.load(open("my_model","rb"))
transformer = pickle.load(open('transformer', 'rb'))

#the page

#the time header
header = st.container()
timestamp = datetime.datetime.now()
if timestamp.hour<12:timestamp = "Good Morning"
elif timestamp.hour < 16:timestamp = "Good afternoon"
else:timestamp = "Good evening"

header.write("<div class='fixed-header'>{} </div>".format(timestamp), unsafe_allow_html=True)
#header.write('The scikit-learn version is {}.'.format(sklearn.__version__))
#the title of the page
st.markdown('<h1 class="title">Employee Churn</h1>', unsafe_allow_html=True)

st.markdown('#')
st.markdown('#')

col1,col2 = st.columns(2)

with col1:
    #for input the satisfaction percentage
    satisfaction_level=st.slider("**What is the employee satisfaction**", 0,100, step=1)
    st.text("The level : %{} ".format(satisfaction_level))
    satisfaction_level = satisfaction_level/100

    st.markdown('#')

    #for input the time in company
    time_spent_company = st.number_input('**Time spent in the company**', min_value=2,max_value=10, value=2, step=1)

    st.markdown('#')

    #for input employee work accident
    work_accident = st.radio("**Does an employee has a work accident ?**",("Yes","No"))
    if work_accident == "Yes": work_accident =1
    elif work_accident == "No": work_accident =0

    st.markdown('#')

    #for input employee Departments
    Departments = st.selectbox("**Select the Departments of the employee**", ('sales', 'technical', 'support', 'IT','product_mng','marketing','RandD','accounting','hr','management'))




with col2:
    #for input the evaluation percentage
    last_evaluation=st.slider("**What was the employee last evaluation**", 0,100, step=1)
    st.text("The level : %{} ".format(last_evaluation))
    last_evaluation = last_evaluation/100

    st.markdown('#')
       
    #for input the number of projects
    number_projects = st.number_input('**How many projects does the employee worked on ?**', min_value=2,max_value=7, value=2, step=1)

    st.markdown('#')

    #for input employee promotion
    promotion_last_5years = st.radio("**Did the employee had a promotion in the last 5 years ?**",("Yes","No"))
    if promotion_last_5years == "Yes": promotion_last_5years =1
    elif promotion_last_5years == "No": promotion_last_5years =0

    st.markdown('#')

    #for input employee Salary level
    Salary = st.selectbox("**Select Salary level of employee**", ('high', 'medium', 'low'))


col3,col4,col5 = st.columns(3)


with col4:
    st.markdown('#')

    #for input employee average monthly hours
    average_monthly_hours = st.number_input('**The average monthly hours**', min_value=96,max_value=310, value=96, step=1)

    st.markdown('#')

    
    
    button = st.button("**prediction**")

    #directory to all stor all the value
    my_dict = {
    "satisfaction_level": satisfaction_level,
    "last_evaluation": last_evaluation,
    "time_spend_company": time_spent_company,
    'number_project':number_projects,
    "promotion_last_5years": promotion_last_5years,
    "Department": Departments,
    "salary": Salary,
    "average_montly_hours":average_monthly_hours,
    "Work_accident": work_accident,
    }
    #directory to DataFrame
    df = pd.DataFrame.from_dict([my_dict])

    if button:
      df2 = transformer.transform(df)
      prediction = model.predict(df2)
      if prediction==0:
          prediction = "Stay"
          time.sleep(0.9)
          st.balloons()
      else:
          prediction = "Lift"
      st.text("The chance is : {} ".format(prediction))

#st.text(df.head())
st.sidebar.header("Created by:\nRuwaidiah   \nRawan   \nSara   \nShuruq   \nLujain   \nAhmed   \nMariam   \nFatima   \nRenad")
