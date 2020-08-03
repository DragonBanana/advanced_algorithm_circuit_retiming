import plotly.express as px
import pandas as pd

df = pd.read_csv("cpu_result.csv", header=None)
df.columns = ["name", "V", "E", "time_opt_1", "std_1", "time_opt_2", "std_2"]
fig = px.scatter(df[df["name"].map(lambda x: "random_delays" in x)],
                 x="V",
                 y="E",
                 color="time_opt_2",
                 size="time_opt_1",
                 log_x=True,
                 hover_name="name",
                 size_max=50)
fig.show()

fig = px.scatter(df[df["name"].map(lambda x: "Correlator" in x)],
                 x="V",
                 y="E",
                 color="time_opt_2",
                 size="time_opt_1",
                 log_x=True,
                 hover_name="name",
                 size_max=50)
fig.show()

fig = px.scatter(df[df["name"].map(lambda x: "random_delays" not in x and "Correlator" not in x)],
                 x="V",
                 y="E",
                 color="time_opt_2",
                 size="time_opt_1",
                 log_x=True,
                 hover_name="name",
                 size_max=50)
fig.show()
fig.write_html("time_bench.html")