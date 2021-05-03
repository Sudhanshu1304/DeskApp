import datetime as dt
from numpy.lib.shape_base import split
import pandas as pd
import calendar
import time
import numpy as np


def DAYS_DATA(data,init,noofdays , separate = False,gen_date =False):
    # separate => to get the data of each day seprately
    
    if gen_date == True: # if data is for the home page rt date dection
     
        with open("STATE/gen_date.txt","r") as read:
            gen_d = read.read()
            read.close()
  
        
        if (abs(pd.to_datetime(gen_d) - pd.to_datetime(init)).days >= 7):
            with open("STATE/gen_date.txt","w") as w:
                w.write(init)
                w.close()
                
        else:
           
            gen_d = pd.to_datetime(gen_d).strftime("%m/%d/%Y")
            init = gen_d
           
            
    dates = list(data['date'])

   
    
    nan = [] # this represents dates which are not in dataset

    DATA = data[data['date']==init]
 
    d = {init : DATA}
    
    for i in range(1,noofdays):
       
        try:
            if gen_date != True:
                req = (pd.to_datetime(dates[0]) - pd.DateOffset(days = i)).strftime("%m/%d/%Y")
            else:
              
                req = (pd.to_datetime(gen_d) + pd.DateOffset(days = i)).strftime("%m/%d/%Y")
               
           
            if req in  dates :
             
                if separate == True :
                  
                    d[req] = data[data['date']==req]
                else:
                    
                    DATA = pd.concat([DATA,data[data['date']==req]],axis=0)
                    
            else:
               
                nan.append(req)

        except:
          
            pass
    
   
    if separate==True:
        
        return d,nan
    else:
        return (DATA,nan)




def get_range_data(data,days=None,date1=None,date2=None,week1=None ,week2=None,Month1=None,Month2=None,gen_data=False):
    
  
    '''
        Date Format should be fixed -- { %m/%d/%Y }
    '''
    data = data.reset_index(drop=True)
    init = data['date'][0] # First date in dataset
    
    if type(days)!= type(None) :
        if gen_data == True:
            return DAYS_DATA(data,init,days,separate=True,gen_date=True)
        else:
            return DAYS_DATA(data,init,days,separate=True)
    
    if (type(date1)!= type(None) and type(date2)==type(None) ):
        '''
            DATA of  A perticular date
        '''
      
        return (data[data['date']==date1],True)
    
    elif(type(date1)!=type(None)  and type(date2)!=type(None) ):
        
        '''
            DATA of between two perticular dates
        '''
        
        
        indx1 = data[data['date']==date1]
        indx2 = data[data['date']==date2]
        
        if len(indx1) != 0:
            indx1 = indx1.index[0]
        else:
            return ([],False)
        if len(indx2) !=0:    
            indx2 = indx2.index[-1]
        else:
            return ([],False)
        
        return (data.iloc[indx1 : indx2+1 ,:],True)
    
    elif( type(week1)!=type(None)  and type(week2)==type(None) ):
        
        # week is a int ex: 1 , 2 => 7 days of data or 14 days data
       
        noofdays = week1*7
        if gen_data==True:
             return DAYS_DATA(data,init,noofdays,gen_date=True)
        else:
            
            return DAYS_DATA(data,init,noofdays)
    
    elif(type(week1)!=type(None)  and type(week2)!=type(None) ):
     
        pass
    
    elif( type(Month1)!=type(None) ):
        
        # week is a int ex: 1 , 2 => 7 days of data or 14 days data
        
        split = init.split("/")
        
        mon = int(split[0])
        year = int(split[-1])
         
        lastday = calendar.monthrange(year,mon)[1] 
        if gen_data ==True:
            return DAYS_DATA(data,init,lastday,gen_date=True)
        else:
            return DAYS_DATA(data,init,lastday)
    
    
    elif(type(Month1)!=type(None)  and type(Month2)!=type(None) ):
       
        pass
    
    else:
       
        
        return (data[data['date']==init],[])
    


def classes_per(data):
    
    '''
        Inview detaails you can show different charts for individula culvers for about a week
        About Month - Premium
    '''

    '''
        This will give the percentage of total activity in a perticular class
    '''
    
    total_clasf = data['Prediction'].value_counts()
    
    pred = total_clasf.index
    d={}
    total = sum(total_clasf)
    
    
    for  i in range(len(pred)):
        d[pred[i]] = (total_clasf[i]/total)*100
            
    return d



def month_cou(data):
   
    mon_indx=0
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']
    #data['date'] =pd.to_datetime(data['date']).dt.strptime("%m/%d/%Y")
   ## data= data.sort_values(by="date")
    #data = data.sort("date")
    
    data2= (data['date'].map(lambda x: x.split('/')[mon_indx]))
    #data2= data2.sort_values(ascending=True,by="date")
   
    m = data2.value_counts(sort=True)
   
    df = {}
    for mon in m.index :
        
        df[months[int(mon)-1]] = str(m[mon])
    
   
    return df

def dates_spent(data,nan_dates):
    
    date = data['date'].value_counts()
    zeros = [0 for i in nan_dates]
    
    ddf = pd.DataFrame({"date":list(date.index)+nan_dates,"count":list(date)+zeros},index=None)
    ddf['Date']=pd.to_datetime(ddf['date'])
    ddf.sort_values(by=['Date'],ascending=True,inplace=True)
    
    
    ddf = ddf.iloc[:,:2]
    ddf['count']= ddf['count'].astype(str)
    
    return dict(zip(ddf['date'], ddf['count']))



def time_spent(data):
    '''
    Give the data specific to the day you want
    '''
    '''
        Inview detaails you can show different charts for individula culvers for about a week
        About Month - Premium
    '''
        
    d = {}

    #data = data[data['date']==date]
    data = data.iloc[::-1]
    
    time = pd.to_datetime(data['time']).dt.hour
    time = time.value_counts()
    
    key = list(time.keys())
          
    
    val = 0

    
    try:
        Max=max(key)
    except:
        Max=0
    for i in range(Max+1):
      
        if val in key:
            if(val<12):
                d[str(val)+" AM"] = str(time[val])
            else:
                d[str(val)+" PM"] = str(time[val])
        else:
            if(val<12):
                d[str(val)+" AM"] = str(0)
            else:
                d[str(val)+" PM"] = str(0)
            
        val = val + 1
        
    return d

def general_source(data):
    '''This is  general sourece graph data '''
    
    return data['urls'].value_counts()


def get_source_graph(data):
    '''
        This Will return Domain specific source graph
         
    '''
  
    total_clasf = data['Prediction'].value_counts()

    indx = total_clasf.index
    
    Clases={}

    for clas in indx:
        per_dom={}
        dat = data[data['Prediction'] == clas]
        
        domains = dat['urls'].value_counts()
        total = sum(domains)
        dom_index =  domains.index
        
        for i in range(len(dom_index)):
            
            per_dom[dom_index[i]] = str((domains[i]/total)*100)
            
        Clases[clas]=per_dom
        
            
    return Clases
    





def class_dist(data,individual_clases_list):
    
    d={}
    
    for Class in individual_clases_list:
        
        d[Class] = time_spent(data[data['Prediction']==Class])
        
    return d