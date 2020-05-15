import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import random
import numpy as np


def generateYValues():
    listY = []
    for i in range(10):
        y_input = [random.randint(1,50) for x in range(101)]
        y_input[0] = 0
        listY.append(y_input)
    return listY

x_input = list(range(101))
y_list = generateYValues()

# ----------------- create and plot 10 plots ---------------------------

def plotFigures():
    figures = []
    for i in range(10):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_input, y=[],
                                 mode='lines',
                                 name='lines'))
        fig.update_layout(
            xaxis=dict(nticks=int(len(x_input) / 2.5), range=[0, len(x_input) - 1], showgrid=False),
            yaxis=dict(nticks=int(len(y_list[i]) / 10), range=[0, max(y_list[i])], showgrid=False),
            plot_bgcolor='#DCDCDC'
        )
        figures.append(fig)
    return figures

allFigures = plotFigures()


# prepare multiple graphs
output = [html.H3(children='Multiple color plots'),
            dcc.Slider(id='slider_input', min=0, max=100, step=1, value=0)]

for i in range(10):
     output.append(dcc.Graph(id='fig'+str(i),figure=allFigures[i],style={
            'height': 350,
            'width': 1200
        },))


app = dash.Dash()
app.layout = html.Div(children=output)

randomColors=["red","SeaGreen","yellow","pink","LightSalmon","orange","aquamarine","bisque","coral","cyan"]

def build(size, index):
    l=list()
    for i in np.arange(1,size+1,0.25):
        l.append(dict(
                type="rect",
                xref="x",
                yref="y",
                x0=i-1,
                x1=i,
                y0=0,
                y1=max(y_list[index]),
                fillcolor=randomColors[random.randint(0,9)],
                opacity=random.uniform(0.1,0.6),
                layer="below",
                line_width=0,
            ))
    return l



callBackOutputs = []
for i in range(10):
    callBackOutputs.append(Output('fig'+str(i), 'figure'))


@app.callback(callBackOutputs,
             [Input('slider_input', 'value')])
def update_plot(slider_input):
    print("slider input is " + str(slider_input))
    outputFigures = []
    if slider_input > 0:
        for i in range(10):
            figure = go.Figure()
            x_update = x_input[0:len(x_input) + 1]
            y_update = y_list[i][0:int(slider_input) + 1]
            figure.add_trace(go.Scatter(x=x_update, y=y_update,
                                        mode='lines', line={'dash': 'solid', 'color': 'black'},
                                        name='lines'))
            figure.update_layout(xaxis=dict(
                nticks=int(len(x_input) / 2.5), range=[0, len(x_input) - 1], showgrid=False),
                yaxis=dict(nticks=int(len(y_list[i]) / 10), range=[0, max(y_list[i])], showgrid=False),
                plot_bgcolor='#DCDCDC',
                shapes=build(slider_input, i)
            )
            outputFigures.append(figure)
        return outputFigures
    else:
        return allFigures

app.run_server(debug=True, use_reloader=False)