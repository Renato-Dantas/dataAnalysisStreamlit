import streamlit as st
from dataAnalysis import *
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import plotly.graph_objects as go 
import numpy as np 


def descriptModel():
    pass
def chooseData():
    startDate = '2020-01-01'
    data = upload_file(startDate)
    return data

def trainTestData(data):
    y = data.Close
    x = data.drop(['Date','Close'], axis = 1) # retirei o Adj aq
    x_train,x_test,y_train,y_test = train_test_split(x,y ,test_size= 0.2, random_state = 123)
    return (x_train,x_test,y_train,y_test)

def trainingModel(x_train,y_train):
    model = RandomForestRegressor(max_depth= 200, n_estimators=200, n_jobs = 20)
    model.fit(x_train,y_train)
    return model

def testingModel(model, x_test, y_test):
    pred = model.predict(x_test)
    rmse = round(mean_squared_error(y_test, pred, squared= False),3)
    st.info(f'The model has an average error of $ {rmse} on the prediction Stock Price')

def prediction(data, model):
    openValue = float(data.Open.tail(1))
    highValue = float(data.High.tail(1))
    lowValue = float(data.Low.tail(1))
    lastValue = float(data['Adj Close'].tail(1))
    lastVolume = float(data.Volume.tail(1))
    
    toPredict = [[openValue, highValue,lowValue, lastValue, lastVolume ]]

    lastPrediction = model.predict(toPredict)
    lastPrediction = list(lastPrediction)
    lastPrediction = round(lastPrediction[0],3)
    st.info(f'The predicted Stock Close Price for the next day is $ {lastPrediction}')

def movingAverage(data):
    MA30 = pd.DataFrame()
    MA30['Adj Close'] = data['Adj Close'].rolling(window = 30).mean()
    MA100 = pd.DataFrame()
    MA100['Adj Close'] = data['Adj Close'].rolling(window = 100).mean()
    return (MA30, MA100)

def fullPlotData(data, MA30, MA100):
    fullData = pd.DataFrame()
    fullData['Adj Close'] = data['Adj Close']
    fullData['MA30'] = MA30['Adj Close']
    fullData['MA100'] = MA100['Adj Close']
    return fullData

def buy_sell(fullData):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1
    
    for i in range(len(fullData)):
        if fullData['MA30'][i] > fullData['MA100'][i]:
            if flag != 1:
                sigPriceBuy.append(fullData['Adj Close'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif fullData['MA30'][i]< fullData['MA100'][i]:
            if flag !=0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(fullData['Adj Close'][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)
    return (sigPriceBuy, sigPriceSell)

def concatData(fullData, sigPriceBuy, sigPriceSell):
    fullData['buySignal'] = sigPriceBuy
    fullData['sellSignal'] = sigPriceSell
    return fullData

def plotStrategy(data, fullData):
    adjClose = go.Scatter(x = data.Date, y = data['Adj Close'], name = 'Adj Close')
    sma30 = go.Scatter(x = data.Date, y = fullData['MA30'], name = 'MA_short')
    sma100 = go.Scatter(x = data.Date, y = fullData['MA100'], name = 'MA_long')
    buySignal = go.Scatter(mode = 'markers', x = data.Date, y = fullData.buySignal, name = 'Buy',
                        marker_symbol = 'arrow-up', marker_size=15, marker_color= 'green')
    sellSignal = go.Scatter(mode = 'markers', x = data.Date, y = fullData.sellSignal, name = 'Sell',
                            marker_symbol = 'arrow-down', marker_size=15, marker_color= 'red')
    trace = [adjClose,sma30, sma100, sellSignal, buySignal]

    layout = dict(title = 'Adjusted Close Price History Buy & Sell Signals',paper_bgcolor = 'aliceblue', plot_bgcolor = 'aliceblue')

    fig = dict(data = trace, layout = layout)
    st.plotly_chart(fig)

def imageStock(picture):
    col1, col2, col3, col4, col5= st.beta_columns(5)
    with col2:
        st.image(picture, width= 400)


def textDescription():
    st.success('The **moving average** widely used in graphical analysis of finances.')
    st.write('**With the moving average we can:**') 
    st.markdown('* *Soften the movements of price series*\n * *Identify the best price tendencies* \n * *Look for opportunities of a buy or sell according to the changes in the tendencies standards*')

    st.markdown('In this strategy, We use the **simple moving average to identify and visualize the price tendency** on a temporal series. \n\n Economic data and information have a **huge variation through time**, which makes it difficult to predict the factors that have an influence on the price movement, but almost ever **We can visualize a tendency**.\n\n The ***moving average*** helps us to understand the path that the data seem to point. With this kind of information, We can get **signals of high or low price, when buy or sell a stock**.')

    st.markdown('To **calculate a simple moving average** We just need to make the price average for a determined period on the temporal series. \n\n As the days go by, **new data will replace the eldest data on the series**, making a sample base to create an average that varies through time. \n\n On this page, you can see the moving average for a ***short period*** (the line in red - 30 days) and for a ***long period*** (the line in green - 100 days). \n\n The strategy used here is **to do a sell or buy the stock when the lines red and green cross**.')

def modelDescription():
    st.title('Creating a machine learning model to predict Stock Prices')
    st.markdown('Using an ***ensemble model*** called ***Random Forest***, We create a model to try **to predict the close price stock** for the next day.\n\n The general idea of the ensemble learning model is simple, **train multiple ML algorithms and combine their predictions**. Such an approach tends to make more accurate predictions than any individual model.\n\n ***Random Forest*** is a **Supervised learning algorithm** that is based on the ensemble learning method and many Decision Trees.')
    st.image('ensemble.jpg', use_column_width=True)
    st.title('Perfomance and Predictions')
    st.write('The model was trained with the data from **January 2020 to today**. \n\n All features are considered for training the model: \n\n * **Open price** \n\n* **High Price** \n\n* **Low Price** \n\n * **Adjusted Price** \n\n * **Volume**.\n\n The model was **improved using GridSearchCV** to find the best fit for some hyperparameters.\n\n **You can see in $ the model average error** (***RMSE***) **below:**')


    
