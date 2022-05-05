import dash
from dash import dcc,html
from dash.dependencies import Input,Output,State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import requests
from dash import dash_table
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np




app = dash.Dash(__name__,suppress_callback_exceptions = True,external_stylesheets = [dbc.themes.BOOTSTRAP],
                meta_tags = [{'name' :'keywords','content':'precious,nliwasa,alpha,vantage,alpha vantage,precious nliwasa,stock data'},
                             {'name':'description','content' :'an app built with python dash to perform analytics on time series and economic data'},
                             {'name':'author','content':'precious nliwasa'},
                             {'name':'viewport','content':'width=device=width,initial-scale=1.0'}])


sidebarstyle = {
        
        'position':'fixed',
        'top':0,
        'left':0,
        'bottom':0,
        'width':'16rem',
        'padding':'2rem 1rem',
        'background-color':'peachpuff'
        
        }

sidebar = html.Div([
        
        html.Img(title = 'alpha vantage',src = '/assets/avlogo.png',alt = 'alpha vantage',width = '220px'),
        html.Hr(),
        dbc.Nav([
                
                dbc.NavLink('Home',href = '/',active = 'exact'),
                dbc.NavLink('Time Series',href = '/timeseries',active = 'exact'),
                dbc.NavLink('Fundamentals',href = '/fundamentals',active = 'exact'),
                dbc.NavLink('Cryptocurrencies',href = '/cryptocurrencies',active = 'exact'),
                dbc.NavLink('About',href = '/about',active = 'exact'),
                
                ],vertical = True,pills = True)
        
        ],style = sidebarstyle)

contentstyle = {
        
        'margin-left':'16rem',
        'margin-right':'0rem',
        'padding':'2rem 1rem'
        }

content = html.Div(id = 'content',style = contentstyle)

app.layout = dbc.Container([
        
        dcc.Location(id = 'url'),
        sidebar,
        content
        
        ],fluid = True)

