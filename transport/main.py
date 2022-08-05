from dash import Dash,html,dcc,dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input,State,Output
from sklearn.cluster import KMeans
import folium
from branca.element import Figure
import openrouteservice 
from openrouteservice import convert

app = Dash(name = 'transport',prevent_initial_callbacks = True,suppress_callback_exceptions = True,external_stylesheets = [dbc.themes.BOOTSTRAP])

sidebar = dbc.Col([
            
            html.Br(),
            dbc.Row([
                    dbc.Col([html.Label(['Latitude'],style = {'color':'white'})],width = {'size':6,'offset':4})
                    ]),
            html.Br(),
            dbc.Row([
                    dbc.Col([
                            dcc.Input(id = 'lat_min',type = 'number',placeholder = 'lat min',style = {'text-align':'center','width':'100px','border-radius':'10px'},)
                            ],width = {'size':5,'offset':1}),
                    dbc.Col([
                            dcc.Input(id = 'lat_max',type = 'number',placeholder = 'lat max',style = {'text-align':'center','width':'100px','border-radius':'10px'})
                            ],width = {'size':6})
                    ]),
            html.Br(),
            dbc.Row([
                    dbc.Col([html.Label(['Longtude'],style = {'color':'white'})],width = {'size':6,'offset':4})
                    ]),
            html.Br(),
            dbc.Row([
                    dbc.Col([
                            dcc.Input(id = 'lng_min',type = 'number',placeholder = 'lng min',style = {'text-align':'center','width':'100px','border-radius':'10px'},)
                            ],width = {'size':5,'offset':1}),
                    dbc.Col([
                            dcc.Input(id = 'lng_max',type = 'number',placeholder = 'lng max',style = {'text-align':'center','width':'100px','border-radius':'10px'})
                            ],width = {'size':6})
                    ]),
            html.Br(),
            dbc.Row([
                    dbc.Col([html.Label(['Number Of Employees'],style = {'color':'white'})],width = {'size':10,'offset':2})
                    ]),
            html.Br(),
            dbc.Row([
                    dbc.Col([
                            dcc.Input(id = 'n_employees',type = 'number',placeholder = 'employees',style = {'text-align':'center','width':'100px','border-radius':'10px'},)
                            ],width = {'size':6,'offset':3})
                    ]),
            html.Hr(style = {'color':'white'}),
            dbc.Row([
                    dbc.Col([html.Label(['Number Of Groups'],style = {'color':'white'})],width = {'size':10,'offset':2})
                    ]),
            html.Br(),
            dbc.Row([
                    dbc.Col([
                            dcc.Input(id = 'clusters',type = 'number',placeholder = 'clusters',style = {'text-align':'center','width':'100px','border-radius':'10px'},)
                            ],width = {'size':6,'offset':3})
                    ]),
            html.Hr(style = {'color':'white'}),
            dbc.Row([
                dbc.Col([html.Label(['Employer Location'],style = {'color':'white'})],width = {'size':10,'offset':2})
                ]),
            html.Br(),
            dbc.Row([
                    dbc.Col([
                            dcc.Input(id = 'empl_lat',type = 'number',placeholder = 'latitude',style = {'text-align':'center','width':'100px','border-radius':'10px'},)
                            ],width = {'size':5,'offset':1}),
                    dbc.Col([
                            dcc.Input(id = 'empl_lng',type = 'number',placeholder = 'longtude',style = {'text-align':'center','width':'100px','border-radius':'10px'})
                            ],width = {'size':6})
                ]),
            html.Hr(style = {'color':'white'}),
            html.Br(),
            dbc.Row([
                    dbc.Col([
                            dbc.Button(id = 'simulate',children = ['Simulate'],n_clicks = 0,style = {'background-color':'white','color':'teal'})
                            ],width = {'size':6,'offset':3})
                    ])

            ],width = 3,style = {'background-color':'teal','position':'fixed','bottom':0,'left':0,'top':0})
        

content = dbc.Col([
        
        html.Br(),
        html.Hr(style = {'background-color':'teal','height':'5px'}),
        dbc.Row([
                
                dbc.Col([html.Iframe(id = 'employee_map',height = '332px',width = '500px')],width = 6),
                dbc.Col([html.Div(id = 'employee_dataset')],width = 6)
                
                ]),
        html.Hr(style = {'background-color':'teal','height':'5px'}),
        dbc.Row([
                
                dbc.Col([dcc.Graph(id = 'graph-clusters',style = {'height':'300px'})],width = 12)
                ]),
        html.Hr(style = {'background-color':'teal','height':'5px'}),
        dbc.Row([
                dbc.Col([html.Iframe(id = 'loc_centers_map',height = '332px',width = '500px')],width = 6),
                dbc.Col([html.Iframe(id = 'loc_routes',height = '332px',width = '500px')],width = 6)
                ]),
        html.Hr(style = {'background-color':'teal','height':'5px'})
        
        ],width = {'offset':3,'size':9})

app.layout = dbc.Container([
        
            dbc.Row([
                    sidebar,
                    content
                    ])
        ],fluid = True)

