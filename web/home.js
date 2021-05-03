
//console.log("hmm");



checkupdatecou = 0;
async function general(val = 1,DEL1=false , val2=1){

    

    if(typeof mychart_gen_src!='undefined'){
        mychart_gen_src.destroy();
    }

    general_class(val,DEL1);
    general_time(val2);
    general_date(gen_date=true);
    inclass_dist();
    general_source(1,"gsg");//general source graph 1;
}




function CheckUpdate(){

    var sec=1;
    var a = setInterval(async function(){
        console.log("Sec is :",sec);
        document.getElementById("ref_notify").innerHTML=String("Auto Refresh In "+String(15-sec));
        document.getElementById("ref_notify").style.color="blue";
        if(sec%15==0){
            sec=1;
            var val = await eel.Check_Update()();
            console.log("Showing  ",val);
            
            if(val!="True"){
                console.log("Ented end");
                document.getElementById("ref_notify").style.display='none';
                Refresh();
                clearInterval(a);
                Refresh();
                //checkupdatecou = checkupdatecou + 1;
                console.log("Calsed 2: ",checkupdatecou);
            }
            else{
                Refresh();
            }
        }
        sec = sec+1;
        
        
    },1000);
    
}

function destroy(elem){

    
    if(typeof elem!='undefined'){
        elem.destroy();
    }
    
}

function graph(element,type,label,X,Y){

    var ctx2 = document.getElementById(element).getContext('2d');//bgsc1=>bar source graph 1
    mychart = new Chart(ctx2, {
        type: type,
        data: {

            datasets:[{
                data : Y,
                label:label
            }],
            labels:X

        },
       
    });

}

async function date_dist_page(val=1){

    var data = await eel.date_graph(val)();
    data = JSON.parse(data);
    var dates = Object.keys(data);
    var values = Object.values(data);

    if(typeof mybarChart44!='undefined'){
        mybarChart44.destroy();
    }

    var ctx2 = document.getElementById('datedist').getContext('2d');

    //ctx2 = document.getElementById('pai1').getContext('2d');
    var blue = ctx2.createLinearGradient(0, 100, 300, 700);
    blue.addColorStop(0, '#0081ff');
    blue.addColorStop(1, '#0045ff');

    var org = ctx2.createLinearGradient(0, 100, 300, 700);
    org.addColorStop(0, '#d09693 ');
    org.addColorStop(1, '#c71d6f');


    mybarChart44 = new Chart(ctx2, {
        type: 'bar',
        data: {
            datasets:[{
                data : values,
                backgroundColor:blue,
                label:"Bar"
            },
            {
                type: 'line',
                data:values,
                backgroundColor:org,
                label:"Area"
            }
        
        ],
            labels:dates

        },
        options: {
            maintainAspectRatio:false,
            responsive: true,
        },
    }
    );


    data = await eel.month_data()();
    data = JSON.parse(data);
    var x = Object.keys(data);
    var y = Object.values(data);

    if(typeof mybarChart45!='undefined'){
        mybarChart45.destroy();
    }

    var ctx3 = document.getElementById('mondist').getContext('2d');

    var red = ctx3.createLinearGradient(0, 100, 300, 700);
    red.addColorStop(0, 'rgb(255, 8, 68)');
    red.addColorStop(1, 'rgb(255, 177, 153)' );

    mybarChart45 = new Chart(ctx3, {
        type: 'bar',
        data: {
            datasets:[{
                data : y,
                backgroundColor:red,
                label:"Months"
            },
        ],
            labels:x

        },
        options: {
            maintainAspectRatio:false,
            responsive: true,
        },
    }
    );



}


