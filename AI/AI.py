'''
 You have to ensure that the data which you are giving it is of proper size
 
 >  It will take in the data provided 
    -> Preprocess it 
    -> Classifi
    -> Create the Prediction_CSV
    -> Will update the database (Prediction_CSV)

'''

import os
import pandas as pd
import numpy as np
from datetime import datetime
import datetime as dt
import re
from tensorflow import keras
import tensorflow as tf
import pickle
from tld import parse_tld
from tensorflow.python.platform.tf_logging import error

os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



'''  Preprocessing Date  '''


''' This Function will format the date time and will add the reguired extra data'''


def get_format(date):
    
    form1 = "%m/%d/%Y"
    form2 = "%Y-%m-%d"
    form3 = "%Y-%d-%m"
    form4 = "%d/%m/%Y"
    form5 = "%Y/%m/%d"
    form5 = "%Y/%d/%m"
    form6 = "%d-%m-%Y"
    form7 = "%m-%d-%Y"
    
   # date2 = str(date[0])  datetime.strptime(data22['date'][0].split(' ')[0], "%m/%d/%Y").date()
    
    date2 = date#['date'][0].split(' ')[0]
 
    try:
       
        datetime.strptime(date2, form1).date()
     
        date_format = form1
   
    
    except:
        try:
         
            datetime.strptime(date2, form2).date()
            date_format = form2
        except:
            try:
            
                datetime.strptime(date2, form3).date()
                date_format = form3
            except:
                try:
                    datetime.strptime(date2, form4).date()
                    date_format = form4
                except:
                    try:
                        datetime.strptime(date2, form5).date()
                        date_format = form5
                    except:
                        try:
                            datetime.strptime(date2, form1).date()
                            date_format = form6
                        except:
                            try:
                                datetime.strptime(date2, form7).date()
                                date_format = form7
                            except:
                                date_format = str(-1)

                                
    return date_format
                      
def org_date(DATA): # 00:00 AM
    
   
    drop =  [] # this will contain the rows which was gave error while processing , these will be removed
    data = DATA.copy()
    date = data['date']
    time = data['time']
    
    time_diff =[0] # initilized with zero cuz first element has no previous element for difference .
    
    # time format
    time_format = '%H:%M'
    
    # latest date
    
    prev_date = date[0]
    
    date_format = get_format(date[0])
    
    data['date'][0] =  dt.datetime.strptime(date[0], date_format).strftime('%m/%d/%Y')
    
    # Latest time  : if date changes == True : init_time is == that date first occured time
    prev_time =  datetime.strptime(time[0], time_format)#data['date'][0]

    for i in range(1, data.shape[0]):
     
        try:
           
            date_i = date[i]
            
            
            try:
              
                val = dt.datetime.strptime(date_i, date_format).strftime('%m/%d/%Y')
                 
                year = val[-4:]
            
                if int(year) < 2000 :
                  
                    drop.append(i)
                    continue
             
                data['date'][i] = val
              
                '''This is just to remove the columns with untracked Date formats'''

            except:
               
                date_format = get_format(date_i)
              
                if date_format == '-1' :
                   
                    drop.append(i)
                    continue     
                
                val = dt.datetime.strptime(date_i, date_format).strftime('%m/%d/%Y')
                year = val[-4:]
                if int(year) < 2000 :
                    drop.append(i)
                    continue
                    
                data['date'][i] = val
                
                '''This is just to remove the columns with untracked Date formats'''

                
            
            time_i = datetime.strptime(time[i], time_format)
            
            flag = 0
            
            if prev_date != date_i : 
                prev_date = date_i
                time_diff.append(0)
                flag = 1

           
            tdelta = abs(time_i - prev_time)
            tdelta = (tdelta.total_seconds()/60)
            if flag == 0 :
                time_diff.append(tdelta)
            prev_time = time_i
    
        except :
            
            
            drop.append(i)
            continue
    
    data = data.reset_index(drop=True)
    
    
    data.drop(drop, axis= 0 , inplace =True)
    df = pd.DataFrame({'del_time':time_diff},index = data.index)
    data = pd.concat([data,df],axis=1)
 
    return data
    
