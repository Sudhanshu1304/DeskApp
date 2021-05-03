import threading
import os
import eel
import pandas as pd
from DATA import Data_Manage
from AI import Analytics
import json 
import sys
import sklearn
import joblib
global DATAUPDATE


try:
    if os.path.exists('DATA/DATA/PREDICTED_DATA_CSV.csv') == True:
        th0 = threading.Thread(target = Data_Manage.Predict)
        th0.daemon = True
        th0.start()
        
    else:
        import main
 
        
except :
    pass
 

path1 = 'DATA/DATA/PREDICTED_DATA_CSV.csv'
#path2 = 'Backend/PREDICTED_DATA1.csv' # for testing'


if os.path.exists(path1) != False : # checking the condition for security
    

    '''This will check if there is any preprocessing Left'''
    # th1 = threading.Thread(target = Data_Manage.Predict)    
    # th1.start()
    
    
    data = pd.read_csv(path1) # **Temp Address**
    
    
    default_data , status = Analytics.get_range_data(data)

    
    @eel.expose
    def UpdateData():
        Data_Manage.Update()
        End()
     
        os.execl(sys.executable, sys.executable, *sys.argv)

    
    @eel.expose
    def last_update():
        with open('STATE/last_update.txt','r') as lup:
            last = lup.read()
            lup.close()
        with open('STATE/preprocess.txt','r') as r:
            state = str(r.read())
            r.close()
        with open('STATE/running.txt','r') as r2:
            running = str(r2.read())
        
        if(state!="True" and running !="True"):
            run = last
        else:
            run = "True"
        
     
        return run
    
    @eel.expose
    def Check_Update():
        with open("STATE/preprocess.txt" ,'r') as r:
            val = r.read()
        return val
    
    @eel.expose
    def class_percent(val = 1):
        if val == 1:
            # Today
            data1 = default_data
        elif val == 2:
            # This Week
        
            data1 , nan = Analytics.get_range_data(data ,week1=1)
            
            if len(nan) != 0:
                pass
                
        elif val == 3 :
            
            data1 , nan = Analytics.get_range_data(data ,Month1=1)
            
            if len(nan) != 0 :
                pass
                
        data1 = data1.reset_index(drop=True)
    
        d = Analytics.classes_per( data1 )

        return d
    
    @eel.expose
    def TIME_GRAPH(val1=1):
        th1=threading.Thread(target=time_graph)
        #time_graph(val1)    
        th1.start()
        
    
    @eel.expose
    def time_graph(val=1): # val is added if in future i want to add some date wise data
        global data
    
        d = {}
        if val == 1:
            '''This will show TODAY + Yesterday -> for comparision '''

            dic2 , nan =  Analytics.get_range_data(data,days=2)
       
            for date in dic2.keys():
                val = Analytics.time_spent(dic2[date])
           
                for k in val.keys():
                    val[k] = int(val[k])
                d[date] = val
            if len(nan) != 0:
                d[str(nan[0])]={0:0}
              
        else:
            
            dic2 , nan =  Analytics.get_range_data(data,days=7)
            for date in dic2.keys():
                val = Analytics.time_spent(dic2[date])
                for k in val.keys():
                    val[k] = int(val[k])
                d[date] = val
            if len(nan) != 0:
                print("DATES NOT PRESENT !!!!",nan)

            pass
        d2 = json.dumps(d)
      
        return d2
    
    @eel.expose
    def date_graph(val=1,gen_date=False):# val is added if in future i want to add some date wise data
        global data
        if val == 1: # =>1 week data
            data2,nan = Analytics.get_range_data(data,week1=1,gen_data=gen_date)
          
            date = Analytics.dates_spent(data2,nan)
           
            
        elif( val == 2):
            data2,nan = Analytics.get_range_data(data,Month1=1,gen_data=gen_date)
           
            date = Analytics.dates_spent(data2,nan)
        else:
           
            data2,nan = Analytics.get_range_data(data,week1=12,gen_data=gen_date)
          
            date = Analytics.dates_spent(data2,nan)
        
     
        date = json.dumps(date)
      
        return date
    
    @eel.expose
    def get_sources(val=1):
        ''''Give opt : 1. to choose time period 2. top 10,20 etc '''
        global data
        
        if val == 1:
            
            src  = Analytics.get_source_graph(default_data)
        elif(val == 2):
            # Week
            dat,nan = Analytics.get_range_data(data,week1=1)
            src  = Analytics.get_source_graph(dat)
        else:
            dat,nan = Analytics.get_range_data(data,Month1=1)
            src  = Analytics.get_source_graph(dat)
        
        
        src = json.dumps(src)
    
        return src
    
    @eel.expose
    def general_sources(val = 1):
        global data
        
        d2={}
        if val == 1:      
            d = Analytics.general_source(default_data)
        
        elif(val == 2): 
            g_src,nan = Analytics.get_range_data(data,week1=1)
            d  = Analytics.general_source(g_src)
        else:
            g_src,nan = Analytics.get_range_data(data,Month1=1)
            d  = Analytics.general_source(g_src)
            
        for k in d.keys():       
            d2[k] = str(d[k])
            
        d = json.dumps(d2)
        
        return d
    
    @eel.expose
    def indi_class_dist(val=1,Class=["AI","GameD","WebD","AppD","Entertainment","Social Media","Lang"]):
        global data
        
        if val ==1:
            d = Analytics.class_dist(default_data,Class)
            
            
        else:
            pass
            
        d = json.dumps(d)
        return d

    @eel.expose
    def month_data():
        
        mon_data = Analytics.month_cou(data)
        return json.dumps(mon_data)
    

    @eel.expose
    def End():
        global data,default_data,dic,nan
        data = pd.read_csv(path1)
        default_data , status = Analytics.get_range_data(data)
        dic , nan =  Analytics.get_range_data(data,days=2)
        
        
    eel.init('web')
    eel.start('test.html')
    try:
        eel.start('test.html',port=27000)
    except Exception as e:
        print(e)
        try:
            eel.start('test.html',port=15000)
        except:
            eel.start('test.html')
        
                
        

    
    
  