@app.callback(Output('content','children'),[Input('url','pathname')])
def content(pathname):
    
    if (pathname == '/') | (pathname == '/symbols') | (pathname == '/calculator'):
        
        navigation = html.Ul([
                                    
                        html.Li([html.A(children = "What's Up",href = '/')]),
                        html.Li([html.A(children = 'Symbols',href = '/symbols')]),
                        html.Li([html.A(children = 'Calculator',href = '/calculator')])
                                    
                        ])
        if pathname == '/':
            output = html.Div([
                    html.Div([navigation]),
                    html.Br(),
                    html.Div([
                            
                            dbc.Row([
                                    
                                    dbc.Col([
                                    dbc.Card([
                                    
                                            dbc.CardImg(title = 'alpha vantage',src = '/assets/a.png'),
                                            dbc.CardBody([
                                                    
                                                    html.H3(children = 'Alpha Vantage',style = {'text-align':'center','color':'peachpuff'}),
                                                    html.P(children = 'Alpha Vantage is a Y Combinator backed company building the modern data platform for the next generation of financial market participants.Constantly ranked as a leading API provider for ease of use, accuracy, and price'),
                                                    dbc.CardLink(children = 'visit site',href = 'http://www.alphavantage.co',target = '_blank')
                                                    
                                                    ])
                                    
                                    ],color = 'dark',outline = False,inverse = True,style = {'height':'500px'})
                                    ],width = 4),
                                    dbc.Col([
                                    dbc.Card([
                                    
                                            dbc.CardImg(title = 'plotly dash',src = '/assets/dash.jpg'),
                                            dbc.CardBody([
                                                    
                                                    html.H3(children = 'Plotly Dash',style = {'text-align':'center','color':'peachpuff'}),
                                                    html.P(children = "Dash is an open source framework for building data visualization interfaces. Released in 2017 as a Python library, it's grown to include implementations for R and Julia. Dash helps data scientists build analytical web applications without requiring advanced web development knowledge"),
                                                    dbc.CardLink(children = 'visit site',href = 'http://www.plotly.com',target = '_blank')
                                                    
                                                    ])
                                    
                                    ],color = 'dark',outline = False,inverse = True,style = {'height':'500px'})
                                    ],width = 4),
                                    dbc.Col([
                                    dbc.Card([
                                    
                                            dbc.CardImg(title = 'disclaimer',src = '/assets/dd.png',style = {'height':'200px'}),
                                            dbc.CardBody([
                                                    
                                                    html.H3(children = 'Disclaimer',style = {'text-align':'center','color':'peachpuff'}),
                                                    html.P(children = "This app is not a property of alpha vantage. It has been authoured by Precious Nliwasa, a student of University of Malawi to track different economical and financial indicators with alpha vantage goal of democractising economical and financial data in mind")
                                                    
                                                    ])
                                    
                                    ],color = 'dark',outline = False,inverse = True,style = {'height':'500px'})
                                    ],width = 4)
                            ])
                            
                            ])
                ])
    
        if pathname == '/symbols':
            output = html.Div([
                    html.Div([navigation]),
                    html.Br(),
                    html.Br(),
                    html.Div([
                            html.Br(),
                            dbc.Row([
                                    
                                    dbc.Col([
                                            dcc.Input(id = 'search',type = 'search',value = 'tesco')
                                            ],width = {'size':3,'offset':3}),
                                    dbc.Col([
                                            dbc.Button(id = 'but',children = 'search',n_clicks = 0,style = {'height':'30px','width':'75px'})
                                            ],width = {'size':3})
                                            
                                    
                                    ]),
                            html.Br(),
                            dbc.Row([
                                    dbc.Col([
                                            dcc.Dropdown(id = 'searchResults',placeholder = 'search results',style = {'width':'330px'})
                                            ],width = {'size':5,'offset':3})
                                    ])
                                                   
                            ])
                ])
    
        if pathname == '/calculator':
            output = html.Div([
                    html.Div([navigation]),
                    html.Br(),
                    html.H3('Currency Exchange Rate',style = {'text-align':'center'}),
                    html.Div([
                            html.Br(),
                            dbc.Row([
                                    
                                    dbc.Col([dcc.Input(id = 'calcuFrom',placeholder = 'From Currency',value = 'btc')],width = {'size':3,'offset':2}),
                                    dbc.Col([html.H3('TO')],width = {'size':2}),
                                    dbc.Col([dcc.Input(id = 'calcuTo',placeholder = 'To Currency',value = 'cny')],width = {'size':3})
                                    
                                    ]),
                            html.Br(),
                            dbc.Row([
                                    dbc.Col([dbc.Button(id = 'but2',children = 'calculate',n_clicks = 0,style = {'height':'30px','width':'75px'})],width = {'size':4,'offset':5})
                                    ]),
                            html.Br(),
                            dbc.Row([
                                    html.Div(id = 'datatable')
                                    ])
                            
                            ])
                ])
        
    elif pathname == '/timeseries':
                
        output = html.Div([

                            html.Div([
                                    dbc.Row([dbc.Col([dcc.Dropdown(id = 'function',value = 'stocks',options = [{'label':'stocks','value':'stocks'},{'label':'crypto','value':'crypto'}])],width = {'size':3,'offset':5}),dbc.Col([dbc.Button(id = 'data2but',n_clicks = 0,children = 'submit',style = {'margin-left':'100px'})],width = {'size':3})]),
                                    html.Br(),
                                    dbc.Row([
                                            dbc.Col([
                                                    dbc.Row([
                                                            dbc.Col([dbc.Card([
                                                                    
                                                                    dbc.CardBody([
                                                                            dcc.Input(id = 'companyNa',value = 'IBM',style = {'margin-left':'19px','border-radius':'10px','border-color':'lightcoral'}),
                                                                            html.Br(),
                                                                            html.Br(),
                                                                            dcc.Dropdown(id = 'outputsize',value = 'compact',options = [{'label':'compact','value':'compact'},{'label':'full','value':'full'}],style = {'margin-left':'6px','width':'190px','color':'black','border-radius':'10px','border-color':'lightcoral'})
                                                                            ])
                                                                    
                                                                    ],color = 'dark',outline = False,inverse = True),
                                                                    dcc.Graph(id = 'indicator-volume',style = {'height':'300px'})],width = {'size':5}),
                                                            dbc.Col([
                                                                    dbc.Card([
                                                                            dbc.CardBody([
                                                                                    dcc.Dropdown(id = 'marketData',value = 'intraday',options = [{'label':'intraday','value':'intraday'},{'label':'daily','value':'daily'},{'label':'weekly','value':'weekly'},{'label':'monthly','value':'monthly'}]),
                                                                                    html.Br(),
                                                                                    dcc.Dropdown(id = 'feature',value = 'open',options = [{'label':'open','value':'open'},{'label':'high','value':'high'},{'label':'low','value':'low'},{'label':'close','value':'close'},{'label':'volume','value':'volume'}])
                                                                                    
                                                                                    ])
                                                                            ],color = 'dark'),
                                                                    html.Br(),
                                                                    html.Div(id = 'dataT2')],width = {'size':7})
                                                            ]),
                                                    dbc.Row([
                                                            dbc.Col([dcc.Graph(id = 'plot')],width = {'size':12})
                                                            ]),
                                                    dbc.Row([
                                                            dbc.Col([dcc.Graph(id = 'plot2')],width = {'size':12})
                                                            ])
                                                       ],width = {'size':7}),
                                            dbc.Col([
                                                    
                                                    dcc.Graph(id = 'trend'),
                                                    dcc.Graph(id = 'cyclic'),
                                                    dcc.Graph(id = 'residual')
                                                    
                                                    ],width = {'size':5})
                                            ]),
                                    dbc.Row([
                                            html.Div(id = 'dataT3')
                                            ])
                                    
                                    ])
                        ])
                
        
    elif pathname == '/fundamentals':
        output = html.Div([
                'f'
                
                ])
    
    elif pathname == '/cryptocurrencies':
        output = html.Div([
                'c'
                
                ])
        
    elif pathname == '/about':
        output = html.Div([
                'a'
                
                ])
    
    else:
        output = html.H3('404:Not Found /n pathname was not found',className = 'text-danger')
    
    return output

