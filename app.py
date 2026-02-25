import streamlit as st
import plotly.express as px 
import plotly.io as pio
pio.renderers.default = "browser"

from apputil import *

"""Survival_demographics creates a new column, 'Age Group', that creates age groupings 
for the survivors from the dataset."""
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

"""Family_Groups  creates a new column called 'Family_Size' that calculates 
the family size of the passengers from the data set."""
df_family= pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

def family_groups():
    df_family['Family_Size'] = df_family['SibSp'] + df_family['Parch'] + 1
    #group by family size and passenger class
    # for ea group calculate
    # n_passengers - total num of passengers
    # avg_fare -average ticket fare 
    #min_fare, max_fare -min/max ticket faires
    grouped = (
        df_family.groupby(["Family_Size", "Pclass"])
          .agg(
              n_passengers=("PassengerId", "count"),
              avg_fare=("Fare", "mean"),
              min_fare=("Fare", "min"),
              max_fare=("Fare", "max")
          )
          .reset_index()
          .sort_values(["Pclass", "Family_Size"])
    )


    return grouped

family_groups()

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