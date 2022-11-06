import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
from scipy.stats import ttest_ind
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import dash_table

hrdata = pd.read_csv('hrData.csv')

option_features = {'salary':list(hrdata.salary.value_counts().index),
                   'sales':list(hrdata.sales.value_counts().index),
                   'time_spend_company':list(hrdata.time_spend_company.value_counts().index),
                   'left':list(hrdata.left.value_counts().index),
                   'Work_accident':list(hrdata.Work_accident.value_counts().index),
                   'number_project':list(hrdata.number_project.value_counts().index),
                   'promotion_last_5years':list(hrdata.promotion_last_5years.value_counts().index)}

sales_dict = dict(sales = 1,technical = 2,support = 3,IT = 4,product_mng = 5,marketing = 6,RandD = 7,accounting = 8,hr = 9,management = 10)

hr = hrdata

hrtable = pd.DataFrame(data = hrdata.values,columns = ['satisfaction','last evaluation','projects','monthly hours','time spent','accident','left','promotion','sales','salary'])

hr.sales = hr.sales.map(sales_dict)
    
X = hr.drop(['salary'],axis = 'columns')
y = hr.salary
    
X_train,X_test,y_train,y_test = train_test_split(X,y)
    
scaler = StandardScaler()
    
X_train = scaler.fit_transform(X_train)
X_test =  scaler.fit_transform(X_test)

app = dash.Dash(__name__,suppress_callback_exceptions=True)

app.layout = html.Div([
        
        html.Div([
                    html.H2(children = 'Human Resource Analytics',style = {'text-align':'center','background':'linear-gradient(to right,pink,aqua)','height':'50px','border-radius':'10px','border-style':'ridge','padding-top':'15px','color':'white','font-size':'25px'})],className = 'partTop'),
        html.Div([
                
                html.Div([
                        html.H3('Page',style = {'text-align':'center'}),
                        html.Br(),
                        dcc.Dropdown(id = 'page',value = 'home',options = [{'label':'Home','value':'home'},{'label':'Difference of means','value':'dom'},{'label':'Predicting salary','value':'predicting'},{'label':'datatable','value':'datatable'}],style = {'width':'90%','left':'23px'}),
                        html.Br(),
                        html.Button(id = 'but',n_clicks = 0,children = 'submit',style = {'color':'white','width':'60px','height':'29px','background-color':'pink','border-radius':'10px','position':'fixed','left':'105px','border-color':'white'}),
                        html.Br(),
                        html.Br(),
                        html.Hr(),
                        html.Div(id = 'settings')],className = 'partLeft'),
                html.Div(id = 'page_type',className = 'partRight')],className = 'partBottom')
        
        ])

