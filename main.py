import os
import threading
import eel
from datetime import datetime

from DATA import FETCH_HISTORY as fh
from DATA import Data_Manage


if os.path.exists('DATA/DATA/PREDICTED_DATA_CSV.csv') == True:

    pass
    
    
    
else:
    
    import eel
    
    message = True
    welcome = False
    error = False

    try:
        with open('STATE/name.txt','w') as r:
            name = r.read() 
            name = "Hello "+str(name)
    except:
        name ="Hello"
        


    try:
        
        if os.path.exists('DATA/DATA/PREDICTED_DATA_CSV.csv') == False:
            try:
                 os.mkdir('STATE')
            except:
                pass
         
            # first.txt => if the opreation is the firast most setup state 
            with open('STATE/first.txt','w') as w:
                w.write('True')
                w.close()
              
            with open("STATE/update.txt",'w') as up :
                up.write("True")
                up.close()
         
            with open("STATE/Closewelcome.txt",'w') as w2:
                w2.write('False')
                w2.close()
            # with open('STATE/preprocess.txt','w') as w3:
            #     w3.write('True')
            #     w3.close()
            with open('STATE/row.txt','w') as w1:
                w1.write('0')
                w1.close()
            
            now = datetime.now()
            dt = now.strftime("%d/%m/%Y  %H:%M")
                
            with open('STATE/last_update.txt','w') as lup:
                lup.write(str(now))
                lup.close()
                
           
                                                      
            cur_dir = os.getcwd()
            eel.init(cur_dir+'\\'+'web\\STARTUP')
            
            @eel.expose
            def user_os(val): # it  will take the name of os selected by the user
                global welcome,error,name
                
                if val !="other":
                
                    message,name = fh.check_req(val)

                    welcome = True
                    
                    return [message,name]

                else:
                    
                
                    error = True
                
            try:
                eel.start('os.html',size=(600,550),port=27000)
            except Exception as e:
                try:
                    print(e)
                    eel.start('os.html',size=(600,550),port=15000)
                except:
                    eel.start('os.html',size=(600,550))

    except :
        pass
       
     
        '''WELCOME PAGE'''
        
    if welcome == True:
        try:
     
            eel.init('web/STARTUP')
            
            th0 = threading.Thread(target = Data_Manage.Predict)
            th0.daemon = True
            th0.start()
            
            @eel.expose
            def get_name():
                return [name]
            
            @eel.expose
            def close():
                with open("STATE/Closewelcome.txt",'r') as r:
                    val = r.read()
                return val               
    
          
            try:
                eel.start('welcome.html',size=(600,550),port=27000)
            except Exception as e:
                try:
                    print(e)
                    eel.start('welcome.html',size=(600,550),port=15000)
                except:
                    eel.start('welcome.html',size=(600,550))
            
            
        except :
           
            pass

    else:
      
        eel.init('web/STARTUP')
        try:
            eel.start('error.html',size=(600,600),port=27000)
        except Exception as e:
            try:
                eel.start('error.html',size=(600,600),port=15000)
            except:
                eel.start('error.html',size=(600,600))



def End():
   
    try:

        import sys
      
        import graph
        
    
    except :
        print("Thread is not ON!! ")
        

