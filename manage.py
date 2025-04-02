import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv("micro_world.csv", encoding='ISO-8859-1')
    return df

df = load_data()

st.title("Global Financial Behavior")
st.caption("*Data Source: Global Findex 2021 - World Bank*")

# Renaming the Region Mapping for a proper and better visualization structure
region_mapping = {
    "East Asia & Pacific (excluding high income)": "East Asia &<br>Pacific",
    "Europe & Central Asia (excluding high income)": "Europe &<br>Central Asia",
    "Latin America & Caribbean (excluding high income)": "Latin America &<br>Caribbean",
    "Middle East & North Africa (excluding high income)": "Middle East &<br>North Africa",
    "South Asia": "South Asia",
    "Sub-Saharan Africa (excluding high income)": "Sub-Saharan Africa",
    "High income": "High-Income<br>Economies"
}

df['regionwb'] = df['regionwb'].replace(region_mapping)
df.rename(columns={'regionwb': 'World Bank Region'}, inplace=True)

# Visualization 1: Savings Behavior Across Regions
st.subheader("Savings Behavior Across World Bank Regions")
st.caption("*How many people save money in different regions?*")
savings_distribution = df.groupby("World Bank Region")["saved"].mean().reset_index()
savings_distribution["saved"] *= 100  

fig1 = px.bar(
    savings_distribution, x="World Bank Region", y="saved",
    title="Percentage of Population Saving Money by Region",
    labels={'saved': 'Savings Rate (%)'},
    color_discrete_sequence=['#1f77b4'],  
    text=savings_distribution["saved"].round(0).astype(int), 
    range_y=[0, 100]  
)

fig1.update_traces(textposition="outside")  
fig1.update_layout(
    width=2000,
    xaxis=dict(tickangle=0, tickfont=dict(size=11)),
    bargap=0.3
)

st.plotly_chart(fig1)

st.caption("*Note: Regions such as East Asia & Pacific, Europe & Central Asia, Latin America & Caribbean, Middle East & North Africa, South Asia, and Sub-Saharan Africa exclude high-income economies.*")

st.markdown("**Insight:** High-income economies lead in savings (74%), while South Asia has the lowest rate (27%), highlighting financial accessibility differences across regions.")

# Visualization 2: Borrowing Behavior Across Regions
st.subheader("Borrowing Trends Across World Bank Regions")
st.caption("*How many people borrow money in different regions?*")

borrowing_behavior = df.groupby("World Bank Region")["borrowed"].mean().reset_index()
borrowing_behavior["borrowed"] *= 100  

fig2 = px.bar(
    borrowing_behavior, x="World Bank Region", y="borrowed",
    title="Borrowing Rate by Region",
    labels={'borrowed': 'Borrowing Rate (%)'},
    color_discrete_sequence=['#d62728'], 
    text=borrowing_behavior["borrowed"].round(0).astype(int),
    range_y=[0, 100]  
)

fig2.update_traces(textposition="outside")
fig2.update_layout(
    width=2000,
    xaxis=dict(tickangle=0, tickfont=dict(size=11)),
    bargap=0.3
)

st.plotly_chart(fig2)

st.caption("*Note: Regions such as East Asia & Pacific, Europe & Central Asia, Latin America & Caribbean, Middle East & North Africa, South Asia, and Sub-Saharan Africa exclude high-income economies.*")

st.markdown("**Insight:** Borrowing rates vary significantly across regions, reflecting differences in financial inclusion, access to credit, and economic conditions.")

import streamlit as st
import pandas as pd
import plotly.express as px

# Visualization 3: Age vs. Savings Behavior 
st.subheader("How Age Affects Saving Habits")
st.caption("*Savings rates peak in early adulthood but decline with age.*")

df['age_group'] = pd.cut(
    df['age'], 
    bins=[15, 25, 35, 45, 55, 65, 75, 85, 95], 
    labels=["15-25", "26-35", "36-45", "46-55", "56-65", "66-75", "76-85", "86-95"]
)

age_savings_trend = df.groupby("age_group")["saved"].mean().reset_index()

fig3 = px.line(
    age_savings_trend, x="age_group", y="saved",
    title="Impact of Age on Savings (Grouped Age Brackets)",
    labels={'age_group': 'Age Group', 'saved': 'Savings Rate (%)'},
    markers=True,
    color_discrete_sequence=['#17becf'],
    line_shape="spline"  
)

