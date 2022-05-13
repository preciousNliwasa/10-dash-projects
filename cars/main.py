import dash
from dash import dcc,html
from dash.dependencies import Input,Output
import json
import numpy as np
import plotly.graph_objs as go
import matplotlib.cm as cm
import pandas as pd

app = dash.Dash(__name__,suppress_callback_exceptions = True)

cars = pd.read_csv('cars.csv')

options = {'car_type':list(cars['car name'].unique())}

app.layout = html.Div([
        
        html.Div([
                html.Br(),
                html.Div([dcc.Dropdown(id = 'select',value = 'mazida-6-2015',options = [{'label':i,'value':i} for i in options['car_type']],style = {'position':'absolute','float':'left','width':'530px','margin-left':'20px','background-color':'aqua'})]),
                html.Div([dcc.Graph(id = 'pie',style = {'height':'600px'})],style = {'margin-top':'60px','border-style':'ridge','width':'600px','height':'600px','background-color':'rgb(10,0,25)'})
                
                ],style = {'position':'absolute','float':'left'}),
        html.Div([
                
                html.Div([dcc.Graph(id = 'gauge',style = {'height':'250px'})],style = {'position':'absolute','float':'left','width':'340px','background-color':'rgb(10,0,35)','height':'250px','border-style':'ridge'}),
                html.Div([dcc.Graph(id = 'gauge2',style = {'height':'250px'})],style = {'float':'right','width':'340px','background-color':'rgb(10,0,35)','height':'250px','border-style':'ridge'}),
                html.Div([dcc.Graph(id = 'carfig')],style = {'margin-top':'280px','width':'700px','background-color':'rgb(10,0,35)','height':'470px','border-style':'ridge'})
                
                ],style = {'float':'right'})
        ])

## copied from kaggle,peking university competition codebook -- starting

def tri_indices(simplices):
    return ([triplet[c] for triplet in simplices] for c in range(3))

def plotly_trisurf(x, y, z, simplices, colormap=cm.RdBu, plot_edges=None):

    points3D=np.vstack((x,y,z)).T
    tri_vertices=map(lambda index: points3D[index], simplices)
    zmean=[np.mean(tri[:,2]) for tri in tri_vertices ]
    min_zmean=np.min(zmean)
    max_zmean=np.max(zmean)
    facecolor=[map_z2color(zz,  colormap, min_zmean, max_zmean) for zz in zmean]
    I,J,K=tri_indices(simplices)

    triangles=go.Mesh3d(x=x, y=y, z=z,
                     facecolor=facecolor,
                     i=I, j=J, k=K,
                     name='')

    if plot_edges is None: return [triangles]
    else:
        lists_coord=[[[T[k%3][c] for k in range(4)]+[ None]   for T in tri_vertices]  for c in range(3)]
        Xe, Ye, Ze=[reduce(lambda x,y: x+y, lists_coord[k]) for k in range(3)]

        lines=go.Scatter3d(x=Xe, y=Ye, z=Ze,
                        mode='lines',
                        line=dict(color= 'rgb(50,50,50)', width=1.5))
        return [triangles, lines]
    
def map_z2color(zval, colormap, vmin, vmax):
    if vmin>vmax: raise ValueError('incorrect relation between vmin and vmax')
    t=(zval-vmin)/float((vmax-vmin))#normalize val
    R, G, B, alpha=colormap(t)
    return 'rgb('+'{:d}'.format(int(R*255+0.5))+','+'{:d}'.format(int(G*255+0.5))+\
           ','+'{:d}'.format(int(B*255+0.5))+')'
 
## ending    

@app.callback(Output('carfig','figure'),[Input('select','value')])
def carfig(select):
    
    try:
        
        with open(r"C:\Users\P'rECIOUS\car_models_json/{}.json".format(select)) as json_file:
            data = json.load(json_file)
            vertices, triangles = np.array(data['vertices']), np.array(data['faces']) - 1
    
            x, y, z = vertices[:,0], vertices[:,2], -vertices[:,1]
            graph_data = plotly_trisurf(x,y,z, triangles, colormap=cm.RdBu, plot_edges=None)
            
            # with no axis
            noaxis=dict(showbackground=True,
                        backgroundcolor='rgb(10,0,25)',
                        showline=False,
                        zeroline=False,
                        showgrid=False,
                        showticklabels=False,
                        title='')
            
            layout = go.Layout(
                    title= select,
                    font = {'color':'white'},
                    width=700, height=470,
                    paper_bgcolor = 'rgb(10,0,25)',
                    scene=dict(
                            xaxis=dict(noaxis), yaxis=dict(noaxis), zaxis=dict(noaxis),
#                      aspectratio=dict( x=1, y=2, z=0.5)
                 )
                    )
                    
            fig = dict(data = graph_data,layout = layout)
            
        return fig
    
    except Exception:
        dat = [go.Indicator(mode = 'gauge',value = 0,title = 'provide argument',name = 'volume')]
        fig = dict(data = dat)
        
        return fig
    
@app.callback([Output('gauge','figure'),Output('gauge2','figure')],[Input('select','value')])
def indicator(car):
    
    try:

        layout_ = dict(paper_bgcolor = 'rgb(10,0,25)',font = {'color':'white'})
        
        speed = cars.loc[cars['car name'] == car,'speed'].values[0]
        graph = [go.Indicator(mode = 'gauge',value = speed,title = 'Speed (km/Hr)',name = 'speed',gauge = dict(bgcolor = 'aqua'))]
        fig = dict(data = graph,layout = layout_)
            
        range_ = cars.loc[cars['car name'] == car,'range'].values[0]
        graph2 = [go.Indicator(mode = 'gauge',value = range_,title = 'Range (Km)',name = 'range',gauge = dict(bgcolor = 'lightcoral'))]
        fig2 = dict(data = graph2,layout = layout_)
        
        return fig,fig2
            
    except Exception:
        dat = [go.Indicator(mode = 'gauge',value = 0,title = 'provide argument',name = 'volume')]
        fig = dict(data = dat)
        
        return fig,fig
    
@app.callback(Output('pie','figure'),[Input('select','value')])
def pie(car):
    
    try:
        layout_ = dict(title ='cars sold' ,paper_bgcolor = 'rgb(10,0,25)',font = {'color':'white'})
        
        filtered = cars.loc[cars['car name'] == car]
        graph = [go.Pie(labels = filtered.continent,values = filtered['cars sold'],hole = 0.7)]
        fig = dict(data = graph,layout = layout_)
        
        return fig
        
    except Exception:
        dat = [go.Indicator(mode = 'gauge',value = 0,title = 'provide argument',name = 'volume')]
        fig = dict(data = dat)
        
        return fig

if __name__ == '__main__':
    app.run_server(debug = True)