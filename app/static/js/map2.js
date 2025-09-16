

    //   call back
      $("#app path").on("click", function(){
         var location = $(this).attr('data-name-zh')
         $('#city2').text(location);
         $('#city3').text($("[name='radio-group1']:checked").val());
         $('#city4').text($("[name='radio-group2']:checked").val());
         $('#city5').text($("#sq").val() + '坪');

         $.getJSON({ url: "/buy_or_rent/cb", 
               data: { 'city':  $(this).attr('data-name-zh'),
                       'type': $("[name='radio-group1']:checked").val(),
                       'duration': $("[name='radio-group2']:checked").val(),
                       'sq': $("#sq").val()
                               
               }, success: function (data) {
           
                $('#total_price').text(data.total_price),
                $('#First_payment').text(data.First_payment),
                $('#loan_payment').text(data.loan_payment),
                $('#rent_payment').text(data.rent_payment);

                // 更新圖表
                updateCharts(location, $("[name='radio-group1']:checked").val(),
                           $("[name='radio-group2']:checked").val(), $("#sq").val());
                
                   }
                });


      });


      // CB 
      $("#send").bind('click' , function() {

         $('#city3').text($("[name='radio-group1']:checked").val());
         $('#city4').text($("[name='radio-group2']:checked").val());
         $('#city4').text($("[name='radio-group2']:checked").val());  
         $('#city5').text($("#sq").val() + '坪');   

         $.getJSON({ url: "/buy_or_rent/cb", 
                 data: { 'city': $('#city2').text(),
                         'type': $("[name='radio-group1']:checked").val(),
                         'duration': $("[name='radio-group2']:checked").val(),
                         'sq': $("#sq").val()
                                 
                 }, success: function (data) {
             
                  $('#total_price').text(data.total_price),
                  $('#First_payment').text(data.First_payment),
                  $('#loan_payment').text(data.loan_payment),
                  $('#rent_payment').text(data.rent_payment);

                  // 更新圖表
                  updateCharts($('#city2').text(), $("[name='radio-group1']:checked").val(),
                             $("[name='radio-group2']:checked").val(), $("#sq").val());

                     }
                  });
        
               });






     $('#app path').mouseover(function(){ 
        var location = $(this).attr('data-name-zh')
        $('#city').text(location);

     });



      // //  heatmap
      // var myColor = d3.scaleLinear() 
      // .range(["white", "#69b3a2"])
      // .domain([1,100]);

      $(function(color) {
         var place_data = {

                 "臺北市" : 711794,
                 "新北市" : 390532,
                 "臺中市" :271460,
                 "臺南市" :204627,
                 "高雄市" :222842,
                 "基隆市" :198598,
                 "桃園市" :240365,
                 "新竹市" :296769,
                 "新竹縣" :301453,
                 "苗栗縣" :167162,
                 "彰化縣" :281950,
                 "南投縣" :185268,
                 "雲林縣" :148579,
                 "嘉義市" :178202,
                 "嘉義縣" :141352,
                 "屏東縣" :155229,
                 "宜蘭縣" :222606,
                 "花蓮縣" :199118,
                 "臺東縣" :186518,
                 "澎湖縣" :145879,
                 "金門縣" :189098,

         };


         var myColor = d3.scaleLinear() 
         .range(['#cee699', '#ff0000'])
         .domain([140000,450000]);

         $("#app path").each(function(){

            var city = $(this).attr('data-name-zh')

            if (city){
               var value = place_data[city] ;
            }else{
               var value = 100000 ; 
            };
      
            $(this).css("fill" , myColor(value))

            }
         );         

         // $("#app path").css("fill" , myColor(1));
      });