async function timepageddist(val){

    var dic2 = await eel.time_graph(val)();
    dic2 = JSON.parse(dic2);
    DATES = Object.keys(dic2);


    // Main

    var multiply = {
        beforeDatasetsDraw: function(chart, options, el) {
        chart.ctx.globalCompositeOperation = 'multiply';
        },
        afterDatasetsDraw: function(chart, options) {
        chart.ctx.globalCompositeOperation = 'source-over';
        },
    };


  
    var BG = ['#FFFFFF'];
    var PBG = ['FFFFFF'];

    Days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];

    if(typeof mychart_tdist =="undefined"){
        console.log("FIRSTTTTTTTTT");
        for(i=0; i<DATES.length;i++){

            var elem = "today-"+String(i);
        
            var td = DATES[i] ;
            var ts = new Date(DATES[i]);
            console.log("%%%%%%%%%%\n",Days[ts.getDay()],ts.getDay(),ts);
            //console.log("NAMES : ",ts.getDayName());
            document.getElementById("tday"+String(i)).innerHTML=Days[ts.getDay()];
            var x = Object.keys(dic2[td]);
            var y = Object.values(dic2[td]);
     
            var ctx2 = document.getElementById(elem);//bgsc1=>bar source graph 1
            var grad = ctx2.getContext('2d').createLinearGradient(0, 0, 0, 150+i*100);
            grad.addColorStop(0, '#FF55B8');
            grad.addColorStop(1, '#FF8787');
            this["mychart_tdist"+i] = new Chart(ctx2, {
                type: 'line',
                data: {
    
                    datasets:[{
                        data : y,
                        label:DATES[i],
                        backgroundColor: grad,
                        pointBackgroundColor: BG[0],
                        pointBorderColor: PBG[0],
                        lineTension: 0.40,
                    }],
                    labels:x
    
                },
                options: {
                    maintainAspectRatio:false,
                    responsive: true,
                },
                plugins: [multiply],
            
            });
        }
    }
    else{
        console.log("SECOUNDDDDDDDDDDDD");
        var inp = [mychart_tdist0,mychart_tdist1,mychart_tdist2,mychart_tdist3,mychart_tdist4,mychart_tdist5,mychart_tdist6];
        for(i=0; i<DATES.length;i++){

            //elem = "today-"+String(i);
            var td = DATES[i] ;
            console.log("NAMES22 : ",Date(td).getDayName());
            var x = Object.keys(dic2[td]);
            var y = Object.values(dic2[td]);
            
            inp[i].data.datasets[0].label = td;
            inp[i].data.datasets[0].data=y;
            inp[i].data.labels = x;
            inp[i].update();
        }
        
    }
    

}