def org_url_main(DATA):
    data = DATA.copy()
    for i in range(data.shape[0]):
         
        url = (parse_tld(data['urls'][i]))
        
        if(url[0]!=None):
            if(url[2]=='www' or url[2]=='' or url[2]=='open'):
                data['urls'][i] = url[1]
            else:
                data['urls'][i] = url[2]
        else:

            data['urls'][i] = "local host"

    return data  
    
def org_url(DATA):
    print("using org ")
   
    drop=[]
    data= DATA.copy()

    for i in range(data.shape[0]):
        dat= data.iloc[i,0]
        if '//' in dat:
            dash=dat.split('//',1)[1]
            if '.co' in dash :     
                com=dash.split('.co',1)[0]       
                if 'www.' in com:            
                    www=com.split('www.',1)[1]
                else:
                    www=com     
                if len(www)>=100:
                    drop.append(i)
                else:
                    data.iloc[i,0]=www             
            else:        
                drop.append(i)           
        else:   
            drop.append(i)
    data.drop(drop,axis=0,inplace=True)
 
    return data 


'''  Text Cleaning '''

''' This will remove all the Symboles '''


puncts = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']', '>', '%', '=', '#', '*','¤','▢',
          '□', '\\', '•',  '~', '@', '£', 
 '·', '_', '{', '}', '©', '^', '®', '`', '→', '°', '€', '™',   '♥', '←', '×', '§', '″', '′', 'Â', '█', '½', 'à', '…', 
 '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―', '¥', '▓', '—', '‹', '─', 
 '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸', '¾', 'Ã', '⋅', '‘', '∞', 
 '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø', '¹', '≤', '‡', '√', ]

# data : text columns 
def clean_data(data , replace_with = '-' ):

    def clean_text( x,replace_with = replace_with ):
        x = str(x)
        for punct in puncts:
            if punct in x:
                x = x.replace(punct, replace_with)
        return x

    for i in range(data.shape[0]):
        
        data.iloc[i] = clean_text(data.iloc[i] ,replace_with )
    
    return data


''' Cleaning the Numbers '''

def clean_data_num(data):
    
    def clean_numbers(x):
        if bool(re.search(r'\d', x)):
            x = re.sub('[0-9]{5,}', '#####', x)
            x = re.sub('[0-9]{4}', '####', x)
            x = re.sub('[0-9]{3}', '###', x)
            x = re.sub('[0-9]{2}', '##', x)
        return x

    
    for i in range(data.shape[0]):
        data.iloc[i] = clean_numbers(data.iloc[i])
    
    return data

'''  Expand the Contractions'''

def clean_contractions(data):
    
    contraction_dict = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not", "didn't": "did not",  "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not", "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",  "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would", "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would", "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have","it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have", "must've": "must have", "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is", "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have","so's": "so as", "this's": "this is","that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would", "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", "they'd've": "they would have", "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are",  "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is", "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have", "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have", "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have","you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have", "you're": "you are", "you've": "you have"}

    def _get_contractions(contraction_dict):
        contraction_re = re.compile('(%s)' % '|'.join(contraction_dict.keys()))
        return contraction_dict, contraction_re

    contractions, contractions_re = _get_contractions(contraction_dict)

    def replace_contractions(text):
        def replace(match):
            return contractions[match.group(0)]
        return contractions_re.sub(replace, text)


    for i in range(data.shape[0]):
        data.iloc[i] = replace_contractions(data.iloc[i])
    
    return data


'''             TEXT PREPROCESSING MODULE               '''

def data_preprocess(data , replace_with =''):

    text=data.str.lower()
    text = clean_data(text , replace_with= replace_with)
    #text= clean_data_num(text)
    text = clean_contractions(text)
  
    return text




'''            Total Preprocessing of DATA            '''


