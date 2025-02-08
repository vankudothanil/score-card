document.addEventListener("DOMContentLoaded", function () {
    // Initialize Plotly charts
    const data = JSON.parse(document.getElementById('chart-data').textContent);
    const employees = data.Employee;
    const scores = data.Score;

    // Bar Chart
    const barChartData = [
        {
            x: employees,
            y: scores,
            type: 'bar',
            marker: { color: 'blue' }
        }
    ];
    const barChartLayout = {
        title: 'Employee Scores',
        xaxis: { title: 'Employee' },
        yaxis: { title: 'Score' }
    };
    Plotly.newPlot('bar-chart', barChartData, barChartLayout);

    // Pie Chart
    const pieChartData = [
        {
            labels: employees,
            values: scores,
            type: 'pie'
        }
    ];
    const pieChartLayout = {
        title: 'Score Distribution'
    };
    Plotly.newPlot('pie-chart', pieChartData, pieChartLayout);

    // Radar Chart
    const radarChartData = [
        {
            type: 'scatterpolar',
            r: scores,
            theta: employees,
            fill: 'toself'
        }
    ];
    const radarChartLayout = {
        polar: {
            radialaxis: {
                visible: true,
                range: [0, 100]
            }
        },
        title: 'Employee Performance Radar Chart'
    };
    Plotly.newPlot('radar-chart', radarChartData, radarChartLayout);
});