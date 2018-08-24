var ctx = $("#mycanvas")
var ctx2 = $("#mycanvas2");
var ctx3 = $("#mycanvas3");
var LineGraph =null;
var LineGraph2 =null;
var LineGraph3 =null;

var GetChartData = function () {
    $.ajax({
        url : "./data.php",
        type : "GET",
        success : function(data){
            var temps = [];
            var humidity_sensor1 = [];
            var humidity_sensor2 = [];
            var humidity_setpoint = [];
            var temperature_sensor1 = [];
            var temperature_sensor2 = [];
            var temperature_air = [];
            var humidity_air = [];  
            var speedm =[]; 
            var temperature_grainM = [];

            for(var i in data) {
                humidity_sensor1.push({x:data[i].Time,y:parseFloat(data[i].Ms1)});
                humidity_sensor2.push({x:data[i].Time,y:parseFloat(data[i].Ms2)});
                humidity_setpoint.push({x:data[i].Time,y:parseFloat(data[i].Sm)});
                temperature_sensor1.push({x:data[i].Time,y:parseFloat(data[i].Ts1)});
                temperature_sensor2.push({x:data[i].Time,y:parseFloat(data[i].Ts2)});
                temperature_air.push({x:data[i].Time,y:parseFloat(data[i].TAir)});
                temperature_grainM.push({x:data[i].Time,y:parseFloat(data[i].TGrain)});
                humidity_air.push({x:data[i].Time,y:parseFloat(data[i].HuAir)});
                speedm.push({x:data[i].Time,y:parseFloat(data[i].speedM)});
                
            }
            
            var chartdata = 
                {
                    
                datasets: [{
                    yAxisID:'H',
                    label: "Entry",
                    data: humidity_sensor1,
                    fill: false,
                    lineTension: 0.3,
                    radius:0,
                    backgroundColor: "rgba(57, 106, 177, 0.75)",
                    borderColor: "rgba(57, 106, 177, 1)",
                    pointHoverBackgroundColor: "rgba(57, 106, 177, 0.75)",
                    pointHoverBorderColor: "rgba(57, 106, 177, 1)"},
                    
                    {
                    yAxisID:'H',
                    label: "Exit",
                    data: humidity_sensor2,
                    fill: false,
                    lineTension: 0.3,
                    radius:0,
                    backgroundColor: "rgba(218,124,48, 0.75)",
                    borderColor: "rgba(218,124,48, 1)",
                    pointHoverBackgroundColor: "rgba(218,124,48, 0.75)",
                    pointHoverBorderColor: "rgba(218,124,48, 1)"},
                    
                    {
                    yAxisID:'H',
                    label: "Setpoint",
                    data: humidity_setpoint,
                    fill: false,
                    lineTension: 0.3,
                    radius:0,
                    backgroundColor: "rgba(62,150,81, 0.75)",
                    borderColor: "rgba(62,150,81, 1)",
                    pointHoverBackgroundColor: "rgba(62,150,81, 0.75)",
                    pointHoverBorderColor: "rgba(62,150,81, 1)"},
                    
                    {
                    yAxisID:'M',
                    label: "Motor Frequency",
                    data: speedm,
                    fill: false,
                    lineTension: 0.3,
                    radius:0,
                    backgroundColor: "rgba(204,37,41, 0.75)",
                    borderColor: "rgba(204,37,41, 1)",
                    pointHoverBackgroundColor: "rgba(204,37,41, 0.75)",
                    pointHoverBorderColor: "rgba(204,37,41, 1)"}
                ]
            }
            var chartdata2 = 
                {
                datasets: [{
                    label: "Entry",
                    data: temperature_sensor1,
                    fill: false,
                    lineTension: 0.3,
                    radius:0,
                    backgroundColor: "rgba(57, 106, 177, 0.75)",
                    borderColor: "rgba(57, 106, 177, 1)",
                    pointHoverBackgroundColor: "rgba(57, 106, 177, 0.75)",
                    pointHoverBorderColor: "rgba(57, 106, 177, 1)"
                    },
                    {
                    label: "Middle",
                    data: temperature_grainM, 
                    fill: false,
                    lineTension: 0.3,
                    radius:0,
                    backgroundColor: "rgba(62,150,81, 0.75)",
                    borderColor: "rgba(62,150,81, 1)",
                    pointHoverBackgroundColor: "rgba(62,150,81, 0.75)",
                    pointHoverBorderColor: "rgba(62,150,81, 1)"
                    },
                    {
                    label: "Exit",
                    data: temperature_sensor2, 
                    fill: false,
                    lineTension: 0.3,
                    radius:0,
                    backgroundColor: "rgba(218,124,48, 0.75)",
                    borderColor: "rgba(218,124,48, 1)",
                    pointHoverBackgroundColor: "rgba(218,124,48, 0.75)",
                    pointHoverBorderColor: "rgba(218,124,48, 1)"
                    }
                    ]
            }
            
            
            var chartdata3 = 
                {
                datasets: [{
                    label: "Temp Air",
                    yAxisID:'T',
                    data: temperature_air,
                    fill: false,
                    lineTension: 0.3,              
                    radius:0,
                    backgroundColor: "rgba(218,124,48, 0.75)",
                    borderColor: "rgba(218,124,48, 1)",
                    pointHoverBackgroundColor: "rgba(218,124,48, 0.75)",
                    pointHoverBorderColor: "rgba(218,124,48, 1)"
                    },
                    {label: "Humidity Air",
                    yAxisID:'H',
                    data: humidity_air,
                    fill: false,
                    lineTension: 0.3,                 
                    radius:0,
                    backgroundColor: "rgba(57, 106, 177, 0.75)",
                    borderColor: "rgba(57, 106, 177, 1)",
                    pointHoverBackgroundColor: "rgba(57, 106, 177, 0.75)",
                    pointHoverBorderColor: "rgba(57, 106, 177, 1)"
                }]
            }


        var config = {
            type: 'line',
            data: chartdata,
            HitRadius: 20,
            options: {
                animation: false,
                responsive: true,
                tooltips: {
                    intersect: false,
                    position: 'average',
                    mode: 'index'
                },
                title:{
                    display:true,
                    text:"Seed Humidity"
                },
                scales: {
                    xAxes: [{
                        type: "time",
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Date'
                        }
                    }],
                    yAxes: [{
                        id:'H',
                        type:'linear',
                        position:'right',
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Humidity'
                        }
                    },
                    {
                        id:'M',
                        type:'linear',
                        position:'right',
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Herz'
                        
                        }
                    }]
                }
            }
        };
        
                var config2 = {
            type: 'line',
            data: chartdata2,
            HitRadius: 20,
            options: {
                animation: false,
                responsive: true,
                point: {radius:0},
                tooltips: {
                
                    intersect: false,
                    position: 'average',
                    mode: 'index'
                },
                title:{
                    display:true,
                    text:"Seed Temperature"
                },
                scales: {
                    xAxes: [{
                        type: "time",
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Date'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        position:'right',
                        scaleLabel: {
                            display: true,
                            labelString: 'Temperature'
                        }
                    }]
                }
            }
        };
                        
        var config3= {
            type: 'line',
            data: chartdata3,
            pointHitRadius: 20,
            options: {
                animation: false,
                responsive: true,
                point: {radius:0},
                tooltips: {
                    
                    intersect: false,
                    position: 'average',
                    mode: 'index'
                    //mode: 'nearest'
                },
                title:{
                    display:true,
                    text:"Air Data"
                },
                scales: {
                    xAxes: [{
                        type: "time",
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Date'
                        }
                    }],
                    yAxes: [{
                        id:'H',
                        type:'linear',
                        position:'right',
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Humidity (%)'
                        }
                    },
                    {
                        id:'T',
                        type:'linear',
                        position:'right',
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Temperature (°C)'
                        
                        }
                    }
                    
                    ]
                }
            }
        };
            
        
        if (LineGraph!==null){
            console.log("updating");
            LineGraph.data.datasets=chartdata.datasets;
            LineGraph.update();
            } 
                else {
                    console.log("creating new chart");
                    LineGraph = new Chart(ctx,config);
                    }
        if (LineGraph2!==null){
            LineGraph2.data.datasets=chartdata2.datasets;
            LineGraph2.update();
            } 
                else {LineGraph2 = new Chart(ctx2,config2);
                    }
        if (LineGraph3!==null){
            LineGraph3.data.datasets=chartdata3.datasets;
            LineGraph3.update();
            }
                else {LineGraph3 = new Chart(ctx3, config3);
                    }
        },
        error : function(data) {

        }
    });
}


var refreshgraph = function () {
    GetChartData();
    }
    
$(document).ready(function(){
    GetChartData();
});