@app.callback(Output('datatable','children'),[Input('but2','n_clicks')],[State('calcuFrom','value'),State('calcuTo','value')])
def dataTable(n_clicks,from_c,to_c):
    
    try:
        url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey=key'.format(from_c,to_c)
        r = requests.get(url)
        data = r.json()
    
        table = pd.DataFrame(list(data['Realtime Currency Exchange Rate'].items()))
        table.columns = ['Feature','Details']
    
        return dash_table.DataTable(columns = [
                   
                                {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                            for i in table.columns
                            ],
                    data = table.to_dict('records'),
                    filter_action = 'native',
                    editable = False,
                    page_size = 9,
                    sort_action = 'native',
                    sort_mode = 'multi',
                    row_selectable = 'multi',
                    column_selectable = 'multi')
        
    except Exception:
        return html.H3('Enter correct data',style = {'text-align':'center','color':'blue'})
    
def intratable(company,outputsize):
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&outputsize={}&interval=5min&apikey=key'.format(company,outputsize)
    r = requests.get(url)
    data = r.json()
    
    return data

@app.callback([Output('dataT3','children'),Output('dataT2','children')],[Input('data2but','n_clicks')],[State('companyNa','value'),State('outputsize','value')])
def dataTable2(n_clicks,company,outputsize):
    
    try:
       data = intratable(company,outputsize)
       table = pd.DataFrame(data['Time Series (5min)'])
       table = table.T
       table.columns = ['open','high','low','close','volume']
       
       table2 = pd.DataFrame(data['Meta Data'].items())
       table2.columns = ['Feature','Details']
       
       table11 =  dash_table.DataTable(columns = [
                   
               {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
               for i in table.columns
               ],
                    data = table.to_dict('records'),
                    filter_action = 'native',
                    editable = False,
                    page_size = 9,
                    sort_action = 'native',
                    sort_mode = 'multi',
                    row_selectable = 'multi',
                    column_selectable = 'multi',
                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95})
       
       
       table22 = dash_table.DataTable(columns = [
                   
                                {'name':i,'id':i,'deletable':False,'hideable':False,'selectable':True}
                            for i in table2.columns
                            ],
                    data = table2.to_dict('records'),
                    filter_action = 'native',
                    editable = False,
                    page_size = 9,
                    sort_action = 'native',
                    sort_mode = 'multi',
                    row_selectable = 'multi',
                    column_selectable = 'multi',
                    style_cell = {'minWidth':95,'maxWidth': 95,'width': 95})
       
       return table11,table22
        
    except Exception:
        return 'data not available','data not available'
    
    
@app.callback(Output('indicator-volume','figure'),[Input('data2but','n_clicks')],[State('companyNa','value'),State('outputsize','value')])
def Indicators(n_clicks,company,outputsize):
    
    try:
        
        data = intratable(company,outputsize)
        table = pd.DataFrame(data['Time Series (5min)'])
        table = table.T
        table.columns = ['open','high','low','close','volume']
        
        
        volume_ = float(table.iloc[0,4])
        
        volume_ = [go.Indicator(mode = 'gauge',value = volume_,title = 'Volume',name = 'volume')]
        fig = dict(data = volume_)
        
        return fig
        
    except Exception:
        dat = [go.Indicator(mode = 'gauge',value = 0,title = 'provide argument',name = 'volume')]
        fig = dict(data = dat)
        
        return fig
    
    
def Table(company,outputsize):
    
        data = intratable(company,outputsize)
        table = pd.DataFrame(data['Time Series (5min)'])
        table = table.T
        table.columns = ['open','high','low','close','volume']
        
        table.open = table.open.apply(float)
        table.close = table.close.apply(float)
        table.high = table.high.apply(float)
        table.low = table.low.apply(float)
        table.volume = table.volume.apply(float)
        
        return table
    
    
@app.callback(Output('plot','figure'),[Input('data2but','n_clicks')],[State('companyNa','value'),State('outputsize','value')])
def graph_m(n_clicks,company,outputsize):
    
    try:
        
        table = Table(company,outputsize)
        
        open_ = go.Scatter(x = table.index,y = table.open.values,name = 'open')
        close_ = go.Scatter(x = table.index,y = table.close.values,name = 'close')
        high_ = go.Scatter(x = table.index,y = table.high.values,name = 'high')
        low_ = go.Scatter(x = table.index,y = table.low.values,name = 'low')
        
        dat = [open_,close_,high_,low_]
        fig = dict(data = dat)
        
        return fig
        
    except Exception:
        dat = [go.Indicator(mode = 'gauge',value = 0,title = 'Current Volume',name = 'volume')]
        fig = dict(data = dat)
        
        return fig
    
@app.callback([Output('trend','figure'),Output('cyclic','figure'),Output('residual','figure')],[Input('data2but','n_clicks')],[State('companyNa','value'),State('outputsize','value'),State('feature','value')])
def decompose(n_clicks,company,outputsize,feature):
    
    try:
        
        table = Table(company,outputsize)
        table.index = pd.to_datetime(table.index)
        desired = table[[feature]]
        desiredlog = np.log(desired)
        
        decomposition = seasonal_decompose(desiredlog,freq = 15)
        
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid
        
        tren = [go.Scatter(x = trend.index,y = trend[feature],name = 'trend',line = dict(color = 'green'))]
        seaso = [go.Scatter(x = seasonal.index,y = seasonal[feature],name = 'seasonal',line = dict(color = 'blue'))]
        residu = [go.Scatter(x = residual.index,y = residual[feature],name = 'residual',line = dict(color = 'red'))]
        
        tfig = dict(data = tren)
        sfig = dict(data = seaso)
        rfig = dict(data = residu)
        
        return tfig,sfig,rfig
        
    except Exception:
        dat = [go.Indicator(mode = 'gauge',value = 0,title = 'Current Volume',name = 'volume')]
        fig = dict(data = dat)
        
        return fig,fig,fig
        
@app.callback(Output('plot2','figure'),[Input('data2but','n_clicks')],[State('companyNa','value'),State('outputsize','value')])
def graph_si(n_clicks,company,outputsize):
    
    try:
        
        table = Table(company,outputsize)
             
        volume_ = go.Scatter(x = table.index,y = table.volume.values,name = 'volume')

        
        dat = [volume_]
        fig = dict(data = dat)
        
        return fig
        
    except Exception:
        dat = [go.Indicator(mode = 'gauge',value = 0,title = 'Current Volume',name = 'volume')]
        fig = dict(data = dat)
        
        return fig

@app.callback(Output('searchResults','options'),[Input('but','n_clicks')],[State('search','value')])
def searchResults(n_clicks,value):
    
    url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey=key'.format(value)
    r = requests.get(url)
    data = r.json()
    
    try:
        df = pd.DataFrame(data['bestMatches'])
        dff = df[['1. symbol','2. name','4. region']]
    
        options_a = {'optionss':dff.values}
    
        return [{'label':str(i),'value':str(i)} for i in list(options_a['optionss'])]
    
    except Exception:
        return [{'label':'No Results Found','value':'nrf'}] 

if __name__ == '__main__':
    app.run_server(debug = True)