def total_preprocess(DATA):
    
    '''    '''
    print("Pre start")
    with open('STATE/preprocess.txt','w') as w:
        w.write('True')
   
    
    try:
        
        data =  DATA.copy()
        date_col = data['date']
        data.drop(['date'],axis=1,inplace=True)
        
        lis = [e.split(' ') for e in date_col ]
      
        new_date =np.array(lis)
        new_date_col = new_date[:,0]
        #new_time_col = new_date[:,1]
        new_time_col = np.array([":".join(e.split(':')[:2])  for e in  new_date[:,1]])
     
        df = pd.DataFrame({'date':new_date_col,'time':new_time_col})
        dat = pd.concat([data,df],axis=1)
    
        ''' organizing the Dates Data'''
        dd = org_date(dat)
        we = pd.to_datetime(dd['date']).dt.day_name()
        dd['week'] = we
    
 
        '''  organizing urls data ''' 
        print("org start")
        dd = org_url(dd)
        print("org end")
        '''  text preprocess '''
    
        dd['urls'] = dd['urls'].str.lower()
        #dd['urls'] = dd['urls'].str.replace('.','_')
        dd['text'] = data_preprocess(dd['text'])
        
    
        dd = dd.reset_index(drop=True)

        print("Pre End")
        return dd

    except:
     
        with open('STATE/running.txt','w') as w:
            w.write('False')
    
   


'''                      LOAD MODEL                     '''

def load_model(mod_name,token_name,encod_name):
    
    
    
    # Model
 
    model = keras.models.load_model(mod_name)
 
    # Mod_Len
    with open('AI/MODELS/mod_len.txt','r') as f:
        mod_len = int(f.read())
        f.close()
 
    
    # Token 
    with open(token_name, 'rb') as handle1:
        token = pickle.load(handle1)
        handle1.close()

    # OHE
    try:
        with open(encod_name, 'rb') as handle:
        
            ohe = pickle.load(handle)
           
            handle.close()
    except Exception as error:
        print('error in getting ohe!!! :',error )
    
    '''
    
        Solve teh ERROR OF LOADING OHE
    
    '''
    return (model,mod_len,token,ohe)

'''                     Predicted                '''


def Predict(model,token,text,max_len,ohe):
    
 
        
    # token obj        
    text_ =token.texts_to_sequences([text])
    # padding
    text_ =tf.keras.preprocessing.sequence.pad_sequences(text_,maxlen=max_len,padding='post')
    
    
    pre = model.predict(text_)
    
    prediction = ohe.inverse_transform(pre)[0][0]
    
    Confidence = max(pre[0])*100
    

    
    
    return (prediction,Confidence)
    
    
'''                     Classify             '''
# data,model,token,mod_len,ohe,min_confidence=5.0


def PredFun(data,i,model,token,text,mod_len,ohe,min_confidence):
    prediction=[]
    confidence=[]
    social = ['github','mail','discord','linkedin','instagram','hangouts','whatsapp']
    if(data['urls'][i] in social):
        d = ["Social Media",100.0]
    elif(data['urls'][i] =='local host'):
        d = ["WebD",100]
    else:
        d = Predict(model,token,str(text),mod_len,ohe)

    if d[1] <= min_confidence :
        try:
            
            prediction.append('Entertainment')#(prediction[len(prediction)-1])
            confidence.append(d[1])#(confidence[len(confidence)-1])
        except:

            prediction.append(d[0])
            confidence.append(d[1])
    else:

     
        prediction.append(d[0])
        confidence.append(d[1])
    
    return [prediction[0],confidence[0]]