async function inclass_dist(){
    //console.log("HADUYQW CLASES");
    var data = await eel.indi_class_dist()();
    //console.log("INDI CLASES",data);
    data = JSON.parse(data);

    var Name = Object.keys(data);
    console.log("HADUYQW CLASES ; ",Name);
    var nam1 = Name[0];
    var X1 = Object.keys(data[nam1]);
    
    var nam1y = Object.values(data[nam1]);

    var nam2 = Name[1];
    var nam2y = Object.values(data[nam2]);
    var X2 = Object.keys(data[nam2]);
   
    var nam3 = Name[2];
    var nam3y = Object.values(data[nam3]);
    var X3 = Object.keys(data[nam3]);
    

    var nam4 = Name[3];
    var nam4y = Object.values(data[nam4]);
    var X4 = Object.keys(data[nam4]);

    var nam5 = Name[4];
    var nam5y = Object.values(data[nam5]);
    var X5 = Object.keys(data[nam5]);

    var nam6 = Name[5];
    var nam6y = Object.values(data[nam6]);
    var X6 = Object.keys(data[nam6]);

    var nam7 = Name[6];
    console.log("Names were : ",nam7);
    var nam7y = Object.values(data[nam7]);
    var X7 = Object.keys(data[nam7]);

    var get = [X1,X2,X3,X4,X5,X6,X7];

    var lar = [X1.length,X2.length,X3.length,X4.length,X5.length,X6.length,X7.length];
    //console.log("GET IS : ",lar);
    
    var i = lar.indexOf(Math.max(...lar));
    //var i = a.reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0);
    
    
    var X = get[i];
    console.log("IN CLASS DIST :",X);
    if(typeof mychart!='undefined'){
        mychart.destroy();
    }

    var canvas = document.getElementById('CLSDIST').getContext("2d");//
    
    // var redd = canvas.createLinearGradient(0, 400, 700, 900);
    // redd.addColorStop(0, "rgba(131,58,180,0.6)");
    // redd.addColorStop(1, "rgba(253,29,29,0.6) ");
   


    
    var config = {
        type: 'line',
        data: {
            labels: X,
            datasets: [
              {
                  label: nam1, //'This week',
                  data: nam1y,//[24, 18, 16, 18, 24, 36,28,
                 
                  borderColor:'white',
                  //backgroundColor:"#208ce3",
                  
                  backgroundColor:"rgba(237,51,76,0.7)",//"rgba(255, 0, 51,0.7)",
                  //backgroundColor:"rgba(105, 30, 66, 0.2)" ,
                  hoverBackgroundColor:"rgba(255, 0, 51,1)",
                  //fill: false,
                  //pointBackgroundColor: '#FFFFFF',
                  //pointBorderColor: '#FFFFFF',
                  //lineTension: 0.40,
              },
              {
                label: nam2, //'This week',
                data: nam2y,//[24, 18, 16, 18, 24, 36,28,
                //backgroundColor:  "rgba(205, 102, 100, 0.2)",
                //borderColor: "#e6515a",
                borderColor:'white',
                backgroundColor:" rgba(22,219,146,0.7)",
                hoverBackgroundColor:"rgba(255, 0, 119, 1)",
                //fill: false,
  
            },
            {
                label: nam3, //'This week',
                data: nam3y,//[24, 18, 16, 18, 24, 36,28,
                //borderColor: "#009688",
                borderColor:'white',
                backgroundColor:"rgba(29,132,232,0.7)",
                hoverBackgroundColor:"rgba(72, 0, 255, 1)",
                // fillColor: "rgba(255, 172, 100, 0.1)",
               // backgroundColor: "rgba(155, 102, 200, 0.2)",
                //fill: false,
                // borderColor: 'transparent',
                // pointBackgroundColor: '#FFFFFF',
                // pointBorderColor: '#FFFFFF',
                // lineTension: 0.40,
            },
            {
                label: nam4, //'This week',
                data: nam4y,//[24, 18, 16, 18, 24, 36,28,
                //borderColor: "#805dca",
                borderColor:'white',
                backgroundColor:"rgba(153,51,222,0.7)",
                //backgroundColor: "rgba(155, 150, 210, 0.2)",
                hoverBackgroundColor: "rgba(0, 98, 255, 1)",
                //fill: false,
                // borderColor: 'transparent',
                // pointBackgroundColor: '#FFFFFF',
                // pointBorderColor: '#FFFFFF', rgba(253,187,45,1)
                // lineTension: 0.40,
                // fillColor: "rgba(19, 71, 34, 0.3)",
                // strokeColor: "rgba(88, 188, 116, 1)",
                // pointColor: "rgba(88, 188, 116, 1)",
                // pointStrokeColor: "#202b33",
                // pointHighlightStroke: "rgba(225,225,225,0.9)",
            },
            {
                label: nam5, //'This week',
                data: nam5y,//[24, 18, 16, 18, 24, 36,28,
                //borderColor:"#805dca",
                borderColor:'white',
                backgroundColor:"rgba(250,252,70,0.7)",//" rgba(253,187,45,0.7)", 
               //backgroundColor: "rgba(15, 202, 200, 0.2)",
                hoverBackgroundColor: "rgba(0, 255, 123, 1)",
                //fill: false,
                // borderColor: 'transparent',
                // pointBackgroundColor: '#FFFFFF',
                // pointBorderColor: '#FFFFFF',
                // lineTension: 0.40,
                //borderColor: "rgba(15, 202, 200, 1)",
            },
            {
                label: nam6, //'This week',
                data: nam6y,//[24, 18, 16, 18, 24, 36,28,
                backgroundColor:  " rgba(0,212,255,0.7)",
                hoverBackgroundColor: "rgba(255, 242, 0, 1)",
                //fill: false,
                // borderColor: 'transparent',
                // pointBackgroundColor: '#FFFFFF',
                // pointBorderColor: '#FFFFFF',
                // lineTension: 0.40,
                borderColor:"white",//rgba(105, 102, 200, 1)",
            },
            {
                label: nam7, //'This week',
                data: nam7y,//[24, 18, 16, 18, 24, 36,28,
                backgroundColor:  "rgba(252,70,107,0.7)",
                hoverBackgroundColor: "rgba(25, 242, 0, 1)",
                //fill: false,
                // borderColor: 'transparent',
                // pointBackgroundColor: '#FFFFFF',
                // pointBorderColor: '#FFFFFF',
                // lineTension: 0.40,
                borderColor:"white",//rgba(105, 102, 200, 1)",
            }
            ]
        },
        options: {
                maintainAspectRatio:false,
                responsive: true,
                elements: { 
            //     point: {
            //       radius: 0,
            //       hitRadius: 5, 
            //     hoverRadius: 5 
            //   } 
            },
                legend: {
                    display: true,
            },
            scales: {
                xAxes: [{
                        display: true,
                }],
                yAxes: [{
                        display: true,
                       
                    ticks: {
                        beginAtZero: true,
                      },
                }]
            },
           
        },
        //plugins: [multiply],
    };
    

    mychart = new Chart(canvas,config);
    

   // background: linear-gradient(90deg, rgba(131,58,180,1) 0%, rgba(253,29,29,1) 100%, rgba(252,176,69,1) 100%);


}


