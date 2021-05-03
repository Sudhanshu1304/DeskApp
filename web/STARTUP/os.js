


async function get_os(c_id){

   
 

    var value;
    if (c_id=="1"){
        value = "chrome";
    }
    else if(c_id == "2"){
        value = "firefox";
    }
    else if(c_id == "3"){
        value = "safari";
    }
    if (c_id =="4"){
        value = "other";

    }

  
    await eel.user_os(value)();
   
    window.close();

    
    


}