import streamlit as st 
from dataAnalysis import *
from machineLearning import *
from aboutMe import *

st.set_page_config( page_title= 'Stock Price Analysis', page_icon= 'logo.png')
 
#st.sidebar.info('# Navigation Sidebar')

pag = st.sidebar.radio('Select a page',['Data Analysis','Machine Learning','About Me'], index = 0)


if pag == 'Data Analysis':
    st.title('Data Analysis - Stock Price Variation')
    imageStock('stock.jpg')
    dataAnalysisText()
    try:
        startDate = get_period() 
        data = upload_file(startDate)              
        check = st.checkbox('Please click here to view the Data')
        if check:
            view_data(data)
        
        linechart_prices(data)
        candlestick(data)
        linechart_volume(data)
        last_value(data)
        avg_value(data)
        percent(data)
    except:
        st.error('No data in the selectioned period. Please choose another day to start the view') 

elif pag == 'Machine Learning':
    st.title('Moving Average Strategy')
    imageStock('stock2.jpg')
    textDescription()
    data = chooseData()
    MA30,MA100 = movingAverage(data)
    fullData = fullPlotData(data, MA30, MA100)
    sigPriceBuy, sigPriceSell = buy_sell(fullData)
    fullData = concatData(fullData, sigPriceBuy, sigPriceSell)
    plotStrategy(data, fullData)

    modelDescription()
    
    x_train, x_test, y_train, y_test = trainTestData(data)
    model = trainingModel(x_train, y_train)
    testingModel(model, x_test, y_test)
    st.markdown('**You can find the predicted value for the next day below:**')
    prediction(data, model)

elif pag == 'About Me':
    descriptionAuthor()