def Classify(data,model,token,mod_len,ohe,min_confidence=10.0,second =False):
    
    
   
    try:
        i=0
        state = ''
      
        with open('STATE/preprocess.txt','r') as r1:
            state = r1.read()
            r1.close()
            
        state = str(state)
      
        if state == str(True) :
         
            if second == True :
               
                data = data.iloc[::-1]

            data = data.reset_index(drop=True)
           
            prediction = []
            confidence = []
            
            '''
                Here you have to also add the condition if the urls 

            '''
           


            path = 'STATE/row.txt'
            path2 = 'DATA/DATA/PREDICTED_DATA_CSV.csv'
           
            
            try:
                with open(path,'r') as r:
                    row = r.read()
                    r.close()
            except:
                with open(path,'w') as w:
                    w.write('0')
                    w.close()
                    row=0
                    
            row = int(row)
          
            start = data['date'].iloc[row]

       
            for i in range(row ,data.shape[0]):
                text = data['text'].iloc[i]
                print('i ',i)
             
           
                if (data['date'].iloc[i] != start or i==len(data)-1):#
                        
            
                    start = data['date'].iloc[i]
                
                    with open(path,'r') as r :
                        row = r.read()
                        r.close()

                    row = int(row)
                 


                    if row!=0 or second == True:
                        
                        if(i==len(data)-1):
                         
                            pred_cofi = PredFun(data,i,model,token,text,mod_len,ohe,min_confidence)
                            prediction.append(pred_cofi[0])
                            confidence.append(pred_cofi[1])
                            main_data_sec = data.iloc[row:i+1,:] # this is a section of original data  
                        else:
                          
                            main_data_sec = data.iloc[row:i,:] # this is a section of original data  
                     
                        df = pd.DataFrame({'Prediction':prediction,'Confidence':confidence},index=main_data_sec.index)
                       
                        dc = pd.concat([main_data_sec,df],axis=1) # in that sec i have added prediction and confidence column 
                     
                        saved_data = pd.read_csv(path2)
                       
                        if second == True :
                          
                            dc = dc.iloc[::-1]
                            updated_data = pd.concat([dc,saved_data],axis = 0).reset_index(drop=True)
                          

                        else:
                            
                            updated_data = pd.concat([saved_data,dc],axis = 0)
                       

                        updated_data.to_csv(path2 ,index=False)
                        
                    else:
                      
                        main_data_sec = data.iloc[row:i,:]
                        df = pd.DataFrame({'Prediction':prediction,'Confidence':confidence},index=main_data_sec.index)
                        dn =pd.concat([main_data_sec,df],axis=1)
                        dn.to_csv(path2,index=False)
                        with open("STATE/Closewelcome.txt",'w') as w:
                            w.write('True')

                    prediction = []
                    confidence = []


                    with open(path,'w') as w:
                        w.write(str(i))
                        w.close()

                pred_cofi = PredFun(data,i,model,token,text,mod_len,ohe,min_confidence)
                prediction.append(pred_cofi[0])
                confidence.append(pred_cofi[1])
                

        else:
            print("Nothing to Predict!!!")

    except :
       
        pass
    
    if (i==data.shape[0]-1):
        
        with open('STATE/first.txt','w') as w3:
            state = w3.write("False")
            w3.close()
        
        with open('STATE/preprocess.txt','w') as w1:
            state = w1.write("False")
            w1.close()

    with open("STATE/row.txt",'w') as wt :
        wt.write("0")
    
 
    

'''                    MODEL MACKING              '''


def Make_Prediction(data):
    
    '''
    
        This is a Greneral Method and should be used in all the cases except the FIRST STEP OF THE prediction_csv making (In this all the indidual steps will be done diffrentelly).
        
    '''
    
    DATA = total_preprocess(data)
    
    model , mod_len , token , ohe = load_model('MODELS/test_model1','MODELS/tok_model1','MODELS/encoder_model1')
    
    prediction = Classify(DATA,model,token,mod_len,ohe)
    
    return prediction
    











# def Classify(data,min_confidence=5.0):
    
#     prediction = []
#     confidence = []
    
#     '''
#         Here you have to also add the condition if the urls 
    
#     '''
   
#     start = data['data_del'][0]
    
    
    
#     with open('STATE/row.txt') as r:
#         row = r.read()
#     r.close()
#     cou = row
    
#     for text in data['text'][row:]:
        
#         if (data['date_del'][cou] != start):
            
#             with open('STATE/row.txt') as r:
#                 row = r.read()
#             r.close()
            
#             df = pd.DataFrame({'Prediction':prediction,'Confidence':confidence})
            
            
            
#             if row!=0:
#                 dd = pd.read_csv('path')
#                 dc = pd.concat([dd,df],axis=1)
#                 dc.to_csv('path')
#             else:
#                 df.to_csv('path')
            
#             prediction = []
#             confidence = []
            
            
#             with open('STATE/row.txt') as w:
#                 w.write(cou)
#             w.close()
            
            
#         d = Predict(model,token,str(text),mod_len,ohe)
        
#         if d[1] <= min_confidence :
#             try:
#                 print('{}    :  {}'.format(text,d[0]))
#                 prediction.append(prediction[len(prediction)-1])
#                 confidence.append(confidence[len(confidence)-1])
#             except:
                
#                 prediction.append(d[0])
#                 confidence.append(d[1])
#         else:
            
#             #print('{}    :  {}'.format(text,d[0]))
#             prediction.append(d[0])
#             confidence.append(d[1])
#         cou = cou + 1
    
#     df = pd.DataFrame({'Prediction':prediction,'Connfidence':confidence})
    
#     return pd.concat([data,df],axis=1)
        
        