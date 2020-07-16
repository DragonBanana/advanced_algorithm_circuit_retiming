import plotly.express as px
import pandas as pd

label="t_1"

df = pd.read_csv("result.csv", header=None)
df.columns = ["name", "V", "E", "t_1", "s_1", "t_2", "s_2"]
fig = px.scatter(df[df["name"].map(lambda x: "random_delays" in x)],
                 x="V",
                 y="E",
                 color="t_2",
                 size="t_1",
                 log_x=True,
                 hover_name="name",
                 size_max=50)
fig.show()

fig = px.scatter(df[df["name"].map(lambda x: "Correlator" in x)],
                 x="V",
                 y="E",
                 color="t_2",
                 size="t_1",
                 log_x=True,
                 hover_name="name",
                 size_max=50)
fig.show()

fig = px.scatter(df[df["name"].map(lambda x: "random_delays" not in x and "Correlator" not in x)],
                 x="V",
                 y="E",
                 color="t_2",
                 size="t_1",
                 log_x=True,
                 hover_name="name",
                 size_max=50)
fig.show()