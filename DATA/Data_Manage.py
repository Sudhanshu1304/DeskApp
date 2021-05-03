#from main import close
import pandas as pd
import browserhistory as bh
from AI.AI import total_preprocess , Classify ,load_model
import threading 
import os
from datetime import datetime


'''
We will can Classify function even for update - > it will then see if previous preprocessing is left or not if not then it will send it to preprocess fun which will 
First update the history.csv 
then check if there is any update 

if updated =True :
    update the first_preprocess.csv 
    Call the Classify function
    


'''

def update_prediction(latest,pre_processed):
  
    history = latest
    prev_p = pre_processed
    date_col = history['date']
    lis = date_col.str.split(expand=True).iloc[:,0]
   
    try:
        date = pd.to_datetime(lis).dt.strftime("%m/%d/%Y")# 100%data
      
    except:
        try:
            lent = int(len(lis)*0.9) #90%data
            lis = lis.iloc[:lent]
            date = pd.to_datetime(lis).dt.strftime("%m/%d/%Y")
        
        except:
       
            lent = int(len(lis)*0.5) #90%data
            lis = lis.iloc[:lent]
            date = pd.to_datetime(lis).dt.strftime("%m/%d/%Y")
         
    
    d = (date[(date==prev_p['date'][0])])
  
    ind=d.index[-1]
   
    prediction_data = pd.read_csv("DATA/DATA/PREDICTED_DATA_CSV.csv")

    pred_indx = prediction_data[prediction_data['date']==prev_p['date'][0]].index[-1]
 
 
    prediction_data2 = prediction_data.iloc[pred_indx+1:]#don't include pred_indx
   
    prediction_data2.to_csv("DATA/DATA/PREDICTED_DATA_CSV.csv",index=False)

    return history.iloc[:ind+1]


    
def preprocess(): 
    with open('STATE/update.txt','r') as r2:
        valu = str(r2.read())
    if(valu=='True'):
        with open("STATE/row.txt",'w') as wt :
            wt.write("0")
        with open("STATE/update.txt",'w') as up :
            up.write("False")
    #print("Preprocessing....")
    '''
        Here I will check if I have some new data for preprocessing (for the first most case it wil be first preprocessing ...)

    '''
    with open('STATE/browser.txt','r') as r:
        browser = r.read() 
        r.close()
    
    # print("Browser detected is : ", browser)                                                                                                                                                                                                                     
    
    
    #path="C:\\Users\\SUDHANSHU\\PycharmProj\\Tracker\\chrome_history.csv"
    '''Somthing wrong'''
    # New hIstory
    history = pd.read_csv("{}_history.csv".format(browser))#(path,header=None) #("{}_history.csv".format(browser))
    
    history.columns =['urls','text','date'] 
    
    #history
    
    try:
        
        if  os.path.exists('DATA/DATA/first_preprocess.csv') != True :
           
            
            #print(history.head(5))
            data = total_preprocess(history)
            with open("STATE/gen_date.txt",'w') as gd:
                gd.write(data['date'][0])
                gd.close()
                
            
            
            data.to_csv("DATA/DATA/first_preprocess.csv",index=False)
            
            Predict()
            
            
            
        
        else:
            with open('STATE/preprocess.txt','r') as r:
                state = r.read()
                r.close()
            if(state=='True' or valu =='True' ):
                
               
                prev_p = pd.read_csv('DATA/DATA/first_preprocess.csv')
               
                
               
                to_preprocess = update_prediction(history,prev_p)
              
                data = total_preprocess(to_preprocess)
                
                data.to_csv("DATA/DATA/first_preprocess.csv",index=False)
                
                with open('STATE/preprocess.txt','w') as w1:
                    w1.write('True')
                    
                Predict()
           
    
    except:
   
        pass
            

def Predict():
    
    
    
    try:
        with open('STATE/running.txt','w') as w:
            w.write('False')
            
        try:
            with open('STATE/preprocess.txt','r') as r:
                state = r.read()
                r.close()
        except:
            with open('STATE/preprocess.txt','w') as w:
                w.write('False') # => call Preprccess for new data
                w.close()
                state = 'False'
        
        if state == str(True) : # implies that there is some un predicted preprocessed data
            
           
            pre_data = pd.read_csv('DATA/DATA/first_preprocess.csv')
          
            model , mod_len , token , ohe = load_model('AI/MODELS/nlp_mod_1_1','AI/MODELS/tok_model_1_1','AI/MODELS/encoder_model1')
      
            
            with open('STATE/first.txt','r') as r:
                first = str(r.read())
                
            if first == str(True):
               
                Classify(pre_data,model,token,mod_len,ohe)
            else:
              
                Classify(pre_data,model,token,mod_len,ohe,second=True)
        
        else:
           
            preprocess()
    
    except :
      
        pass
        '''To ensure In case User Direcetly Clossed the Application in the mid of working !!! '''
        
            

        
def Update(): # Should be called using Threading
    
   
    try:
        
        with open('STATE/preprocess.txt','r') as r:
            state = str(r.read())
            
        with open('STATE/running.txt','r') as r:
            running = str(r.read())
        
        if(state!="True" and running !="True"):
                
            if os.path.exists('DATA/DATA/PREDICTED_DATA_CSV.csv') == True :
                with open('STATE/update.txt','w') as w:
                    w.write(str(True))
                try:
                    with open('STATE/os.txt','r') as r:
                        user_os = str(r.read())
                except:
                    import platform
                    user_os = platform.system()
                    with open('STATE/os.txt','w') as w:
                        w.write(str(user_os))
                
                
                if user_os == 'Windows':
                    
                    try:
                        os.system("taskkill /im chrome.exe /f") # **for now**
                        chrome= True # It has been closed
                    except:
                        chrome = False
                    try:
                        os.system("taskkill /im firefox.exe /f")
                        fire = True
                    except:
                        fire = False
                        
                    '''
                        ADD FOR SAFARI
                        
                    '''
                    
                # MacOS User
                elif( user_os == 'MacOS'):
                    
                    try:
                        os.system("killall -9 'Google Chrome'")
                        chrome = True
                    except:
                        chrome  = False
                        
                    '''
                        ADD FOR FIREFOX , SAFARI
                    '''
                    
                else: # Linux User
                    
                    '''
                        ADD FOR Chrome ,FIREFOX , SAFARI
                        
                    '''

                with open("STATE/browser.txt",'r') as r:
                    browser = r.read()
            
                # old_hist = pd.read_csv("{}_history.csv".format(browser))
                # old_hist.to_csv('old_hist.csv',index=False)
                bh.write_browserhistory_csv()

                
                now = datetime.now()
                dt = now.strftime("%d/%m/%Y %H:%M:%S")
                    
                with open('STATE/last_update.txt','w') as lup:
                    lup.write(str(now))
                    lup.close()
                    
            
                
                with open("STATE/first.txt",'w') as w:
                    w.write("False")
                
                with open('STATE/preprocess.txt','w') as w:
                    w.write("False")
                
                with open("STATE/row.txt",'w') as wt :
                    wt.write("0")
                    
                # if state == str(False) and running == str(False): # => the
                #     preprocess()
                    
    except:
        pass

























