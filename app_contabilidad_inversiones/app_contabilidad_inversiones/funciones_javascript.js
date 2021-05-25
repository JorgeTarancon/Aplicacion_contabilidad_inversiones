function show_chart(chart_type,id_canvas,titulo,labels_chart,label_chart,data) {
    var ctx = document.getElementById(id_canvas).getContext('2d');
    var myChart = new Chart(ctx, {
        type: chart_type,
        data: {
            labels: labels_chart,
            datasets: [{
                label: label_chart,
                data: data,
                backgroundColor:"rgb(100,200,100)",
                borderColor:"rgb(100,160,100)",
                hoverBackgroundColor:"rgb(100,250,100)"
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: titulo,
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                }
            }
        }
    });   
}


function show_mixed_charts(id_canvas,titulo,labels_chart,chart_type1,label_chart1,data1,chart_type2,label_chart2,data2) {
    var ctx = document.getElementById(id_canvas).getContext('2d');
    var myChart = new Chart(ctx, {
        data: {
            datasets: [{
                type: chart_type1,
                label: label_chart1,
                data: data1,
                backgroundColor:"rgb(100,200,100)",
                borderColor:"rgb(100,160,100)",
                hoverBackgroundColor:"rgb(100,250,100)"
            }, {
                type: chart_type2,
                label: label_chart2,
                data: data2,
                backgroundColor:"rgb(200,100,100)",
                borderColor:"rgb(160,100,100)",
                hoverBackgroundColor:"rgb(250,100,100)"
            }],
            labels: labels_chart,
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: true
                },
                title: {
                    display: true,
                    text: titulo,
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                }
            }
        }
    });   
}