import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('final_startup_funding.csv')
#st.dataframe(df)

def load_overall_analysis():
    st.title('Overall Analysis')
    total_amt= round(df['amount'].sum())
    max_amt = round(df['amount'].max())
    avg_amt = round(df['amount'].mean())
    c = round(df['startup'].nunique())

    col1,col2,col3,col4= st.columns(4)
    with col1:
        st.metric('Total',str(total_amt)+'cr')

    with col2:
        st.metric('Max', str(max_amt) + 'cr')

    with col3:
        st.metric('Avg', str(avg_amt) + 'cr')

    with col4:
        st.metric('No Of Startup', c)


    df['date']= pd.to_datetime(df['date'])
    df['year']= df['date'].dt.year
    df['month']= df['date'].dt.month
    st.header('Month on Month Analysis')
    selected_option= st.selectbox('Select Type',['Total','Count'])

    if selected_option == 'Total':
        temp = df.groupby(['year', 'month'])['amount'].sum().reset_index()

    else:
        temp = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp['x_axis'] = temp['month'].astype(str) + '-' + temp['year'].astype(str)

    fig, ax = plt.subplots()
    ax.plot(temp['x_axis'], temp['amount'])
    plt.xticks(fontsize=6, rotation=90)
    plt.yticks(fontsize=6)
    st.pyplot(fig)




def load_investor(investor):
    st.title(investor)

    # last 5 investment of investor
    last_df=df[df['investors'].str.contains(investor)][['date', 'startup', 'industry', 'subvertical', 'city', 'round', 'amount']].sort_values(by='date', ascending=False).head()
    st.dataframe(last_df)

    col1,col2 = st.columns(2)
    with col1:
        big_invest= df[df['investors'].str.contains(investor)].groupby(['startup'])['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        st.dataframe(big_invest,width=300,height=200)
    with col2:
        st.subheader('Biggest Investment')
        fig,ax=plt.subplots()
        ax.bar(big_invest.index, big_invest.values)
        plt.xticks(fontsize=15,rotation=90)
        plt.yticks(fontsize=15)
        st.pyplot(fig)

    col1,clo2 = st.columns(2)
    with col1:
        invest_vert= df[df['investors'].str.contains(investor)].groupby(['subvertical'])['amount'].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.pie(invest_vert.values, labels=invest_vert.index, autopct='%0.2f%%')
        # plt.xticks(fontsize=15, rotation=90)
        # plt.yticks(fontsize=15)
        st.pyplot(fig)

    with col2:
        invest_city = df[df['investors'].str.contains(investor)].groupby(['city'])['amount'].sum().sort_values(
            ascending=False).head()
        fig, ax = plt.subplots()
        ax.pie(invest_city.values, labels=invest_city.index, autopct='%0.2f%%')
        # plt.xticks(fontsize=15, rotation=90)
        # plt.yticks(fontsize=15)
        st.pyplot(fig)


    df['date']= pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    st.subheader('Investing trend of investors year of year')


    yoy= df[df['investors'].str.contains(investor)].groupby(['year'])['amount'].sum().sort_values(ascending=False).head()
    fig, ax = plt.subplots()
    ax.plot(yoy.index, yoy.values, marker='o', markersize=5, color='yellow')
    plt.xticks(fontsize=15, rotation=90)
    plt.yticks(fontsize=15)
    st.pyplot(fig)


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investors'])

if option == 'Overall Analysis':
    #st.title('Overall Analysis')
    load_overall_analysis()

elif option == 'Startup':
    #st.title('Startup')
    st.sidebar.selectbox('Select Startup', sorted(set(df['startup'].unique())))
    btn1=st.sidebar.button('Find Startup Detail')
    if btn1:
        st.title('Startup')



else:
    #st.title('Investors')
    selected_investor= st.sidebar.selectbox('Select Investors', sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investors Detail')
    if btn2:
        #st.title('Investors')
        load_investor(selected_investor)







