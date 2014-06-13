window.onload = function () {

      var dps_mem = [];   //dataPoints.
      var dps_404 = [];
      var dps_500 = [];

      var chart_mem = new CanvasJS.Chart("chart-mem",{
        title :{
            text: "Memory Usage"
        },
        axisX: {                        
            title: "Axis X Title"
        },
        axisY: {                        
            title: "Memory Used"
        },
        data: [{
            type: "line",
            dataPoints : dps_mem
        }]
      });

      var chart_404 = new CanvasJS.Chart("chart-404",{
        title :{
            text: "HTTP 404"
        },
        axisX: {                        
            title: "Axis X Title"
        },
        axisY: {                        
            title: "Response"
        },
        data: [{
            type: "line",
            dataPoints : dps_404
        }]
      });

      var chart_500 = new CanvasJS.Chart("chart-500",{
        title :{
            text: "HTTP 500"
        },
        axisX: {                        
            title: "Axis X Title"
        },
        axisY: {                        
            title: "Response"
        },
        data: [{
            type: "line",
            dataPoints : dps_500
        }]
      });

      chart_mem.render();
      chart_404.render();
      chart_500.render();
      var xVal_mem = dps_mem.length + 1;
      var xVal_404 = dps_404.length + 1;
      var xVal_500 = dps_500.length + 1;
      var updateInterval = 500;

      var updateChart = function () {

        $.ajax({
            url: "http://127.0.0.1:8888/serverstat/",
            dataType: "json",
            success: function(response){
                mem_stat = response["mem_stat"];
                http_stat = response["http_stat"];

                stat = mem_stat[mem_stat.length - 1];
                usage = (stat[0] - stat[1])/(stat[0]+0.0);
                dps_mem.push({x: xVal_mem, y: usage});

                stat = http_stat[http_stat.length - 1];
                res_404 = stat[404];
                dps_404.push({x: xVal_404, y: res_404});

                stat = http_stat[http_stat.length - 1];
                res_500 = stat[500];
                dps_500.push({x: xVal_500, y: res_404});

                xVal_mem++;
                xVal_404++;
                xVal_500++;

                if (dps_mem.length >  10 )
                {
                    dps_mem.shift();
                }
                if (dps_404.length >  10 )
                {
                    dps_404.shift();
                }
                if (dps_500.length >  10 )
                {
                    dps_500.shift();
                }

                chart_mem.render();
                chart_404.render();
                chart_500.render();
                setTimeout(updateChart, updateInterval);
            }
        });
      };
    updateChart();
}
