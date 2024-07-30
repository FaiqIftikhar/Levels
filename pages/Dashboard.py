import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import utils


st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dashboard")

st.markdown("""
            **This page can tell you an interesting story ⛩️.**
            """)

# st.set_page_config()

countries = utils.COUNTRIES

sales_data = pd.read_csv("Salary_Data.csv")
Wage_Yearly = []
Wage_Monthly = []
Wage_Hourly = []
for idx, rows in sales_data.iterrows():
    if rows['Wage Unit'] == 'Yearly':
        Wage_Yearly.append(rows['Salary'])
        Wage_Monthly.append(rows['Salary']/12)
        Wage_Hourly.append(rows['Salary']/(52.143*rows['Number of Hours']))
    elif rows['Wage Unit'] == 'Monthly':
        Wage_Yearly.append(rows['Salary']*12)
        Wage_Monthly.append(rows['Salary'])
        Wage_Hourly.append(rows['Salary']/(4.345*(rows['Number of Hours'])))
    elif rows['Wage Unit'] == 'Hourly':
        Wage_Yearly.append(rows['Salary']*(52.143*rows['Number of Hours']))
        Wage_Monthly.append(rows['Salary']*(4.345*rows['Number of Hours']))
        Wage_Hourly.append(rows['Salary'])

sales_data['Wage_Monthly'] = Wage_Monthly
sales_data['Wage_Yearly'] = Wage_Yearly
sales_data['Wage_Hourly'] = Wage_Hourly

regions = ["LATAM", "EMEA", "NA", "APAC"]

colors = [
    "#aa423a",
    "#f6b404",
    "#327a88",
    "#303e55",
    "#c7ab84",
    "#b1dbaa",
    "#feeea5",
    "#3e9a14",
    "#6e4e92",
    "#c98149",
    "#d1b844",
    "#8db6d8",
]
months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

@st.cache_data
def get_data():
    dates = pd.date_range(start="1/1/2022", end="12/31/2022")
    data = pd.DataFrame()
    sellers = {
        "LATAM": ["S01", "S02", "S03"],
        "EMEA": ["S10", "S11", "S12", "S13"],
        "NA": ["S21", "S22", "S23", "S24", "S25", "S26"],
        "APAC": ["S31", "S32", "S33", "S34", "S35", "S36"],
    }
    rows = 25000
    data["transaction_date"] = np.random.choice([str(i) for i in dates], size=rows)
    data["region"] = np.random.choice(regions, size=rows, p=[0.1, 0.3, 0.4, 0.2])
    data["transaction_amount"] = np.random.uniform(100, 250000, size=rows).round(2)
    data["seller"] = data.apply(
        lambda x: np.random.choice(sellers.get(x["region"])), axis=1
    )
    return data.sort_values(by="transaction_date").reset_index(drop=True)




# st.title("2022 Sales Dashboard")

pivot0 = st.sidebar.selectbox('You can select the country here:', options=sales_data['Country'].unique(), index= 0)
pivot1 = st.sidebar.selectbox('You can select wage unit here:', options=['Yearly', 'Monthly', 'Hourly'], index=0)
pivot2 = st.sidebar.selectbox('You can select working hours here:', options=['Full Time', 'Part Time'], index=0)
pivot3 = st.sidebar.selectbox('You can select here the key column:', options=['City', 'Gender', 'Job Title', 'Tag'])

# sales_data = pd.read_csv("Salary_Data.csv")



sales_data['OG_Salary'] = sales_data['Salary']
sales_data['OG_Wage_Unit'] = sales_data['Wage Unit']

sales_data = sales_data[sales_data['Country'] == pivot0]
if pivot1 == 'Yearly':
    sales_data['Salary'] = sales_data['Wage_Yearly']
    sales_data['Wage Unit'] = 'Yearly'
elif pivot1 == 'Monthly':
    sales_data['Salary'] = sales_data['Wage_Monthly']
    sales_data['Wage Unit'] = 'Monthly'
elif pivot1 == 'Hourly':
    sales_data['Salary'] = sales_data['Wage_Hourly']
    sales_data['Wage Unit'] = 'Hourly'

if pivot2 == 'All':
    upper_bound, lower_bound = 60, 0
elif pivot2 == 'Full Time':
    upper_bound, lower_bound = 40, 20
elif pivot2 == 'Part Time':
    upper_bound, lower_bound = 20, 0


data = sales_data[(sales_data['Number of Hours'] <= upper_bound) & (sales_data['Number of Hours'] > lower_bound)]


# st.dataframe(get_data())

regions = sales_data[pivot3].unique()

months = list(sales_data.columns)[1:]

# st.write(f"REGIONS:\n{regions}")

# st.write(f"Pivot3:\n{pivot3}")
# st.dataframe(data)

region_select = alt.selection_point(fields=[pivot3])
region_pie = (
    (
        alt.Chart(data)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(
                "Salary",
                type="quantitative",
                aggregate="count",
                title="Number of Input data points",
            ),
            color=alt.Color(
                field=pivot3,
                type="nominal",
                scale=alt.Scale(domain=regions, range=colors),
                title=pivot3,
            ),
            opacity=alt.condition(region_select, alt.value(1), alt.value(0.25)),
        )
    )
    .add_params(region_select)
    .properties(width=300,
                #  title=f"Salaries by {pivot3}"
                 )
)
# st.write(alt.FontStyle)
region_summary = (
    (
        alt.Chart(data)
        .mark_bar(cornerRadiusEnd=20)
        .encode(
            xOffset=f"{pivot3}:N",
            x=alt.X(
                "Level",
                type="nominal",
                sort=['Fresh Graduate', 'Junior', 'Associate', 'Senior']
            ),
            y=alt.Y(
                field="Salary",
                type="quantitative",
                aggregate="mean",
                title="Average Salary",
                
            ),
            color=alt.Color(
                pivot3,
                type="nominal",
                # title="Cities",
                scale=alt.Scale(domain=regions, range=colors),
                legend=alt.Legend(
                    direction="vertical",
                    orient='right',
                    # legendY=0.5,
                    # legendX=1050,
                    titleColor="#8db6d8",
                    titleFontSize=35,
                    titleFontWeight=900,
                    titleLimit=200,
                    titleLineHeight=10,
                    # fontWeight=900,
                    # clipHeight=1,
                    # columns=8,
                    rowPadding=10,
                    # titleAnchor='middle',
                    
                    symbolType="circle",
                    tickCount=4,
                ),
            ),
        )
    )
    .transform_filter(region_select)
    .properties(width=650)
)

top_row = region_pie | region_summary
st.altair_chart(top_row)
