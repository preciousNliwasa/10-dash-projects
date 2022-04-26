import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.graph_objs as go
import dash_table
from statsmodels import datasets

dt = datasets.grunfeld
df = dt.load(as_pandas = True)
table = df.data

option_all = {'firm':list(table.firm.value_counts().index),'year':list(table.year.value_counts().index)}

app = dash.Dash(__name__,suppress_callback_exceptions = True)

app.layout = html.Div([
        
            html.H2(children = 'Top USA Firms 1935-1953',style = {'text-align':'center','background-color':'black','height':'50px','color':'white','border-style':'ridge','padding-top':'10px'}),
            html.Div([
                    
                    html.Div([html.H4(id = 'infoboxH'),html.Hr(),html.H3(id = 'infobox')],style = {'background':'linear-gradient(to right,aqua,peachpuff)','width':'400px','height':'100px','margin-left':'15px','margin-top':'0px','text-align':'center','border-style':'ridge','position':'absolute','float':'left'}),
                    html.Div([html.H4(id = 'infoboxH3'),html.Hr(),html.H3(id = 'infobox3')],style = {'background':'linear-gradient(to right,lightcoral,teal)','width':'400px','height':'100px','margin-right':'15px','margin-top':'0px','text-align':'center','border-style':'ridge','float':'right'}),
                    html.Div([html.H4(id = 'infoboxH2'),html.Hr(),html.H3(id = 'infobox2')],style = {'background':'linear-gradient(to right,teal,aqua)','width':'400px','height':'100px','margin-left':'460px','margin-top':'0px','text-align':'center','border-style':'ridge'})
                    
                    ]),
            html.Br(),
            html.Div([
                    
                    html.Div([
                            
                            dcc.Graph(id = 'bar-feature',style = {'width':'880px','height':'340px','margin-left':'15px','border-style':'ridge','border-color':'peachpuff'}),
                            html.Br(),
                            dcc.Graph(id = 'bar-year',style = {'width':'880px','height':'340px','margin-left':'15px','border-style':'ridge','border-color':'peachpuff'})
                            
                            ],style = {'position':'absolute','float':'left'}),
                    html.Div([
                            
                            html.Div([dash_table.DataTable(id ='dashTable',columns = [
                   
                            {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':False}
                            if i == 'year' or i == 'firm'
                            else {'name':i,'id':i,'deletable':False,'selectable':True}
                            for i in table.columns
                ],
                data = table.to_dict('records'),
                filter_action = 'native',
                editable = False,
                page_size = 10,
                sort_action = 'native',
                sort_mode = 'multi',
                row_selectable = 'single',
                column_selectable = 'single',
                style_cell = {'minWidth':73,'maxWidth': 73,'width': 73})],style = {'background-color':'white','height':'420px','border-style':'ridge','border-color':'peachpuff'}),
                html.Br(),
                html.Div(children = [
                        html.Br(),
                        html.H3('YEAR (for top barplot)',style = {'text-align':'center'}),
                        dcc.Dropdown(id = 'dropd',value = 1935,options = [{'label':i,'value':i} for i in option_all['year']],style = {'width':'60%','margin-left':'70px'}),
                        html.H3('FIRM (for bottom barplot)',style = {'text-align':'center'}),
                        dcc.Dropdown(id = 'dropd2',value = 'IBM',options = [{'label':i,'value':i} for i in option_all['firm']],style = {'width':'60%','margin-left':'70px'})
                        
                        ],style = {'background-color':'peachpuff','height':'230px','border-style':'ridge'})
                            
                ],style = {'float':'right','margin-right':'15px'})
                    
                    ])
        
        ])

@app.callback(Output('bar-feature','figure'),[Input('dashTable','selected_columns'),Input('dropd','value')])
def bar_feature(selected_column,year):
    
    filtered = table.loc[table['year'] == int(year)]
    
    graph_data = [go.Bar(x = filtered.firm,y = filtered[selected_column[0]])]
    layout = dict(title = str(selected_column[0]) + ' against US firms ' + str(year),plot_bgcolor = 'peachpuff')
    
    fig = dict(data = graph_data,layout = layout)
    
    return fig

@app.callback(Output('bar-year','figure'),[Input('dashTable','selected_columns'),Input('dropd2','value')])
def bar_year(selected_column,firm):
    
    filtered = table.loc[table['firm'] == firm]
    
    graph_data = [go.Bar(x = filtered.year,y = filtered[selected_column[0]])]
    layout = dict(title = str(selected_column[0]) + ' (' + firm + ')' + ' 1935-1953',plot_bgcolor = 'peachpuff')
    
    fig = dict(data = graph_data,layout = layout)
    
    return fig

@app.callback(Output('infobox','children'),[Input('dashTable','selected_rows')])
def infobox(selected_row):
    
    filtered = dict(table.iloc[selected_row,])
    return filtered['invest']

@app.callback(Output('infoboxH','children'),[Input('dashTable','selected_rows')])
def infoboxH(selected_row):
    
    filtered = dict(table.iloc[selected_row,])
    return filtered['firm']

@app.callback(Output('infobox3','children'),[Input('dashTable','selected_rows')])
def infobox3(selected_row):
    
    filtered = dict(table.iloc[selected_row,])
    return filtered['capital']

@app.callback(Output('infoboxH3','children'),[Input('dashTable','selected_rows')])
def infoboxH3(selected_row):
    
    filtered = dict(table.iloc[selected_row,])
    return filtered['firm']

@app.callback(Output('infobox2','children'),[Input('dashTable','selected_rows')])
def infobox2(selected_row):
    
    filtered = dict(table.iloc[selected_row,])
    return filtered['value']

@app.callback(Output('infoboxH2','children'),[Input('dashTable','selected_rows')])
def infoboxH2(selected_row):
    
    filtered = dict(table.iloc[selected_row,])
    return filtered['firm']

if __name__ == '__main__':
    app.run_server(debug = True)