/// Test End







async function general_source(val=1,elem){

    var data = await eel.general_sources(val)();
    data = JSON.parse(data);
    x_gen_src= Object.keys(data);
    y_gen_src = Object.values(data);
    //graph(elem,"bar","Sites Visted",x_gen_src,y_gen_src);
    
    if(typeof mychart_gen_src=='undefined'){
        
        var ctx2 = document.getElementById(elem).getContext('2d');//bgsc1=>bar source graph 1
        var purple_orange_gradient = ctx2.createLinearGradient(0, 0, 0, 600);
        purple_orange_gradient.addColorStop(0, 'orange');
        purple_orange_gradient.addColorStop(1, 'purple');
        var mychart_gen_src = new Chart(ctx2, {
            type: "bar",
            data: {

                datasets:[{
                    data : y_gen_src,
                    label: "Sites Visted",
                    backgroundColor: purple_orange_gradient,
                    hoverBackgroundColor: purple_orange_gradient,
                    hoverBorderWidth: 2,
                    hoverBorderColor: 'purple'
                }],
                labels:x_gen_src

            },
            options:{
                maintainAspectRatio:false,
                responsive: true,
            }
        
        });

    }
    else{

        mychart_gen_src.data.datasets[0].label = "Sites Visted";
        mychart_gen_src.data.datasets[0].data=y_gen_src;
        mychart_gen_src.data.labels = x_gen_src;
        mychart_gen_src.update();
    }

    

}


async function source_graph(val=1,req_class=["AI","GameD","WebD","AppD","Entertainment","Social Media","Lang"]){

    var data = await eel.get_sources(val)();
    data = JSON.parse(data);
    var Cls = Object.keys(data);
    //console.log('Class are : ',Cls);
    

    if (val == 1){
        //destroy(["sg1"]);
        //graph("srchead","bar","All Sources",x_gen_src,y_gen_src);
        if(typeof mychart_gen_s!='undefined'){
            //var elem2 = "srchead";//"clasif"+String(i+1);
            mychart_gen_s.data.datasets[0].label = "Sites Visted";
            mychart_gen_s.data.datasets[0].data=y_gen_src;
            mychart_gen_s.data.labels = x_gen_src;
            mychart_gen_s.update();
        }
        else{

            var ctx33 = document.getElementById("srchead").getContext('2d');//bgsc1=>bar source graph 1
            var purple_orange_gradient = ctx33.createLinearGradient(0, 0, 0, 600);
            purple_orange_gradient.addColorStop(0, 'orange');
            purple_orange_gradient.addColorStop(1, 'purple');
            mychart_gen_s = new Chart(ctx33, {
                type: "bar",
                data: {
        
                    datasets:[{
                        data : y_gen_src,
                        label: "Sites Visted",
                        backgroundColor: purple_orange_gradient,
                        hoverBackgroundColor: purple_orange_gradient,
                        hoverBorderWidth: 2,
                        hoverBorderColor: 'purple'
                    }],
                    labels:x_gen_src
        
                },
                options:{
                    maintainAspectRatio:false,
                    responsive: true,
                }
            
            });

        }
        

    }
    else{
        console.log("VAL IS changed");
        data2 = await eel.general_sources(val)();
        data2 = JSON.parse(data2);
        x_gen_src2= Object.keys(data2);
        y_gen_src2 = Object.values(data2);
        mychart_gen_s.data.datasets[0].label = "Sites Visted";
        mychart_gen_s.data.datasets[0].data=y_gen_src2;
        mychart_gen_s.data.labels = x_gen_src2;
        mychart_gen_s.update();
        
    }
    
   
    if(typeof mychart_sour0!='undefined'){
        console.log("IN SRC GRAPH ALREADY EXISTS");
        var inp = [mychart_sour0,mychart_sour1,mychart_sour2,mychart_sour3,mychart_sour4,mychart_sour5,mychart_sour6];
        for (var i = 0; i < req_class.length; i++) {
            cls1 = req_class[i];
            console.log("Out put of CLS is : ",cls1);
            try{
                
                x = Object.keys(data[cls1]);
                y = Object.values(data[cls1]);
                
            }
            catch (error){
                console.log("CATCH : ",error);
                x = 0;
                y = 0;
            }
            var elem = "clasif"+String(i+1);
            inp[i].data.datasets[0].label = cls1;
            inp[i].data.datasets[0].data=y;
            inp[i].data.labels = x;
            inp[i].update();

        }
    }
    else{
        //Con
        console.log("IN SRC GRAPH NO!!! EXISTS");
        for (var i = 0; i < req_class.length; i++) {
            var cls1 = req_class[i];
            //console.log("Out put of CLS is : ",cls);
            try{
                var x = Object.keys(data[cls1]);
                var y = Object.values(data[cls1]);
                
            }
            catch{
                var x = 0;
                var y = 0;
            }
            
            
            var elem = "clasif"+String(i+1);
    
            var ctx22 = document.getElementById(elem).getContext('2d');//bgsc1=>bar source graph 1
            this["mychart_sour"+i] = new Chart(ctx22, {
                type: "bar",
                data: {
    
                    datasets:[{
                        data : y,
                        label:cls1,
                        backgroundColor: purple_orange_gradient,
                        hoverBackgroundColor: purple_orange_gradient,
                        hoverBorderWidth: 2,
                        hoverBorderColor: 'purple'
                    }],
                    labels:x
    
                },
                options:{
                    maintainAspectRatio:false,
                    responsive: true,
                }
            
            });
    
        }

    }
    
    
    

}



