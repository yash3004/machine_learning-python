import dash 
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import plotly.express as px
import webbrowser
from plotly import tools
import base64
import io
import re 
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
import random
import plotly
from wordcloud import WordCloud
import pickle
from dash.dependencies import Input , Output , State
def browser():
    webbrowser.open_new('http://127.0.0.1:8050/')
#importing the dta
df = pd.read_csv('nlp/balanced_rev_2.csv')
rev = df.iloc[:,1].values

#creating the new_ds
def pie_df():
    b = []

    df = pd.read_csv('nlp/balanced_rev_2.csv')
    
     
    for i in df['positivity']:
        if (i == '[0]'):
            i = 0
        else:
            i = 1#print(a.item())
        
        b.append(i)
        
    a = [b.count(1) , b.count(0)]
    labels = ['Positive' , 'Negative']
    plt.pie(a,labels = labels,autopct='%1.2f%%')
   
    plt.savefig('assets/pie2.jpg')
#creating the word cloud
def word_cloud():
    
    x = df.iloc[: , 1].values
    #y = df.iloc[: , -1].values
    corpus = []
    for i in range(0, df.shape[0 ]):
          review = re.sub('[^a-zA-Z]', ' ', x[i])
          review = review.lower()
          review = review.split()
          ps = PorterStemmer()
          all_stopwords = stopwords.words('english')
          all_stopwords.remove('not')
          review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
          review = ' '.join(review)
          corpus.append(review)
    
    list1 = corpus[:100]
    plt.subplots(figsize = (8,8))
    
    wordcloud = WordCloud (
                        background_color = 'white',
                        width = 600,
                        height = 500
                            ).generate(' '.join(list1))
    plt.imshow(wordcloud) # image show             children =  )

    plt.axis('off') # to off the axis of x and y
    plt.savefig('assets/Plotly-World_Cloud3.png')
    plt.show()
    #creating the list of the words
    
    
    #print(corpus)
    
    #creating the word cloud
    
    

rev_list = rev[:100]#100 reviews 

#function for chechk reviews
    #load the model from the pikle file
def check_review(reviewText):
    #load the model from the pikle file
    file = open('nlp/pickle_model_tfidf.pkl','rb')
    recreated_model = pickle.load(file)
    
    
    vocab_file = open('nlp/features.pkl','rb')
    recreated_vocab = pickle.load(vocab_file)
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    recreated_vect = TfidfVectorizer(vocabulary = recreated_vocab)

    reviewText_vectorized = recreated_vect.fit_transform([reviewText])
    
    
    
    return recreated_model.predict(reviewText_vectorized)    
#init the app
app = dash.Dash(__name__)
#creating the app layout 


def create_app():
    word_cloud()
    pie_df()
    main_layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Etsy-app-ui', className="app-header--title")
        ]
    ),
    html.Div(className = 'pie-chart',
        children=html.Div([ 
    
            html.H3('pie-chart'),
            html.Img(src = app.get_asset_url('pie2.jpg')
                )
        ])
    ),
    html.Div(className = 'word-cloud' , 
             children = html.Div([
                 html.H3('word-cloud'),
                 html.Img(src = app.get_asset_url('Plotly-World_Cloud3.png'))
                 
                 ])
             ),
    html.Div(className = 'drop-down',
             children = html.Div([
                 html.H3('drop-down list of reviews'),
                 dcc.Dropdown(id = 'drpdown' , 
                              options = [{'label': t, 'value': t} for t in rev_list] ),
                 html.H4(id = 'drop-down_result' , children = None)
                 
                 ]) ),
    html.Div(className = 'text-area_rev' , 
             children = html.Div([
                 html.H3('reviews chechking'),
                 dcc.Textarea(id = 'textarea_rev' , placeholder = 'enter the review...' , style = {'width':'100%' , 'height' : '100%'}),
                 html.H4(id = 'text-area_result' , children = None)
                 ]))
])
    return main_layout
@app.callback(
    Output( 'drop-down_result'   , 'children'     ),
    [
    Input( 'drpdown'    ,  'value'    )
    ],
    )
def update_app_ui(value):
    print('Data Type of ', str(type(value)))
    print('Value = ', str(value) )

    response = check_review(value)
    print('response = ', response)

    if (response[0] == 0):
        result1 = 'Negative'
    elif  (response[0] == 1):   
        result1 = 'Positive'
    else:
        result1 = 'Unknown'
        
    return result1
@app.callback(
    Output( 'text-area_result'   , 'children'     ),
   
    [
    Input( 'textarea_rev'    ,  'value'    )
    ],
    )
def update_app_ui2(values):
    print('Data Type of ', str(type(values)))
    print('Value = ', str(values) )

    response = check_review(values)
    print('response = ', response)

    if (response[0] == 0):
        result1 = 'Negative'
    elif  (response[0] == 1):   
        result1 = 'Positive'
    else:
        result1 = 'Unknown'
        
    return result1
    
app.layout = create_app()
browser()
app.run_server()                     