@app.callback(Output('page_type','children'),[Input('but','n_clicks')],[State('page','value')])
def page_select(n_clicks,page):
    
    if 'home' in page:
        
        output = html.Div([
                
                            dcc.Graph(id = 'bar-fig',style = {'width':'50%','height':'50%','margin-top':'15px','margin-left':'15px','position':'absolute','float':'left'}),
                            dcc.Graph(id = 'box-fig',style = {'width':'50%','height':'50%','margin-top':'15px','margin-right':'15px','float':'right'}),
                            dcc.Graph(id = 'hist-fig',style = {'width':'95%','height':'45%','margin-bottom':'0px','margin-left':'15px','position':'absolute','top':'290px'})],className = 'home')
        
    elif 'dom' in page:
        
        output = html.Div([
                
                            html.Div([
                                    
                                    dcc.Graph(id = 'dom-fig',style = {'position':'absolute','height':'60%'}),
                                    dcc.Graph(id = 'dom-fig2',style = {'position':'absolute','height':'60%','top':'290px'})],style = {'position':'absolute','float':'left','margin-top':'15px','margin-left':'15px','height':'80%'}),
                            html.Div([
                                    
                                    html.H2(children = 'Satisfaction (current)',style = {'text-align':'center','color':'white'}),
                                    html.H4(id = 'meanSC',style = {'text-align':'center'}),
                                    html.H4(id = 'stdSC',style = {'text-align':'center'}),
                                    html.H2(children = 'Satisfaction (last)',style = {'text-align':'center','color':'white'}),
                                    html.H4(id = 'meanSL',style = {'text-align':'center'}),
                                    html.H4(id = 'stdSL',style = {'text-align':'center'}),
                                    html.H2(children = 'Test statistic',style = {'text-align':'center','color':'white'}),
                                    html.H4(id = 'tstat',style = {'text-align':'center'}),
                                    html.H2(children = 'P-value',style = {'text-align':'center','color':'white'}),
                                    html.H4(id = 'pvalue',style = {'text-align':'center'})],className = 'smallright')],className = 'dom')
        
    elif 'predicting' in page:
        
        output = html.Div([
                
                            html.Div([
                                    
                                    html.Br(),
                                    html.Br(),
                                    html.Div([
                                            
                                            dcc.Input(id = 'satisfaction_level',type = 'text',placeholder = 'enter satisfaction level',value = '0',style = {'position':'absolute','float':'left','left':'100px','width':'200px','height':'30px'}),
                                            dcc.Input(id = 'last_evaluation',type = 'text',placeholder = 'enter last evaluation',value = '0',style = {'float':'right','height':'30px','width':'200px','margin-right':'100px'})]),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Div([
                                        
                                            dcc.Input(id = 'number_project',type = 'text',placeholder = 'enter number of projects',value = '0',style = {'position':'absolute','float':'left','left':'100px','width':'200px','height':'30px'}),
                                            dcc.Input(id = 'average_montly_hours',type = 'text',placeholder = 'enter average_monthly hours',value = '0',style = {'float':'right','height':'30px','width':'200px','margin-right':'100px'})
                                            
                                            ]),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Div([
                                            
                                            dcc.Input(id = 'time_spend_company',type = 'text',placeholder = 'enter time spent',value = '0',style = {'position':'absolute','float':'left','left':'100px','width':'200px','height':'30px'}),
                                            dcc.Input(id = 'Work_accident',type = 'text',placeholder = 'enter work accident',value = '0',style = {'float':'right','height':'30px','width':'200px','margin-right':'100px'})
                                            
                                            ]),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Div([
                                            
                                            dcc.Input(id = 'left',type = 'text',placeholder = 'enter if left',value = '0',style = {'position':'absolute','float':'left','left':'100px','width':'200px','height':'30px'}),
                                            dcc.Input(id = 'promotion_last_5years',type = 'text',placeholder = 'enter if promoted',value = '0',style = {'float':'right','height':'30px','width':'200px','margin-right':'100px'})
                                            
                                            ]),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Div([
                                            
                                            dcc.Dropdown(id = 'mldrop',value = 'sales',options = [{'label':i,'value':i} for i in option_features['sales']],style = {'width':'60%','margin-left':'100px'})
                                            
                                            ]),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Div([
                                            
                                            html.Button(id = 'but4',n_clicks = 0,children = 'submit',style = {'color':'white','width':'60px','height':'29px','background-color':'aqua','border-radius':'10px','border-color':'white','margin-left':'300px'})
                                            
                                            ])],style = {'position':'fixed','float':'left','left':'320px','height':'80%','width':'50%','background-color':'white','border-style':'ridge','border-color':'pink'}),
                            html.Div([
                                    
                                    html.Div([
                                            
                                            html.H3(children = 'Model Score',style = {'text-align':'center'}),
                                            html.Br(),
                                            html.H3(id = 'modelscore',style = {'text-align':'center'})],style = {'height':'48%','width':'100%','background-color':'white','background':'linear-gradient(to right,pink,aqua)','border-style':'ridge','border-color':'pink'}),
                                    html.Br(),
                                    html.Div([
                                            
                                            html.H3(children = 'Salary Type',style = {'text-align':'center'}),
                                            html.Br(),
                                            html.H3(id = 'salaryType',style = {'text-align':'center'})
                                            ],style = {'height':'48%','width':'100%','background-color':'white','background':'linear-gradient(to right,pink,white)','border-style':'ridge','border-color':'pink'})],style = {'position':'fixed','float':'right','right':'15px','height':'80%','width':'22%'})],className = 'predicting')
    
    else:
        
        output = html.Div([dash_table.DataTable(columns = [
                   
                            {'name':i,'id':i,'deletable':False,'hideable':True,'selectable':True}
                            if i == 'species'
                            else {'name':i,'id':i,'deletable':False,'selectable':True}
                            for i in hrtable.columns
                ],
                data = hrtable.to_dict('records'),
                filter_action = 'native',
                editable = False,
                page_size = 15,
                sort_action = 'native',
                sort_mode = 'multi',
                row_selectable = 'multi',
                column_selectable = 'multi')],className = 'dtable')
        
    return output

