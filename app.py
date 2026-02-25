import streamlit as st
import plotly.express as px 
import plotly.io as pio
pio.renderers.default = "browser"

from apputil import *

# Load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
bins = [0, 12, 19, 59, 110]
labels = ["Child", "Teen", "Adult", "Senior"]

#df.head()
def survival_demographics():
    df["Age Group"]=pd.cut(df["Age"], bins=bins, labels=labels)
    grouped = (
        df.groupby(["Pclass", "Sex", "Age Group"])
          .agg(
              n_passengers=("Survived", "count"),
              n_survivors=("Survived", "sum"),
          )
          .reset_index()
    )

    # Compute survival rate
    grouped["survival_rate"] = grouped["n_survivors"] / grouped["n_passengers"]

    return grouped

survival_demographics()

st.write(
'''
# Titanic Visualization 1

'''
)
# Generate and display the figure
#Were there more female or male survivors by age group?
def visualize_demographic():
    df["Age Group"]=pd.cut(df["Age"], bins=bins, labels=labels)
    # grouped = (
    #     df.groupby(["Pclass", "Sex", "Age Group"])
    #       .agg(
    #           n_passengers=("Survived", "count"),
    #           n_survivors=("Survived", "sum"),
    #       )
    #       .reset_index()
    # )
    # grouped["survival_rate"] = grouped["n_survivors"] / grouped["n_passengers"]
    fig = px.histogram(#df,
             df[df["Survived"] ==1],                     
             x='Age Group',
             color='Sex',
             hover_data=['Name'],
             template='plotly_white',
             color_discrete_sequence=px.colors.qualitative.D3
            )
    fig.show()
    return fig

fig1 = visualize_demographic()
st.plotly_chart(fig1, use_container_width=True)

st.write(
'''
# Titanic Visualization 2
'''
)
# Generate and display the figure
fig2 = visualize_families()
st.plotly_chart(fig2, use_container_width=True)

st.write(
'''
# Titanic Visualization Bonus
'''
)
# Generate and display the figure
fig3 = visualize_family_size()
st.plotly_chart(fig3, use_container_width=True)