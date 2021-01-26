(function () {
 //  var ready =true;
   
//   setInterval(function(){

//     console.log("SetInterval");

//     if (ready == true){ 
//                 ready=false;
//               $.ajax({
//               type: "GET",
//               url:  "{% url 'fx:live_url' member.id %}",
              
//               success: function (response) {
//                 $("#display").empty();
//                 $("#display").append
//                 ready=true;
                
//                 row_ctr =0;
//                 response["live"].forEach(function (item) {
//                             //console.log("....item:",item);
//                             row_ctr = row_ctr + 1;
//                             //fill_table(item, row_ctr );
//                           var temp = "<tr><td>"+ row_ctr+"</td> <th scope='row'>" +item.customer__member_id+ "</th> <td>"+item.status+"</td><td>"+item.remarks+"</td></tr>"
//                             $("#display").append(temp);

//                     });
                  

                
//               },
//               error: function (response) {
//                 // do something with response
//                 console.log("Error");
//                 ready=true;
                
//               },
//             });
//             ready=true;
//             }


// }, 10000);



  var code ="";
  //   Handle Login
  $("#login-btn").click(function(e) {

    code="login";
    //var form =  document.querySelector(".needs-validation");
    var form = document.querySelector('#login-form');
    var reportVal = form.checkValidity();
    if (reportVal == false) {
        console.log("validating......login");
        // $("#venture-payment-failed-alert").show();
        form.reportValidity();
        return;
    }
 // $("#login-form").submit(function (e) {
    console.log("submit form init");
    e.preventDefault();
//  url: "/sign_in_url/",url: "{% url 'fx:sign_in_url' %}",
    $.ajax({
      type: "POST",
      url: "/sign-in/",

      data: $("#login-form").serialize(),
      success: function (response) {
        // do something with response
        response["result"]; // equals 'Success or failed';
        response["message"]; // equals 'you"re logged in or You messed up';

        if (response["type"] === "success") {
          $("#login-form").trigger("reset");
          // $("#login-success").text(response["message"]);
          // $("#login-success").css({ display: "block" });
          console.log("Acccess granted");
         // $("#user-page-lnk").click();
          id = response["id"];
          window.location.replace("/user/"+id);
        } else if (response["type"] === "error") {
         
          $("#login-danger-alert").fadeIn();  // alert message
          closeSnoAlertBox("login","danger");
           
          console.log("Acccess denied");

        }
      },
      error: function (response) {
        // do something with response
        console.log("Something went wrong! Try again..");
     //   $("#login-error").text("Something went wrong! Try again.");
     $("#login-danger-alert").fadeIn();  // alert message
     closeSnoAlertBox("login","danger");
      },
    });

    setTimeout(function () {
      $("#login-success").css({ display: "none" });
      $("#login-error").css({ display: "none" });
    }, 10000);
  });
  // validate form button
  $(".validate-form-btn").click(function(e){
      console.log("validate is cliked");
      id = $(this).attr("code");
      console.log("id: "+id);
      var form = document.querySelector("#"+id  +"-form");
      console.log("form");
      console.log(form);

      var reportVal = form.checkValidity();
      if (reportVal == false) {
          console.log("validating...... forl from validate -form - btn");
          // $("#venture-payment-failed-alert").show();
          form.reportValidity();
          return
          // $("#mobile-dialog").show();
           
          
      }else { 
         
          //$(this).prop("disabled", true);
//          $("#mobile-form :input").prop("disabled", true);
          // $("#close-mobile-btn").show();
          
          // $("#close-"+id).show()
        
          //$("[code='mobile-btn']")[0].show();
          
          $("#"+id+"-btn").submit();
          console.log(" submit btn is cliked on other button");
          
         
 
      }
     

     });
      

    
     $(".close-form-btn").click(function(e) {
      code= $(this).attr("code");
      $("#"+code+"-x-ico").click();
      $("#" +code+"-form").trigger("reset");
     });

     $(".submit-btn").submit(function(e) {
      // var form = document.querySelector(".needs-validation");
         console.log('----------------submit-btn');
         console.log("---------- fom id:"+$(this).attr("form"));
         selected_form = $(this).attr("form");
         code = $(this).attr("code");
         console.log(">>>Selected form: " +selected_form + " " +code);
       
         e.preventDefault();
         console.log("initiating ajax call!!!!!!");
     //  url: "/sign_in_url/",url: "{% url 'fx:sign_in_url' %}",
         $.ajax({
           type: "POST",
           url: "/process-form/",
           data: $("#"+selected_form).serialize(),
           success: function (response) {
             // do something with1 response
             console.log("success!");
             response["result"]; // equals 'Success or failed';
             response["message"]; // equals 'you"re logged in or You messed up';
     
             if (response["type"] === "success") {
               //$("#" +code+"-form").trigger("reset");
               //$("#" +code+"-dialog").show();
              console.log("----");
              console.log(" code::"+"#"+code+"-success-alert" );
               $("#"+code+"-success-alert").css({ display: "block" });//.fadeIn();  // alert message
               closeSnoAlertBox(code,"success");

              //  $("#"+code+"-success").text(response["message"]);
              //  $("#"+code+"-success").css({ display: "block" });
               console.log("data saved");
               
              //window.location.replace("/user/2/");
             } else if (response["type"] === "error") {
              // console.log("Something went wrong! Try again.");
              $("#"+ code+"-danger-alert").fadeIn();  // alert message
              closeSnoAlertBox(code,"danger");
              //  $("#"+code+"-error").text(response["message"]);
              //  $("#" +code+"-error").css({ display: "block" });
               console.log("saving denied");
     
             }
           },
           error: function (response) {
             // do something with response'
             $("#profile-danger-alert").fadeIn();  // alert message
             closeSnoAlertBox(code,"danger");
             console.log("Something went wrong! Try again.response:");
             console.log(response);
            //  $("#"+code+ "-error").text("Something went wrong! Try again.");
            //  $("#"+code+"-error").css({ display: "block" });
           },
         });
     
         setTimeout(function () {
           console.log("Settimeout:"+code)
           $("#"+code+"-success").css({ display: "none" });
           $("#"+code+"-error").css({ display: "none" });
         }, 10000);
       
       
        //  $("#"+selected_form+" :input").prop("disabled", true);
        });



        function closeSnoAlertBox(code,message){
          console.log("closeSnoalertBox===================");
          window.setTimeout(function () {
            console.log("line:"+"#"+code+"-"+ message+"-alert");
            $("#"+code+"-"+ message+"-alert").fadeOut(300)
            $("#"+code+"-"+ message+"-alert").css({ display: "none" });

          }, 10000);
          } 
          
          
          $(".hide-modal-btn").click(function(e) {
            code= $(this).attr("code");
            console.log(" code::"+ code);
            $("#"+code).modal('hide');

            
           });         


})();
