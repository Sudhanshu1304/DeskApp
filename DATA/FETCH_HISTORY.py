''' This File will run when the Update Function will be called !!!'''


import os
import platform
import browserhistory as bh
import webbrowser

#  Checking if te  Prediction_csv exist

def check_req(browser):
    
    name = False
    message = True # IF TRUE IMPLIES THAT THE USER HAS ALL THE NECESSARY OS REQUIRMENTS ELSE NOT 
    
    # I will check the OS  to kill the running window
    list_os = ['Windows','MacOS','Linux'] # this is nee3d becouse i need to know the comount to kill the active brouser in the perticular os
 
    
    # Brousers avalable = Firefox, Google Chrome, and Safari
    
    user_os = platform.system()
    
    
    with open('STATE/os.txt','w') as w:
        w.write(str(user_os))   
    
    
    if user_os in list_os :
        
        '''
            See we have to Off all the Browsers from the user but have to ask user which browsers data do he wants
            
        '''
                
        # Windoes User
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
            
            ''' ** DO RESERCH ON OTHER BROUSER BROUSER TO CLOSE THEM **'''
       
        # ['safari', 'chrome', 'firefox'] spel.. of browsers
        
        # print("CHROME IS : ",chrome,fire)
        dict_obj = bh.get_browserhistory()
       
        if browser in list(dict_obj.keys()):
            
            name = bh.get_username()
            bh.write_browserhistory_csv()
            
            '''
                Initalizing the ROW = 0 file
            
            '''
            with open('STATE/row.txt','w') as w1:
                w1.write("0")
                w1.close()
                  
            with open('STATE/name.txt','w') as w2:
                w2.write(name)
                w2.close()
            
            with open('STATE/browser.txt','w') as w3:
                w3.write(browser)
                w3.close()
                
                
        else:
            message = False
        
        '''
        If Chrome , firefox or Safari is True
        -> Ensure that we start them up again
        '''
        
        webbrowser.open_new("www.google.com")
    
    return message,name

       
    





def get_history():
    
    dict_obj = bh.get_browserhistory()
    name = bh.get_username()
    

    try:
        for key in dict_obj.keys():
            if key!='chrome':
                del dict_obj[key]
    except:
        pass

    bh.write_browserhistory_csv()
