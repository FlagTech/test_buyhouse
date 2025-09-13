

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
                $('#rent_payment').text(data.rent_payment)
                
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
                  $('#rent_payment').text(data.rent_payment)

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