fig3.update_traces(marker=dict(size=8))
fig3.update_layout(
    xaxis=dict(title="Age Group", tickangle=0, tickfont=dict(size=12)), 
    yaxis=dict(
        title="Average Savings Rate (%)",
        tickfont=dict(size=12), 
        range=[0.4, 0.6],  
        tickvals=[0.4, 0.45, 0.5, 0.55, 0.6],  
        tickformat=".0%" 
    ),
    width=900, height=500
)

max_point = age_savings_trend.loc[age_savings_trend["saved"].idxmax()]
min_point = age_savings_trend.loc[age_savings_trend["saved"].idxmin()]

fig3.add_annotation(
    x=max_point["age_group"], y=max_point["saved"],
    text=f"Peak: {max_point['saved']:.2%}", showarrow=True, arrowhead=2
)

fig3.add_annotation(
    x=min_point["age_group"], y=min_point["saved"],
    text=f"Low: {min_point['saved']:.2%}", showarrow=True, arrowhead=2
)

st.plotly_chart(fig3)

st.write("**Insight:** Savings rates peak in early adulthood (26-35 years) and gradually decline with age, reaching the lowest point in the 86-95 age group.")

# Visualization 4: Digital Payment Usage
st.subheader("Digital Payment Adoption by Region")
st.caption("*How popular are digital payments around the world?*")

digital_payment_data = df.groupby("World Bank Region")["anydigpayment"].mean().reset_index()
digital_payment_data["anydigpayment"] *= 100  

fig4 = px.bar(
    digital_payment_data, x="World Bank Region", y="anydigpayment",
    title="Digital Payment Usage by Region",
    labels={'anydigpayment': 'Digital Payment Usage (%)'},
    color_discrete_sequence=['#2ca02c'],
    text=digital_payment_data["anydigpayment"].round(0).astype(int), 
    range_y=[0, 100]
)

fig4.update_traces(textposition="outside")
fig4.update_layout(
    width=2000,
    xaxis=dict(tickangle=0, tickfont=dict(size=11)),
    bargap=0.3
)

st.plotly_chart(fig4)

st.caption("*Note: Regions such as East Asia & Pacific, Europe & Central Asia, Latin America & Caribbean, Middle East & North Africa, South Asia, and Sub-Saharan Africa exclude high-income economies.*")

st.markdown("**Insight:** Digital payment adoption is highest in high-income economies (95%), reflecting strong financial infrastructure, while South Asia has the lowest (36%), likely due to limited access to digital financial services.")

# Visualization 5: Income Level & Borrowing Trends
st.subheader("Does Income Level Affect Borrowing?")
st.caption("*Do richer people borrow more than poorer ones?*")

income_borrowing = df.groupby("inc_q")["borrowed"].mean().reset_index()

income_borrowing["borrowed"] = income_borrowing["borrowed"] * 100 

fig5 = px.line(
    income_borrowing, x="inc_q", y="borrowed",
    title="Borrowing Rate by Income Quartile",
    labels={'inc_q': 'Income Quartile (1 = Lowest, 5 = Highest)', 'borrowed': 'Borrowing Rate (%)'},
    markers=True,  
    color_discrete_sequence=['#ff7f0e'],  
    line_shape="spline" 
)

fig5.update_traces(marker=dict(size=8))  

fig5.update_layout(
    xaxis=dict(
        title="Income Quartile (1 = Lowest, 5 = Highest)",  
        tickangle=0,  
        tickfont=dict(size=12)  
    ),
    yaxis=dict(
        title="Borrowing Rate (%)",  
        tickfont=dict(size=12),  
        range=[40, 60],  
        tickvals=[40, 45, 50, 55, 60],  
        ticktext=["40%", "45%", "50%", "55%", "60%"]
    ),
    width=900, height=500 
)

max_point = income_borrowing.loc[income_borrowing["borrowed"].idxmax()]
min_point = income_borrowing.loc[income_borrowing["borrowed"].idxmin()]

fig5.add_annotation(
    x=max_point["inc_q"], y=max_point["borrowed"],
    text=f"Highest: {max_point['borrowed']:.1f}%", showarrow=True, arrowhead=2
)

fig5.add_annotation(
    x=min_point["inc_q"], y=min_point["borrowed"],
    text=f"Lowest: {min_point['borrowed']:.1f}%", showarrow=True, arrowhead=2
)

st.plotly_chart(fig5)

st.markdown("**Insight:** Borrowing rates increase as income levels rise, with the highest income group borrowing the most.")