async function general_date(gen_date=false){

    var data = await eel.date_graph(val=1,gen_date)();
    data = JSON.parse(data);
    var dates = Object.keys(data);
    var values = Object.values(data);

    if(typeof mybarChart4!='undefined'){
        mybarChart4.destroy();
    }

    var ctx2 = document.getElementById('bar3').getContext('2d');
    var purple_orange_gradient = ctx2.createLinearGradient(0, 0, 0, 600);
    purple_orange_gradient.addColorStop(0, 'orange');
    purple_orange_gradient.addColorStop(1, 'purple');

    mybarChart4 = new Chart(ctx2, {
        type: 'bar',
        data: {

            datasets:[{
                data : values,
                backgroundColor: purple_orange_gradient,
				hoverBackgroundColor: purple_orange_gradient,
                hoverBorderWidth: 2,
                hoverBorderColor: 'purple',
                label:"This Week"
            }],
            labels:dates

        },
        options:{
            maintainAspectRatio:false,
            responsive: true,

            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            },

        }
       
    });

}

function Updatedata(chart, label, data) {
    chart.data.labels = label;
    chart.data.datasets[0].data=data;
    chart.update();
}


async function general_class(val,DEL1){
    
    var dic = await eel.class_percent(val)();

    var names = Object.keys(dic);
    var values = Object.values(dic);
    //alert(dic);
    // PAI CHART

    if(typeof mypaiChart1!='undefined'){
        console.log("Pai hart is to be delated");
        //removeData(mypaiChart1);
        //removeData(mybarChart1);
        Updatedata(mypaiChart1,names,values);
        Updatedata(mybarChart1,names,values);
        //mypaiChart1.destroy();
        //mybarChart1.destroy();
        console.log("Destroyed!");
    }
    else{

        Chart.elements.Rectangle.prototype.draw = function() {
            var ctx = this._chart.ctx;
            var vm = this._view;
            var left, right, top, bottom, signX, signY, borderSkipped, radius;
            var borderWidth = vm.borderWidth;
            var cornerRadius = 20;
        
            if (!vm.horizontal) {
                left = vm.x - vm.width / 2;
                right = vm.x + vm.width / 2;
                top = vm.y;
                bottom = vm.base;
                signX = 1;
                signY = bottom > top? 1: -1;
                borderSkipped = vm.borderSkipped || 'bottom';
            } else {
                left = vm.base;
                right = vm.x;
                top = vm.y - vm.height / 2;
                bottom = vm.y + vm.height / 2;
                signX = right > left? 1: -1;
                signY = 1;
                borderSkipped = vm.borderSkipped || 'left';
            }
        
            if (borderWidth) {
                var barSize = Math.min(Math.abs(left - right), Math.abs(top - bottom));
                borderWidth = borderWidth > barSize? barSize: borderWidth;
                var halfStroke = borderWidth / 2;
                var borderLeft = left + (borderSkipped !== 'left'? halfStroke * signX: 0);
                var borderRight = right + (borderSkipped !== 'right'? -halfStroke * signX: 0);
                var borderTop = top + (borderSkipped !== 'top'? halfStroke * signY: 0);
                var borderBottom = bottom + (borderSkipped !== 'bottom'? -halfStroke * signY: 0);
                if (borderLeft !== borderRight) {
                    top = borderTop;
                    bottom = borderBottom;
                }
                if (borderTop !== borderBottom) {
                    left = borderLeft;
                    right = borderRight;
                }
            }
        
            ctx.beginPath();
            ctx.fillStyle = vm.backgroundColor;
            ctx.strokeStyle = vm.borderColor;
            ctx.lineWidth = borderWidth;
            var corners = [
                [left, bottom],
                [left, top],
                [right, top],
                [right, bottom]
            ];
        
            var borders = ['bottom', 'left', 'top', 'right'];
            var startCorner = borders.indexOf(borderSkipped, 0);
            if (startCorner === -1) {
                startCorner = 0;
            }
        
            function cornerAt(index) {
                return corners[(startCorner + index) % 4];
            }
        
            var corner = cornerAt(0);
            ctx.moveTo(corner[0], corner[1]);
        
            for (var i = 1; i < 4; i++) {
                corner = cornerAt(i);
                nextCornerId = i+1;
                if(nextCornerId == 4){
                    nextCornerId = 0
                }
        
                nextCorner = cornerAt(nextCornerId);
        
                width = corners[2][0] - corners[1][0];
                height = corners[0][1] - corners[1][1];
                x = corners[1][0];
                y = corners[1][1];
                
                var radius = cornerRadius;
                
                if(radius > height/2){
                    radius = height/2;
                }if(radius > width/2){
                    radius = width/2;
                }
        
                ctx.moveTo(x + radius, y);
                ctx.lineTo(x + width - radius, y);
                ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
                ctx.lineTo(x + width, y + height - radius);
                ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
                ctx.lineTo(x + radius, y + height);
                ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
                ctx.lineTo(x, y + radius);
                ctx.quadraticCurveTo(x, y, x + radius, y);
            }
        
            ctx.fill();
            if (borderWidth) {
                ctx.stroke();
            }
        };
        
        // background-color: #4361ee;
        // background: linear-gradient(to left, #0081ff 100%, #0045ff 100%);
        
        // var org = ctx2.createLinearGradient(0, 100, 300, 700);
        // org.addColorStop(0, '#d09693 ');
        // org.addColorStop(1, '#c71d6f');
        Chart.defaults.global.FontFamily="Helvetica";
        Chart.defaults.global.FontSize = 12;

        ctx = document.getElementById('pai1').getContext('2d');
        var blue = ctx.createLinearGradient(0, 100, 300, 700);
        blue.addColorStop(0, '#0081ff');
        blue.addColorStop(1, '#0045ff');

        var org = ctx.createLinearGradient(0, 100, 300, 700);
        org.addColorStop(0, '#d09693 ');
        org.addColorStop(1, '#c71d6f');

        var pink = ctx.createLinearGradient(0, 100, 300, 700);
        pink.addColorStop(0, '#f09819  ');
        pink.addColorStop(1, '#ff5858 ');

        var gren = ctx.createLinearGradient(0, 100, 300, 700);
        gren.addColorStop(0, '#13b497');
        gren.addColorStop(1, '#05737a ');

        var pink2 = ctx.createLinearGradient(0, 100, 300, 700);
        pink2.addColorStop(0, '#ad244b');
        pink2.addColorStop(1, '#d6406b');

        var purple_orange_gradient = ctx.createLinearGradient(0, 0, 0, 600);
        purple_orange_gradient.addColorStop(0, 'orange');
        purple_orange_gradient.addColorStop(1, 'purple');

        var red = ctx.createLinearGradient(0, 100, 300, 700);
        red.addColorStop(0, '#ff0049');
        red.addColorStop(1, '#ff0000');


        

        mypaiChart1 = new Chart(ctx, {
            type: 'pie',
            data: {

                datasets:[{
                    data : values,
                    backgroundColor: [purple_orange_gradient,blue,pink,gren,pink2,org,red],
                    // [
                    //     'rgba(255, 99, 132, 0.2)',
                    //     'rgba(54, 162, 235, 0.2)',
                    //     'rgba(255, 206, 86, 0.2)',
                    //     'rgba(75, 192, 192, 0.2)',
                    //     'rgba(153, 102, 255, 0.2)',
                    //     'rgba(255, 159, 64, 0.2)',
                    //     'rgba(190, 178, 80, 0.2)'
                    // ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(205, 130, 94, 1)'
                    ],
                    hoverBackgroundColor: "red",//[
                        // 'rgba(255, 99, 132, 1)',
                        // 'rgba(54, 162, 235, 1)',
                        // 'rgba(255, 206, 86, 1)',
                        // 'rgba(75, 192, 192, 1)',
                        // 'rgba(153, 102, 255, 1)',
                        // 'rgba(255, 159, 64, 1)',
                        // 'rgba(190, 178, 80, 1)'
                    //]
                }],
                labels:names

            },
            options:{
                maintainAspectRatio:false,
                responsive: true,
            }
        
        });
        
        // BAR CHART
        ctx2 = document.getElementById('bar1').getContext('2d');
        Chart.defaults.global.defaultFontColor = "white";
        mybarChart1 = new Chart(ctx2, {
            type: 'horizontalBar',
            data: {

                datasets:[{
                    label:"Total Activity",
                    data : values,
                    backgroundColor:blue ,// [
                        // 'rgba(255, 99, 132, 0.2)',
                        // 'rgba(54, 162, 235, 0.2)',
                        // 'rgba(255, 206, 86, 0.2)',
                        // 'rgba(75, 192, 192, 0.2)',
                        // 'rgba(153, 102, 255, 0.2)',
                        // 'rgba(255, 159, 64, 0.2)',
                        // 'rgba(190, 178, 80, 0.2)'
                    //     'rgba(255, 99, 132, 1)',
                    //     'rgba(54, 162, 235, 1)',
                    //     'rgba(255, 206, 86, 1)',
                    //     'rgba(75, 192, 192, 1)',
                    //     'rgba(153, 102, 255, 1)',
                    //     'rgba(255, 159, 64, 1)',
                    //     'rgba(190, 178, 80, 1)'
                    // ],
                    // borderColor: [
                    //     'rgba(255, 99, 132, 1)',
                    //     'rgba(54, 162, 235, 1)',
                    //     'rgba(255, 206, 86, 1)',
                    //     'rgba(75, 192, 192, 1)',
                    //     'rgba(153, 102, 255, 1)',
                    //     'rgba(255, 159, 64, 1)',
                    //     'rgba(205, 130, 94, 1)'
                        

                    // ],
                    hoverBackgroundColor:[
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(190, 178, 80, 1)'
                    ]
                }],
                labels:names

            },
            options:{
                maintainAspectRatio:false,
                responsive: true,

                legend: {
                    labels: {
                        fontColor: 'white'
                    }

            
                }
            }
       
        });

    }


    
    


}




