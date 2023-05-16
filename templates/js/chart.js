// 準備畫圖的資料
var ws = new WebSocket("wss://poll-fastapi-demo/sendVote");
var Chart;

function setChart(vote_cnt){
    
    var ctx = document.getElementById("VoteChart").getContext('2d'); 
    var chartData = 
{
    type: 'bar',
    data: {
        labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        datasets: [{
            label: '# of Votes',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
}
    var myChart = new Chart(ctx, chartData);
    myChart.data.datasets[0].data = vote_cnt;
    console.log(vote_cnt);
    myChart.update();
    Chart = myChart;
}


function Votselect(voteTo) {
    // labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
    sendMessage(voteTo);
    // idx = labels.indexOf(voteTo);
    // Chart.data.datasets[0].data[idx] += 1;
    // Chart.update();
    
}

// send message to backend (python)
function sendMessage(value) {
    ws.send(value);
    event.preventDefault;
}

ws.onmessage = function(event){
    var vote_now = JSON.parse(event.data);
    console.log(vote_now);
    Chart.data.datasets[0].data = vote_now;
    Chart.update();
}

function VotReset(){
    ws.send("Reset");
    event.preventDefault;
}