// 更新圖表的函數
function updateCharts(city, type, duration, sq) {
    // 獲取收入、消費、投資報酬率的值
    const income = $('#income-input').val() || '60000';
    const consume = $('#consume-input').val() || '30000';
    const investRate = $('#Range_bar').val() / 100 || 0.05;

    $.getJSON({
        url: "/buy_or_rent/charts",
        data: {
            'city': city,
            'type': type,
            'duration': duration,
            'sq': sq,
            'income': income,
            'consume': consume,
            'invest_rate': investRate
        },
        success: function(data) {
            if (data.error) {
                if (data.error === 'validation_failed') {
                    // 只在圓餅圖區域顯示驗證失敗訊息
                    document.getElementById('pie-chart').innerHTML =
                        '<div style="display: flex; align-items: center; justify-content: center; height: 350px; font-size: 24px; font-weight: bold; color: #dc3545; text-align: center;">' +
                        data.message + '</div>';
                    // 清空折線圖區域
                    document.getElementById('line-chart').innerHTML = '';
                } else {
                    console.error('圖表更新錯誤:', data.error);
                }
                return;
            }

            // 更新圓餅圖 - 先清空容器確保移除任何錯誤訊息
            const pieContainer = document.getElementById('pie-chart');
            pieContainer.innerHTML = '';
            const pieWidth = pieContainer.offsetWidth;
            const pieHeight = 350;

            const pieConfig = {
                responsive: true,
                displayModeBar: false,
                staticPlot: false
            };
            Plotly.newPlot('pie-chart', data.pie_chart.data,
                Object.assign({}, data.pie_chart.layout, {
                    width: pieWidth,
                    height: pieHeight,
                    autosize: false,
                    margin: {l: 40, r: 10, t: 30, b: 10}
                }), pieConfig);

            // 更新折線圖 - 先清空容器確保移除任何錯誤訊息
            const lineContainer = document.getElementById('line-chart');
            lineContainer.innerHTML = '';
            const lineWidth = lineContainer.offsetWidth;
            const lineHeight = 350;

            const lineConfig = {
                responsive: true,
                displayModeBar: false,
                staticPlot: false
            };
            Plotly.newPlot('line-chart', data.line_chart.data,
                Object.assign({}, data.line_chart.layout, {
                    width: lineWidth,
                    height: lineHeight,
                    autosize: false,
                    margin: {l: 40, r: 10, t: 30, b: 40}
                }), lineConfig);
        },
        error: function(xhr, status, error) {
            // 檢查是否是驗證失敗
            if (xhr.responseJSON && xhr.responseJSON.error === 'validation_failed') {
                // 只在圓餅圖區域顯示驗證失敗訊息
                document.getElementById('pie-chart').innerHTML =
                    '<div style="display: flex; align-items: center; justify-content: center; height: 350px; font-size: 24px; font-weight: bold; color: #dc3545; text-align: center;">' +
                    xhr.responseJSON.message + '</div>';
                // 清空折線圖區域
                document.getElementById('line-chart').innerHTML = '';
            } else {
                console.error('AJAX 錯誤:', error);
            }
        }
    });
}

// 頁面載入時初始化圖表
$(document).ready(function() {
    // 使用收入足夠的初始組合，避免顯示錯誤訊息
    updateCharts('雲林縣', '透天厝', '三十年以上', '30');

    // 監聽輸入變化
    $('#income-input, #consume-input').on('input', function() {
        if ($('#city2').text() !== '-') {
            updateCharts($('#city2').text(), $("[name='radio-group1']:checked").val(),
                       $("[name='radio-group2']:checked").val(), $("#sq").val());
        }
    });

    // 監聽投資報酬率滑桿變化
    $('#Range_bar').on('input', function() {
        if ($('#city2').text() !== '-') {
            updateCharts($('#city2').text(), $("[name='radio-group1']:checked").val(),
                       $("[name='radio-group2']:checked").val(), $("#sq").val());
        }
    });

    // 監聽窗口大小變化，調整圖表大小
    $(window).resize(function() {
        if (document.getElementById('pie-chart') && document.getElementById('line-chart')) {
            setTimeout(function() {
                const pieContainer = document.getElementById('pie-chart');
                const lineContainer = document.getElementById('line-chart');

                if (pieContainer && lineContainer) {
                    const pieWidth = pieContainer.offsetWidth;
                    const lineWidth = lineContainer.offsetWidth;

                    Plotly.relayout('pie-chart', {
                        width: pieWidth,
                        height: 350
                    });

                    Plotly.relayout('line-chart', {
                        width: lineWidth,
                        height: 350
                    });
                }
            }, 100);
        }
    });
});