@app.callback(Output('settings','children'),[Input('but','n_clicks')],[State('page','value')])
def settings_type(n_clicks,page):
    
    if 'home' in page:
        sett = html.Div([
                
                html.H3(children = 'Bar chart',style = {'text-align':'center'}),
                html.Br(),
                dcc.Dropdown(id = 'barX',value = 'salary',options = [{'label':'salary','value':'salary'},{'label':'sales','value':'sales'},{'label':'promotion','value':'promotion_last_5years'},{'label':'left','value':'left'},{'label':'work accident','value':'Work_accident'},{'label':'time spent','value':'time_spend_company'},{'label':'projects','value':'number_project'}],style = {'position':'absolute','left':'5px','float':'left','width':'65%'}),
                dcc.Dropdown(id = 'barY',value = 'satisfaction_level',options = [{'label':'satisfaction level','value':'satisfaction_level'},{'label':'last evaluation','value':'last_evaluation'},{'label':'monthly hours','value':'average_montly_hours'}],style = {'float':'right','width':'65%','margin-right':'5px'}),
                html.Br(),
                html.Br(),
                html.H3(children = 'Boxplot',style = {'text-align':'center'}),
                dcc.Dropdown(id = 'boxX',value = 'salary',options = [{'label':'salary','value':'salary'},{'label':'sales','value':'sales'},{'label':'promotion','value':'promotion_last_5years'},{'label':'left','value':'left'},{'label':'work accident','value':'Work_accident'},{'label':'time spent','value':'time_spend_company'},{'label':'projects','value':'number_project'}],style = {'position':'absolute','left':'5px','float':'left','width':'65%'}),
                dcc.Dropdown(id = 'boxY',value = 'satisfaction_level',options = [{'label':'satisfaction level','value':'satisfaction_level'},{'label':'last evaluation','value':'last_evaluation'},{'label':'monthly hours','value':'average_montly_hours'}],style = {'float':'right','width':'65%','margin-right':'5px'}),
                html.Br(),
                html.Br(),
                html.H3(children = 'Histogram',style = {'text-align':'center'}),
                dcc.RadioItems(id = 'radiobox',value = 'satisfaction_level',options = [{'label':'satisfaction level','value':'satisfaction_level'},{'label':'last evaluation','value':'last_evaluation'}])
                ])
    elif 'dom' in page:
        sett = html.Div([
                
                html.H3(children = 'Category',style = {'text-align':'center'}),
                dcc.Dropdown(id = 'category',value = 'salary',options = [{'label':'salary','value':'salary'},{'label':'sales','value':'sales'},{'label':'promotion','value':'promotion_last_5years'},{'label':'left','value':'left'},{'label':'work accident','value':'Work_accident'},{'label':'time spent','value':'time_spend_company'},{'label':'projects','value':'number_project'}],style = {'width':'80%','margin-left':'20px'}),
                html.Br(),
                dcc.Dropdown(id = 'feature',value = 'low',style = {'width':'80%','margin-left':'20px'}),
                html.H3(children = 'Plot type',style = {'text-align':'center'}),
                dcc.RadioItems(id = 'radiobox2',value = 'violin',options = [{'label':'Violin','value':'violin'},{'label':'Histogram','value':'histogram'}],style = {'text-align':'center'}),
                html.Br(),
                html.Button(id = 'but2',n_clicks = 0,children = 'submit',style = {'color':'white','width':'60px','height':'29px','background-color':'pink','border-radius':'10px','position':'fixed','left':'105px','border-color':'white'})])
    elif 'predicting' in page:
        sett = html.Div([
                
                html.H3(children = 'Knn Classifier',style = {'text-align':'center'}),
                html.Br(),
                html.H4(children = 'Number of neighbours',style = {'text-align':'center'}),
                dcc.Input(id = 'neighbors',value = '5',type = 'text',style = {'margin-left':'29px','width':'200px','height':'30px'}),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Button(id = 'but3',n_clicks = 0,children = 'submit',style = {'color':'white','width':'60px','height':'29px','background-color':'pink','border-radius':'10px','border-color':'white','margin-left':'95px'})])
    
    else:
        
        sett = html.Div([])
        
    return sett

