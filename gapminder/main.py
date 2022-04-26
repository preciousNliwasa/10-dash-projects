import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.graph_objs as go
import dash_table
from plotly.data import gapminder 
import plotly.express as px


table = gapminder()
table2 = table.drop(['iso_alpha','iso_num'],axis = 'columns')

option_all = {'continent':list(table.continent.value_counts().index),'year':list(table.year.value_counts().index)}

app = dash.Dash(__name__,suppress_callback_exceptions = True)

app.layout = html.Div([
        
            html.Div([
                    html.Div([
                            
                            dcc.Graph(id = 'bar1',style = {'position':'absolute','float':'left','width':'50%','height':'25%'}),
                            dcc.Graph(id = 'box1',style = {'float':'right','width':'50%','height':'25%'}),
                            html.Div([
                                    
                                    html.Div([dcc.Graph(id = 'mapp',figure = {},style = {'height':'100%'})],style = {'position':'absolute','float':'left','width':'550px','height':'650px','background-color':'white'}),
                                    html.Div([
                                            
                                            dcc.Graph(id = 'pie',style = {'width':'450px','height':'340px'}),
                                            dcc.Graph(id = 'box2',style = {'width':'450px','height':'310px'})
                                            
                                            ],style = {'position':'absolute','left':'570px','width':'450px','height':'600px','background-color':'white'})
                                    
                                    ],style = {'position':'absolute','top':'340px'}),
                            html.Div([
                                    
                                    dcc.Graph(id = 'hist',style = {'position':'absolute','height':'300px','width':'1030px'})
                                    ],style = {'background-color':'white','width':'100%','position':'absolute','top':'1000px','height':'300px'})
                            
                            ],style = {'position':'absolute','float':'left','width':'1030px','margin-left':'15px','height':'1300px','background-color':'white','border-style':'ridge'}),
                    html.Div([
                            
                            html.H3('Continent',style = {'text-align':'center','color':'white'}),
                            dcc.Dropdown(id = 'dropcont',value = 'Africa',options = [{'label':i,'value':i} for i in option_all['continent']],style = {'width':'70%','margin-left':'30px'}),
                            html.H3('Parameter',style = {'text-align':'center','color':'white'}),
                            dcc.Dropdown(id = 'droppara',value = 'pop',options = [{'label':'Population','value':'pop'},{'label':'GDP per capita','value':'gdpPercap'},{'label':'Life Expectancy','value':'lifeExp'}],style = {'width':'70%','margin-left':'30px'}),
                            html.H3('Plot 2 type',style = {'text-align':'center','color':'white'}),
                            dcc.RadioItems(id = 'boxovio',value = 'violin',options = [{'label':'violin','value':'violin'},{'label':'boxplot','value':'boxplot'}],style = {'width':'70%','margin-left':'40px','color':'white'}),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Hr(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.H3('Year',style = {'text-align':'center','color':'white'}),
                            dcc.Dropdown(id = 'yeardrop',value = 1952,options = [{'label':i,'value':i} for i in option_all['year']],style = {'width':'70%','margin-left':'30px'}),
                            html.H3('Parameter',style = {'text-align':'center','color':'white'}),
                            dcc.Dropdown(id = 'droppara2',value = 'pop',options = [{'label':'Population','value':'pop'},{'label':'GDP per capita','value':'gdpPercap'},{'label':'Life Expectancy','value':'lifeExp'}],style = {'width':'70%','margin-left':'30px'}),
                            html.H3('Plot 2 type',style = {'text-align':'center','color':'white'}),
                            dcc.RadioItems(id = 'boxovio2',value = 'violin',options = [{'label':'violin','value':'violin'},{'label':'boxplot','value':'boxplot'}],style = {'width':'70%','margin-left':'40px','color':'white'}),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Hr(),
                            html.H3('Continent',style = {'text-align':'center','color':'white'}),
                            dcc.Dropdown(id = 'contlast',value = 'Africa',options = [{'label':i,'value':i} for i in option_all['continent']],style = {'width':'70%','margin-left':'30px'}),
                            html.H3('Year',style = {'text-align':'center','color':'white'}),
                            dcc.Dropdown(id = 'yearlast',value = 1952,options = [{'label':i,'value':i} for i in option_all['year']],style = {'width':'70%','margin-left':'30px'}),
                            html.H3('Parameter',style = {'text-align':'center','color':'white'}),
                            dcc.Dropdown(id = 'para3',value = 'pop',options = [{'label':'Population','value':'pop'},{'label':'GDP per capita','value':'gdpPercap'},{'label':'Life Expectancy','value':'lifeExp'}],style = {'width':'70%','margin-left':'30px'})
                            
                            ],style = {'positition':'fixed','float':'right','width':'240px','height':'1300px','background-color':'#444444','margin-right':'15px','border-style':'ridge'})]),
            html.Div([
                    
                dash_table.DataTable(id ='dashTable',columns = [
                   
                            {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                            if i == 'year'
                            else {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                            for i in table2.columns
                ],
                data = table2.to_dict('records'),
                filter_action = 'native',
                editable = False,
                page_size = 6,
                sort_action = 'native',
                sort_mode = 'multi',
                row_selectable = 'multi',
                column_selectable = 'multi',
                style_cell = {'minWidth':95,'maxWidth': 95,'width': 95})
                    
                    ],style = {'position':'absolute','top':'1330px','width':'1300px','height':'300px','background-color':'white','margin-left':'15px','border-style':'ridge'})
        
        ])
                
@app.callback(Output('box1','figure'),[Input('dropcont','value'),Input('droppara','value'),Input('boxovio','value')])
def boxOvio(continent,parameter,boxovio):
    
    graph_box = [go.Box(x = table.loc[table['continent'] == continent]['year'],y = table.loc[table['continent'] == continent][parameter])]
    graph_violin = [go.Violin(x = table.loc[table['continent'] == continent]['year'],y = table.loc[table['continent'] == continent][parameter])]
    layout = dict(title = parameter,xaxis = dict(title = 'years'))
    
    if 'violin' in boxovio:
        fig =  dict(data = graph_violin,layout = layout)
        
    else:
        fig = dict(data = graph_box,layout = layout)
        
    return fig

@app.callback(Output('bar1','figure'),[Input('dropcont','value')])
def bar1(continent):
    
    filtered = table.loc[table['continent'] == continent].groupby('year').sum()
    graph_data = [go.Bar(x = filtered.index,y = filtered['pop'])]
    layout = dict(title = 'Total Population',xaxis = dict(title = 'years'))
    
    fig =  dict(data = graph_data,layout = layout)
    return fig

@app.callback(Output('pie','figure'),[Input('yeardrop','value')])
def pie(year):
    
    filtered = table.loc[table['year'] == year].groupby('continent').sum()
    graph_data = [go.Pie(labels = filtered.index,values = filtered['pop'])]
    layout = dict(title = 'Total Population',xaxis = dict(title = 'continents'))
    
    fig =  dict(data = graph_data,layout = layout)
    return fig

@app.callback(Output('box2','figure'),[Input('yeardrop','value'),Input('droppara2','value'),Input('boxovio2','value')])
def boxOvio2(year,parameter,boxovio):
    
    graph_box = [go.Box(x = table.loc[table['year'] == year]['continent'],y = table.loc[table['year'] == year][parameter])]
    graph_violin = [go.Violin(x = table.loc[table['year'] == year]['continent'],y = table.loc[table['year'] == year][parameter])]
    layout = dict(title = parameter,xaxis = dict(title = 'continents'))
    
    if 'violin' in boxovio:
        fig =  dict(data = graph_violin,layout = layout)
        
    else:
        fig = dict(data = graph_box,layout = layout)
        
    return fig

@app.callback(Output('hist','figure'),[Input('contlast','value'),Input('yearlast','value'),Input('para3','value')])
def histo(continent,year,parameter):
    
    filtered = table.loc[(table['continent'] == continent) & (table['year'] == year)]
    
    graph_data = [go.Histogram(x = filtered[parameter])]
    layout = dict(title = parameter + ' distribution',xaxis = dict(title = parameter))
    
    fig =  dict(data = graph_data,layout = layout)
    return fig

@app.callback(Output('mapp','figure'),[Input('yeardrop','value'),Input('droppara2','value')])
def mapp(year,parameter):
    
    df = table[table['year'] == year]
    fig = go.Figure(data = [go.Choropleth(locations = df['iso_alpha'],z = df[parameter],colorscale = 'reds',hovertext = df['country'])])
    
    return fig
    
if __name__ == '__main__':
    app.run_server(debug = True)