comp = true; // tisi is form time graph
async function general_time(val2,del=false){
    
        // 1. Create a detail page 
        // 2. info card
        // 3. am,pm,now - to be markes on x-axis
        //console.log("After and Bef upd 11 ");
    dic22 = await eel.time_graph(val2)();
    //console.log("Time obj : ",dic2);
    //console.log("After and Bef upd 22 : ",dic2);

    dic22 = JSON.parse(dic22);
    DATES = Object.keys(dic22);
    Today = dic22[DATES[0]];
    today_x = Object.keys(Today);
    today_y = Object.values(Today);
    Yesterday = dic22[DATES[1]];
    yest_x = Object.keys(Yesterday);
    yest_y = Object.values(Yesterday);
    
    console.log("X DATES\n",DATES);
    // console.log("y",today_y);
    // console.log("X",yest_x);
    // console.log("y",yest_y)
    

    // if (del==true){
    //     mybarChart3.destroy();
    // }
    
    if (comp == true){
        comp= false;
    }
    else{
        comp=true;
    }
    
    

    if(typeof mybarChart3=='undefined'){

        var ctx2 = document.getElementById('bar2');//.getContext('2d');

        var multiply = {
            beforeDatasetsDraw: function(chart, options, el) {
            chart.ctx.globalCompositeOperation = 'multiply';
            },
            afterDatasetsDraw: function(chart, options) {
            chart.ctx.globalCompositeOperation = 'source-over';
            },
        };

        var grad1 = ctx2.getContext('2d').createLinearGradient(0, 0, 0, 150);
        grad1.addColorStop(0, '#5555FF');
        grad1.addColorStop(1, '#9787FF');

        // Gradient color - previous week
        var grad2 = ctx2.getContext('2d').createLinearGradient(0, 0, 0, 150);
        grad2.addColorStop(0, '#FF55B8');
        grad2.addColorStop(1, '#FF8787');


        mybarChart3 = new Chart(ctx2, {
            type: 'line',
            data: {
                labels:yest_x,//today_x,
                datasets:[{
                    label:DATES[0],
                    data : today_y,
                    backgroundColor: grad1,
                    pointBackgroundColor: '#FFFFFF',
                    pointBorderColor: '#FFFFFF',
                    lineTension: 0.40,
                },
                {
                    label:DATES[1],
                    data : yest_y,
                    backgroundColor: grad2,
                    pointBackgroundColor: '#FFFFFF',
                    pointBorderColor: '#FFFFFF',
                    lineTension: 0.40,
                }
                
                ],
            },
            options:{
                maintainAspectRatio:false,
                responsive: true,
            },
            plugins: [multiply],

        });

        mybarChart3.data.datasets[1].data=[];
        mybarChart3.update();

    }
    else{
        
        if (comp==true){

            mybarChart3.data.datasets[1].data=yest_y;
            //mybarChart3.data.labels = today_x;
            mybarChart3.data.labels = yest_x;
            mybarChart3.data.datasets[0].label=DATES[0];
            mybarChart3.data.datasets[1].label=DATES[1];
            mybarChart3.update();
            
        }
        else{
            mybarChart3.data.datasets[1].data=[];
            mybarChart3.data.datasets[0].data=today_y;
            mybarChart3.data.datasets[0].label=DATES[0];
            mybarChart3.data.datasets[1].label=DATES[1];
            mybarChart3.data.labels = today_x;
            mybarChart3.update();
        }

    }


    

        

    

}


