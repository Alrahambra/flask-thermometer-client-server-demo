function make_plot() {
    var json_obj;
    var time_data;
    var hum_data;
    var temp_data;
    var url_path;


    $.ajax({
        url: window.location.href + 'api/records',
        async: false,
        dataType: 'json',
        success: function (response) {
            json_obj = response;
        }
    });


    hum_data = json_obj.hum_data
    time_data = json_obj.time_data
    temp_data = json_obj.temp_data

    var temperature = {
        x: time_data,
        y: temp_data,
        name: 'Temperature data',
        type: 'scatter'
    };

    var humidity = {
        x: time_data,
        y: hum_data,
        name: 'Humidity data',
        yaxis: 'y2',
        type: 'scatter',
        color: 'blue'
    };

    var data = [temperature, humidity];

    var layout = {
        title: 'Temperature vs. Humidity',
        yaxis: {
            title: 'Temperature',
            titlefont: {
                color: 'blue',
                tickfont: {
                    color: 'blue'
                }
            }
        },

        yaxis2: {
            title: 'Humidity',
            titlefont: {
                color: 'orange'
            },
            tickfont: {
                color: 'orange'
            },
            overlaying: 'y',
            side: 'right'
        }
    };

    Plotly.newPlot('datawindow', data, layout);
}

make_plot();