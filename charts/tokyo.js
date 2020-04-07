// 2) CSVから２次元配列に変換
function csv2Array(str) {
  var csvData = [];
  var lines = str.split("\n");
  for (var i = 0; i < lines.length; ++i) {
    var cells = lines[i].split(",");
    csvData.push(cells);
  }
  return csvData;
}

function drawLineChart(data) {
  // 3)chart.jsのdataset用の配列を用意
  var Labels = [], cumsum = [], logcumsum = [], rolling = [], logrolling = [];
  for (var row in data) {
    Labels.push(data[row][0])
    cumsum.push(data[row][1])
    logcumsum.push(data[row][2])
    rolling.push(data[row][3])
    logrolling.push(data[row][4])
  };

  // 4)chart.jsで描画
  var ctx = document.getElementById("myChart").getContext("2d");
  var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: logcumsum,
      datasets: [
        {
          label: '東京都',
          data: logrolling,
          borderColor: "rgba(255,0,0,1)",
          backgroundColor: "rgba(0,0,0,0)"
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: '総患者数'
      },
	scales: {
        xAxes: [{
          ticks: {
            // suggestedMax: 40,
            // suggestedMin: 0,
            stepSize: 1,
            callback: function(value, index, values){
              return  'log10(' + value +  ')人'
            }
          }
        }],
        yAxes: [{
          ticks: {
            // suggestedMax: 40,
            // suggestedMin: 0,
            stepSize: 1,
            callback: function(value, index, values){
              return  'log10(' + value +  ')人'
            }
          }
        }]
      },
    }
  });
}

function main() {
  // 1) ajaxでCSVファイルをロード
  var req = new XMLHttpRequest();
  //var filePath = './csv/COVID-192020-04-07-073007/東京都.csv';
  var filePath = 'https://koh-t.github.io/charts/csv/COVID-192020-04-07-073007/東京都.csv';
  req.open("GET", filePath, true);
  req.onload = function() {
    // 2) CSVデータ変換の呼び出し
    data = csv2Array(req.responseText);
    // 3) chart.jsデータ準備、4) chart.js描画の呼び出し
    drawLineChart(data);
    // drawBarChart(data);
  }
  req.send(null);
}

main();
