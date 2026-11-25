

    // 取得被點擊區塊的縣市名稱（金門等縣市的 data-name-zh 在外層 <g> 上）
      function getCityName(el){
         return $(el).closest('[data-name-zh]').attr('data-name-zh');
      }

      // 是否已選擇縣市
      function hasCity(){
         var c = $('#city2').text();
         return c && c !== '--';
      }

    //   call back
      $("#app path").on("click", function(){
         var location = getCityName(this);
         if (!location) { return; }
         $('#city2').text(location);
         $('#city3').text(location);

         $.getJSON({ url: "/plt", 
               data: { 'city': location,
                        'price': $("#inlineCheckbox1:checked").val(),
                        'rent': $("#inlineCheckbox2:checked").val(),
                        'A_price': $("#inlineCheckbox3:checked").val(),
                        'A_rent': $("#inlineCheckbox4:checked").val(),
                        'index' : $("#inlineCheckbox5:checked").val()
                                 
               }, success: function (data) {
                   // jQuery getJSON 已經自動解析 JSON，不需要再 parse
                   Plotly.purge('graph_trend');
                   Plotly.newPlot('graph_trend', data.data, data.layout, {
                       responsive: true,
                       displayModeBar: false
                   });
                     }
               });

         $.getJSON({ url: "/cb2", 
               data: { 'city':  location,
                       'type': $("[name='radio-group1']:checked").val(),
                       'duration': $("[name='radio-group2']:checked").val()
                               
               }, success: function (data) {
           
                $('#price_location').text(data.price_location),
                $('#rent_location').text(data.rent_location)

                   }
                });

         // 更新箱型圖
         $.getJSON({ url: "/pltbox", 
               data: { 'city': location,
                       'type': $("[name='radio-group1']:checked").val(),
                       'duration': $("[name='radio-group2']:checked").val()
                               
               }, success: function (data) {
           
                Plotly.newPlot('graph_box', data);

                   }
                });

         // 更新長條圖
         $.getJSON({ url: "/pltbar", 
               data: {  'high': $("#inlineCheckbox6:checked").val(),
                        'price': $("#inlineCheckbox7:checked").val(),
                        'rent': $("#inlineCheckbox8:checked").val(),
                        'income': $("#inlineCheckbox9:checked").val(),
                        'times': $("#inlineCheckbox10:checked").val()
                           
               }, success: function (data) {
      
               Plotly.newPlot('graph_bar', data);

               }
         });

      });

      $(".form-check input").on("click", function(){

         if (hasCity()) $.getJSON({ url: "/plt", 
               data: { 'city': $('#city2').text(),
                        'price': $("#inlineCheckbox1:checked").val(),
                        'rent': $("#inlineCheckbox2:checked").val(),
                        'A_price': $("#inlineCheckbox3:checked").val(),
                        'A_rent': $("#inlineCheckbox4:checked").val(),
                        'index' : $("#inlineCheckbox5:checked").val()
                                 
               }, success: function (data) {
                   // jQuery getJSON 已經自動解析 JSON，不需要再 parse
                   Plotly.purge('graph_trend');
                   Plotly.newPlot('graph_trend', data.data, data.layout, {
                       responsive: true,
                       displayModeBar: false
                   });

                     }
               });
         $.getJSON({ url: "/pltbar", 
               data: {  'high': $("#inlineCheckbox6:checked").val(),
                        'price': $("#inlineCheckbox7:checked").val(),
                        'rent': $("#inlineCheckbox8:checked").val(),
                        'income': $("#inlineCheckbox9:checked").val(),
                        'times': $("#inlineCheckbox10:checked").val()
                           
               }, success: function (data) {
      
               Plotly.newPlot('graph_bar', data);


               }
         });

      });



      $("#Hero input").on("click", function(){
         $('#city4').text($("[name='radio-group1']:checked").val());
         $('#city5').text($("[name='radio-group2']:checked").val());
         if (!hasCity()) { return; }
         $.getJSON({ url: "/cb2", 
                 data: { 'city': $('#city2').text(),
                         'type': $("[name='radio-group1']:checked").val(),
                         'duration': $("[name='radio-group2']:checked").val()
                                 
                 }, success: function (data) {
             
                  $('#price_location').text(data.price_location),
                  $('#rent_location').text(data.rent_location)

                     }
                  });
         $.getJSON({ url: "/pltbox", 
                 data: { 'city': $('#city2').text(),
                         'type': $("[name='radio-group1']:checked").val(),
                         'duration': $("[name='radio-group2']:checked").val()
                                 
                 }, success: function (data) {
             
                  Plotly.newPlot('graph_box', data);

                     }
                  });         
               });

      $("#Villain input").on("click", function(){
         $('#city4').text($("[name='radio-group1']:checked").val());
         $('#city5').text($("[name='radio-group2']:checked").val());
         if (!hasCity()) { return; }
         $.getJSON({ url: "/cb2", 
                  data: { 'city': $('#city2').text(),
                           'type': $("[name='radio-group1']:checked").val(),
                           'duration': $("[name='radio-group2']:checked").val()
                                 
                  }, success: function (data) {
               
                  $('#price_location').text(data.price_location),
                  $('#rent_location').text(data.rent_location)

                     }
                  });

         $.getJSON({ url: "/pltbox", 
                  data: { 'city': $('#city2').text(),
                          'type': $("[name='radio-group1']:checked").val(),
                          'duration': $("[name='radio-group2']:checked").val()
                                  
                  }, success: function (data) {
              
                   Plotly.newPlot('graph_box', data);
 
                      }
                   });
               });






     $('#app path').mouseover(function(){ 
        var location = getCityName(this);
        if (!location) { return; }
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

            var city = getCityName(this);

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
