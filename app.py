#ABMPC-USA
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Must be called first.
st.set_page_config(
    layout="wide", # 'centered' or 'wide'
    page_title='ABMPC-USA',
    menu_items={
        'About': "This is a shareable data application. Visit https://www.transmissionvamp.com."
    }
)

header = st.container()
dataset = st.container()
model = st.container()
footer = st.container()

with header:
    st.title('Agent-Based Model Choice USA (ABMPC-USA)')

    if 'disclaimer' not in st.session_state:
        st.session_state.disclaimer = False

with dataset:
    data_url = ('https://danodriscoll.github.io/abmpc-usa/abmpc-real-us-03.csv')
    
    @st.cache
    def load_data(nrows):
        data = pd.read_csv(data_url, nrows=nrows)
        return data

with model:
    colA, colB = st.columns(2)
    with colA:
        st.write("ABMPC output consuming United States of America government expenditures and (primary) discount-rate spanning financial year 1974 to present day.")

    with colB:    
        st.text("Model Run: 07th July 2022")
        disclaimer = st.checkbox("Disclaimer: I accept it's not investment advice.")
        if disclaimer:
            st.session_state.disclaimer = True

    with st.expander("Model Parameters"):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Government", "1")
        col2.metric("Central Bank", "1")
        col3.metric("Producers", "1")
        col4.metric("Consumers", "1")


        col5, col6, col7 = st.columns(3)
        col5.metric("Tax Rate", "37%")
        col6.metric("Consumption Disposable", "60%")
        col7.metric("Consumption Opening", "40%")

    col8, col9 = st.columns(2)

    with col8:
        if st.session_state.disclaimer:
            st.write("Hover over a specific chart for options. View fullscreen and select (unselect) categories.")
        else:
            st.write("Please accept the disclaimer to view chart data.")

    with col9:
        finQuarters = 193 # Default number of financial quarters to show.
        quarters = st.slider("Financial Quarters", min_value=16, max_value=200, value=finQuarters, step=2)

    # Load data if disclaimer is accepted.
    if st.session_state.disclaimer:
        df = load_data(quarters)
    else:        
        df = load_data(0)
    
    # Model Bills (Money) Supply Velocity & Real-World Bond Yields
    st.header("Money Supply Velocity")

    st.write("The change, from one financial period to the next, in net-financial asset flows as a percentage of income (GDP).")

    goFig = go.Figure()
    goFig.add_trace(go.Scatter(x=df.date, y=df.velocity_bills_issued_as_percent_gdp,
        mode='lines+markers',
        name='Bills Velocity'
    ))
    goFig.add_trace(go.Scatter(x=df.date, y=df.bills_supply_trend,
        mode='lines',
        name='Bills Trend',
        opacity=0.6
    ))
    goFig.add_trace(go.Scatter(x=df.date, y=df.value,
        mode='lines+markers',
        name='Bond Yield'
    ))
    goFig.add_trace(go.Scatter(x=df.date, y=df.value_trend,
        mode='lines',
        name='Bond Trend',
        opacity=0.6
    ))    

    goFig.update_layout(
        margin=dict(l=50,r=50,b=50,t=50),
        template="gridon",
        xaxis_title="Financial Quarters",
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Percent',
            titlefont_size=16,
            tickfont_size=14,
        ),        
        showlegend=True,
        title=go.layout.Title(
            text="Model Bills Issued (Money) Velocity As Percent Of Model GDP & Real-World USA 10-Year Bond-Yields",
            xref="paper",
            x=0
        )
    )

    st.plotly_chart(goFig, use_container_width=True, sharing='streamlit')

    # Fiscal Balance
    st.header("Fiscal Balance")

    st.write("This is the government sector fiscal balance, either in surplus (a money flow away from the Non-Government sector), or more typically, in deficit (a money flow toward the Non-Government sector).")

    goFig1 = go.Figure()
    values = list(df.fiscal_balance)
    goFig1.add_trace(go.Bar(x=df.date, y=df.fiscal_balance,
        marker=dict(
            color=values,
            colorscale="Rdbu", 
        )
    ))

    goFig1.update_layout(
        margin=dict(l=50,r=50,b=50,t=50),
        template="gridon",
        xaxis_title="Financial Quarters",
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='USD',
            titlefont_size=16,
            tickfont_size=14,
        ),
        showlegend=False,
        title=go.layout.Title(
            text="Model Fiscal Balance: The Flow of Net-Financial Assets from Government to the Domestic Sector",
            xref="paper",
            x=0
        )
    )

    st.plotly_chart(goFig1, use_container_width=True, sharing='streamlit')
    
    st.header("Data Citation")
    st.write("The model consumes real-world USA government expenditure and (primary) discount-rate time-series data.")
    st.subheader("Expenditure")
    st.write("U.S. Bureau of Economic Analysis, Real Government Consumption Expenditures and Gross Investment [GCEC1], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/GCEC1")
    st.subheader("Interest on Bills")
    st.write("International Monetary Fund, Interest Rates, Discount Rate for United States [INTDSRUSM193N], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/INTDSRUSM193N")
    st.markdown("---")
    st.caption("For Reference:")
    st.subheader("Bond-Yields")
    st.write("Organization for Economic Co-operation and Development, Long-Term Government Bond Yields: 10-year: Main (Including Benchmark) for the United States [IRLTLT01USQ156N], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/IRLTLT01USQ156N")

with footer:
    st.caption("Visit the [TransmissionVamp](https://www.transmissionvamp.com) website.")