@app.callback(Output('bar-fig','figure'),[Input('barX','value'),Input('barY','value')])
def barplot(x,y):
    
    data = hrdata.groupby([x])[y].mean()
    
    graph_data = [go.Bar(x = data.index,y = data.values,name = x)]
    layout = dict(title = 'Barplot',xaxis = dict(title = x),yaxis = dict(title = y))
    
    figure = dict(data = graph_data,layout = layout)
    
    return figure
    
@app.callback(Output('box-fig','figure'),[Input('boxX','value'),Input('boxY','value')])
def boxplot(x,y):
    
    graph_data = [go.Box(x = hrdata[x],y = hrdata[y],name = x)]
    layout = dict(title = 'Boxplot',xaxis = dict(title = x),yaxis = dict(title = y))
    
    figure = dict(data = graph_data,layout = layout)
    
    return figure 

@app.callback(Output('hist-fig','figure'),[Input('radiobox','value')])
def histogram(x):
    
    graph_data = [go.Histogram(x = hrdata[x],name = x)]
    layout = dict(title = 'Histogram',xaxis = dict(title = x),yaxis = dict(title = 'count'))
    
    figure = dict(data = graph_data,layout = layout)
    
    return figure 

@app.callback(Output('feature','options'),[Input('category','value')])
def optionss(category):
    return [{'label':i,'value':i} for i in option_features[category]]

@app.callback(Output('dom-fig','figure'),[Input('but2','n_clicks')],[State('category','value'),State('feature','value'),State('radiobox2','value')])
def satisfaction_fig(n_clicks,category,feature,typeplot):

    filtered = hrdata.loc[hrdata[category] == feature]
    
    if 'violin' in typeplot:
        
        graph_data = [go.Violin(x = filtered.satisfaction_level,name = '')]
        layout = dict(title = 'satisfaction distribution(current)',xaxis = dict(title = 'satisfaction level'))
        
        figure = dict(data = graph_data,layout = layout)
        
    else: 
        graph_data = [go.Histogram(x = filtered.satisfaction_level)]
        layout = dict(title = 'satisfaction distribution(current)',xaxis = dict(title = 'satisfaction level'),yaxis = dict(title = 'count'))
        
        figure = dict(data = graph_data,layout = layout)
        
    return figure

@app.callback(Output('dom-fig2','figure'),[Input('but2','n_clicks')],[State('category','value'),State('feature','value'),State('radiobox2','value')])
def last_eval_fig(n_clicks,category,feature,typeplot):

    filtered = hrdata.loc[hrdata[category] == feature]
    
    if 'violin' in typeplot:
        
        graph_data = [go.Violin(x = filtered.last_evaluation,name = '')]
        layout = dict(title = 'satisfaction distribution(last)',xaxis = dict(title = 'satisfaction level'))
        
        figure = dict(data = graph_data,layout = layout)
        
    else: 
        graph_data = [go.Histogram(x = filtered.last_evaluation)]
        layout = dict(title = 'satisfaction distribution(last)',xaxis = dict(title = 'satisfaction level'),yaxis = dict(title = 'count'))
        
        figure = dict(data = graph_data,layout = layout)
        
    return figure

