d1  = [];
l   = 0; // The letter 'L' - NOT a one

// Pre-pad the arrays with 250 null values
for (var i=0; i<1000; ++i) {
    d1.push(null);
}

function getGraph(id, d1)
{
    // After creating the chart, store it on the global window object
    if (!window.__rgraph_line__) {
        window.__rgraph_line__ = new RGraph.Line(id, d1);
        window.__rgraph_line__.set('xticks', 100);
        window.__rgraph_line__.set('background.barcolor1', 'white');
        window.__rgraph_line__.set('background.barcolor2', 'white');
        window.__rgraph_line__.set('title.xaxis', 'Time >>>');
        window.__rgraph_line__.set('title.yaxis', 'Bandwidth (MB/s)');
        window.__rgraph_line__.set('title.vpos', 0.5);
        window.__rgraph_line__.set('title', 'Bandwidth used');
        window.__rgraph_line__.set('title.yaxis.pos', 0.5);
        window.__rgraph_line__.set('title.xaxis.pos', 0.5);
        window.__rgraph_line__.set('colors', ['black']);
        window.__rgraph_line__.set('linewidth',0.5);
        //obj.set('ylabels.inside', true);
        window.__rgraph_line__.set('yaxispos', 'right');
        window.__rgraph_line__.set('ymax', 50);
        window.__rgraph_line__.set('xticks', 25);
        window.__rgraph_line__.set('filled', true);
        
        var grad = window.__rgraph_line__.context.createLinearGradient(0,0,0,250);
        grad.addColorStop(0, '#efefef');
        grad.addColorStop(0.9, 'rgba(0,0,0,0)');

        window.__rgraph_line__.set('fillstyle', [grad]);
    }

    return window.__rgraph_line__;
}

function drawGraph ()
{
    document.getElementById("num_updates").innerHTML = parseInt(document.getElementById("num_updates").innerHTML) + 1;

    RGraph.clear(document.getElementById("mem-stat"));
    RGraph.clear(document.getElementById("http-stat"));
    
    var graph_mem = getGraph('mem-stat', d1);
    var graph_http = getGraph('http-stat', d1);
    graph_mem.draw();
    graph_http.draw();

    $.ajax({
        url: "http://127.0.0.1:8888/serverstat/",
        dataType: "json",
        success: function(response){
            mem_stat = response["mem_stat"];
            http_stat = response["http_stat"];

            for (i in mem_stat){
                stat = mem_stat[i];
                usage = (stat[0] - stat[1])/(stat[0]+0.0) * 50;
                d1.push(usage);
            }

             // Add some data to the data arrays
             // var r1 = RGraph.random(
             //                        RGraph.is_null(d1[d1.length - 1]) ? 26 : d1[d1.length - 1] - 2,
             //                        RGraph.is_null(d1[d1.length - 1]) ? 24 : d1[d1.length - 1] + 2
             //                       );
            // r1 = Math.max(r1, 0);
            // r1 = Math.min(r1, 50);

            //  d1.push(r1);
             
             if (d1.length > 250) {
                 d1 = RGraph.array_shift(d1);
             }

             if (document.all && RGraph.ISIE8) {
                 alert('[MSIE] Sorry, Internet Explorer 8 is not fast enough to support animated charts');
             } else {
                 window.__rgraph_line__.original_data[0] = d1;
                 setTimeout(drawGraph, 1000);
             }
        }
    });
    
}

drawGraph();