def create_dataset(lat_min : float,lat_max : float,lng_min : float,lng_max : float,n_employees:int):
    
    np.random.seed(35)
    
    employees_lat = np.random.random(1000000)
    
    lat = []
    
    for i in employees_lat:
        
        if (i + lat_min ) > lat_max:
            
            pass
            
        elif (i + lat_min ) < lat_min:
            
            pass
            
        elif ((i + lat_min ) >= lat_min) and ((i + lat_min ) <= lat_max):
            
            lat.append(i + lat_min)
       
    employees_lat = np.random.choice(lat,size = n_employees,replace = False)
    
    employees_lng = np.random.random(1000000)
    
    lng = []
    
    for i in employees_lng:
        
        if (i + lng_min ) > lng_max:
            
            pass
            
        elif (i + lng_min ) < lng_min:
            
            pass
            
        elif ((i + lng_min ) >= lng_min) and ((i + lng_min ) <= lng_max):
            
            lng.append(i + lng_min)
       
    employees_lng = np.random.choice(lng,size = n_employees,replace = False)
    
    Location = pd.DataFrame({'Lat':employees_lat,'Lng':employees_lng})
    
    return Location

def model_(clusters,dataset):
    
    model = KMeans(n_clusters = clusters)
    
    model.fit(dataset.values)
    
    return model

def with_predicted_labels(model,dataset):
    
    dataset_with_labs = dataset
    dataset_with_labs['Group'] = model.labels_
    
    return dataset_with_labs
    
    
@app.callback([Output('employee_dataset','children'),Output('employee_map','srcDoc'),Output('graph-clusters','figure'),Output('loc_centers_map','srcDoc'),Output('loc_routes','srcDoc')],
              [State('lat_min','value'),State('lat_max','value'),State('lng_min','value'),State('lng_max','value'),State('n_employees','value'),State('clusters','value'),State('empl_lat','value'),State('empl_lng','value')],
              [Input('simulate','n_clicks')]) 
def employee_dataset_(lat_min,lat_max,lng_min,lng_max,n_employees,clusters,emp_lat,emp_lng,n):
    
    employees_loc = create_dataset(float(lat_min),float(lat_max),float(lng_min),float(lng_max),int(n_employees))
    
    table =  dash_table.DataTable(columns = [
                   
               {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
               for i in employees_loc.columns
               ],
                    data = employees_loc.to_dict('records'),
                    filter_action = 'native',
                    editable = False,
                    page_size = 9,
                    sort_action = 'native',
                    sort_mode = 'multi',
                    row_selectable = 'multi',
                    column_selectable = 'multi',
                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95,'background-color':'rgb(7, 14, 26)','color':'white'},
                    style_header = {'background-color':'teal','border-color':'teal'})
    
    model = model_(clusters,employees_loc)
    
    with_labs = with_predicted_labels(model,employees_loc)
    
    map_data = folium.Map(location = [employees_loc.loc[1].Lat,employees_loc.loc[1].Lng],zoom_start = 8,control_scale = True)
    
    for i in employees_loc.index:
            
        folium.Marker(location = [employees_loc.loc[i].Lat,employees_loc.loc[i].Lng],
                      popup = 'Employee House Location',
                      tooltip = 'Employee {} location'.format(i),
                      icon = folium.Icon(icon = 'bed',icon_color = 'white',prefix = 'fa')).add_to(map_data)
    
    folium.LatLngPopup().add_to(map_data)
    
    fig = Figure()   
         
    fig.add_child(map_data)
        
    fig.save('employees_loc.html')
    
    map_data2 = folium.Map(location = [employees_loc.loc[1].Lat,employees_loc.loc[1].Lng],zoom_start = 14,control_scale = True)
    
    colors = {0:'blue',1:'gold',2:'green',3:'orange',4:'yellow',5:'purple'}
    
    for i in list(range(len(model.cluster_centers_))):
        
        folium.Circle(location = [model.cluster_centers_[i][0],model.cluster_centers_[i][1]],radius = 3800,fill = True,fill_color = colors[i],tooltip = 'Group {} Area'.format(i)).add_to(map_data2)
    
    fig2 = Figure()   
         
    fig2.add_child(map_data2)
        
    fig2.save('centers.html')
    
    map_data3 = folium.Map(location = [employees_loc.loc[1].Lat,employees_loc.loc[1].Lng],zoom_start = 14,control_scale = True)
    
    
    client = openrouteservice.Client(key='put your key')
    
    coords = [[emp_lng,emp_lat]]
    
    for i in list(range(len(model.cluster_centers_))):
        
        coords.append([model.cluster_centers_[i][1],model.cluster_centers_[i][0]])
        folium.Marker(location = [model.cluster_centers_[i][0],model.cluster_centers_[i][1]],icon = folium.Icon(icon = 'users',prefix = 'fa',icon_color = 'white'),tooltip = 'Group {} Area'.format(i)).add_to(map_data3)

    folium.Marker(location = [emp_lat,emp_lng],tooltip = 'Work Center',icon = folium.Icon(icon = 'money',prefix = 'fa',icon_color = 'white')).add_to(map_data3)
    
    res = client.directions(coords,optimize_waypoints=True)
    geometry = client.directions(coords,optimize_waypoints=True)['routes'][0]['geometry']
    decoded = convert.decode_polyline(geometry)
        
    distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
    duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"
        
    folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(map_data3)
    
    fig3 = Figure()   
     
    fig3.add_child(map_data3)
    
    fig3.save('routes.html')
    
    graph_data = []
    
    for i in np.unique(model.labels_):
        
        graph_data.append(go.Scatter(x = with_labs.loc[with_labs['Group'] == i].Lat,y = with_labs.loc[with_labs['Group'] == i].Lng,mode = 'markers',marker = dict(size = 7),name = 'Group {}'.format(i)))
    
    layout = go.Layout(title = 'Location Clusters',xaxis = dict(title = 'Latitude'),yaxis = dict(title = 'Longtude'))
    
    graph = dict(data = graph_data,layout = layout)
    
    return table,open('employees_loc.html','r').read(),graph,open('centers.html','r').read(),open('routes.html','r').read()


if __name__ == '__main__':
    app.run_server(debug = True)