@app.callback(Output('meanSC','children'),[Input('but2','n_clicks')],[State('category','value'),State('feature','value')])
def meansc(n_clicks,category,feature):
    
    filtered = hrdata.loc[hrdata[category] == feature]
    
    return 'Mean : ' + str(np.mean(filtered.satisfaction_level))

@app.callback(Output('stdSC','children'),[Input('but2','n_clicks')],[State('category','value'),State('feature','value')])
def stdsc(n_clicks,category,feature):
    
    filtered = hrdata.loc[hrdata[category] == feature]
    
    return 'Std : ' + str(np.std(filtered.satisfaction_level))

@app.callback(Output('meanSL','children'),[Input('but2','n_clicks')],[State('category','value'),State('feature','value')])
def meansl(n_clicks,category,feature):
    
    filtered = hrdata.loc[hrdata[category] == feature]
    
    return 'Mean : ' + str(np.mean(filtered.last_evaluation))

@app.callback(Output('stdSL','children'),[Input('but2','n_clicks')],[State('category','value'),State('feature','value')])
def stdsl(n_clicks,category,feature):
    
    filtered = hrdata.loc[hrdata[category] == feature]
    
    return 'Std : ' + str(np.std(filtered.last_evaluation))

@app.callback([Output('tstat','children'),Output('pvalue','children')],[Input('but2','n_clicks')],[State('category','value'),State('feature','value')])
def tstat(n_clicks,category,feature):
    
    filtered = hrdata.loc[hrdata[category] == feature]
    
    tstat,pvalue = ttest_ind(filtered.satisfaction_level,filtered.last_evaluation)
    
    return 't statistic : ' + str(tstat),'p-value : ' + str(pvalue)

#@app.callback(Output('pvalue','children'),[Input('but2','n_clicks')],[State('category','value'),State('feature','value')])
#def pvalue(n_clicks,category,feature):
    
#    filtered = hrdata.loc[hrdata[category] == feature]
    
#    _,pvalue = ttest_ind(filtered.satisfaction_level,filtered.last_evaluation)
    
#    return 'p-value : ' + str(pvalue)

@app.callback([Output('modelscore','children'),Output('salaryType','children')],[Input('but3','n_clicks'),Input('but4','n_clicks')],[State('neighbors','value'),State('satisfaction_level','value'),State('last_evaluation','value'),State('number_project','value'),State('average_montly_hours','value'),State('time_spend_company','value'),State('Work_accident','value'),State('left','value'),State('promotion_last_5years','value'),State('mldrop','value')])
def modelScorepred(n_clicks,n_clicks2,neighbors,sl,le,np,avg,time,acci,left,promo,drop):
    
    model = KNeighborsClassifier(n_neighbors = int(neighbors),metric = 'euclidean')
    
    model.fit(X_train,y_train)
    
    score = model.score(X_test,y_test)
    prediction = model.predict([[float(sl),float(le),float(np),float(avg),float(time),float(acci),float(left),float(promo),sales_dict[drop]]])

    return str(score),str(prediction)
    
#@app.callback(Output('salaryType','children'),[Input('but4','n_clicks')],[State('neighbors','value'),State('satisfaction_level','value'),State('last_evaluation','value'),State('number_project','value'),State('average_montly_hours','value'),State('time_spend_company','value'),State('Work_accident','value'),State('left','value'),State('promotion_last_5years','value'),State('mldrop','value')])
#def salaryTY(n_clicks,neighbor,sl,le,np,avg,ti me,acci,left,promo,drop):
    
#    model = KNeighborsClassifier(n_neighbors = int(neighbor),metric = 'euclidean')
    
#    model.fit(X_train,y_train)
    
#    return model.predict([[float(sl),float(le),float(np),float(avg),float(time),float(acci),float(left),float(promo),sales_dict[drop]]])
    
if __name__ == '__main__':
    app.run_server(debug = True)