window.onload = function() {
    
    //document.getElementById("below").style.display="none";
    
    var myVar = setTimeout(start, 2000);
    
    
};

function start(){
   
    document.getElementById("loader").style.display="none";
    //document.getElementById("below").style.display="block";
    CheckUpdate();
    general();
    
}



// window.onbeforeunload = function(){
//     //eel.End()();
// };


/*!
    * Start Bootstrap - Freelancer v6.0.5 (https://startbootstrap.com/theme/freelancer)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-freelancer/blob/master/LICENSE)
    */
(function($) {
    "use strict"; // Start of use strict
  
    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
      if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        if (target.length) {
          $('html, body').animate({
            scrollTop: (target.offset().top - 71)
          }, 1000, "easeInOutExpo");
          return false;
        }
      }
    });
  
    // Scroll to top button appear
    $(document).scroll(function() {
      var scrollDistance = $(this).scrollTop();
      if (scrollDistance > 100) {
        $('.scroll-to-top').fadeIn();
      } else {
        $('.scroll-to-top').fadeOut();
      }
    });
  
    // Closes responsive menu when a scroll trigger link is clicked
    $('.js-scroll-trigger').click(function() {
      $('.navbar-collapse').collapse('hide');
    });
  
    // Activate scrollspy to add active class to navbar items on scroll
    $('body').scrollspy({
      target: '#mainNav',
      offset: 80
    });
  
    // Collapse Navbar
    var navbarCollapse = function() {
      if ($("#mainNav").offset().top > 100) {
        $("#mainNav").addClass("navbar-shrink");
      } else {
        $("#mainNav").removeClass("navbar-shrink");
      }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);
  
    // Floating label headings for the contact form
    $(function() {
      $("body").on("input propertychange", ".floating-label-form-group", function(e) {
        $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
      }).on("focus", ".floating-label-form-group", function() {
        $(this).addClass("floating-label-form-group-with-focus");
      }).on("blur", ".floating-label-form-group", function() {
        $(this).removeClass("floating-label-form-group-with-focus");
      });
    });
  
  })(jQuery); // End of use strict
  