(function () {
  $("#mobile-success").css({ display: "block" });

  var code ="";
  //   Handle Login
  $("#login-btn").click(function(e) {


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
    console.log("submit form inis");
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
          $("#login-success").text(response["message"]);
          $("#login-success").css({ display: "block" });
          console.log("Acccess granted");
         // $("#user-page-lnk").click();
           window.location.replace("/user/");
        } else if (response["type"] === "error") {
         // console.log("Something went wrong! Try again.");
          $("#login-error").text(response["message"]);
          $("#login-error").css({ display: "block" });
          console.log("Acccess denied");

        }
      },
      error: function (response) {
        // do something with response
        console.log("Something went wrong! Try again.");
        $("#login-error").text("Something went wrong! Try again.");
        $("#login-error").css({ display: "block" });
      },
    });

    setTimeout(function () {
      $("#login-success").css({ display: "none" });
      $("#login-error").css({ display: "none" });
    }, 10000);
  });
  // validate form button
  $(".validate-form-btn").click(function(e){

       id = $(this).attr("code");
      var form = document.querySelector("#"+id  +"-form");

      var reportVal = form.checkValidity();
      if (reportVal == false) {
          console.log("validating...... mobile from validate -form - btn");
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
         console.log("Selected form: " +selected_form + " " +code);
       
         e.preventDefault();
     //  url: "/sign_in_url/",url: "{% url 'fx:sign_in_url' %}",
         $.ajax({
           type: "POST",
           url: "/process-form/",
           data: $("#"+selected_form).serialize(),
           success: function (response) {
             // do something with response
             response["result"]; // equals 'Success or failed';
             response["message"]; // equals 'you"re logged in or You messed up';
     
             if (response["type"] === "success") {
               //$("#" +code+"-form").trigger("reset");
               //$("#" +code+"-dialog").show();
                
               $("#"+code+"-success").text(response["message"]);
               $("#"+code+"-success").css({ display: "block" });
               console.log("data saved");
               
              //  window.location.replace("/user/");
             } else if (response["type"] === "error") {
              // console.log("Something went wrong! Try again.");
               $("#"+code+"-error").text(response["message"]);
               $("#" +code+"-error").css({ display: "block" });
               console.log("saving denied");
     
             }
           },
           error: function (response) {
             // do something with response
             console.log("Something went wrong! Try again.");
             $("#"+code+ "-error").text("Something went wrong! Try again.");
             $("#"+code+"-error").css({ display: "block" });
           },
         });
     
         setTimeout(function () {
           console.log("Settimeout:"+code)
           $("#"+code+"-success").css({ display: "none" });
           $("#"+code+"-error").css({ display: "none" });
         }, 10000);
       
       
        //  $("#"+selected_form+" :input").prop("disabled", true);
        });


$("#message-btnsa").click(function(e) {
      // $("#login-form").submit(function (e) {
         console.log("submit form message");
         e.preventDefault();
     //  url: "/sign_in_url/",url: "{% url 'fx:sign_in_url' %}",
         $.ajax({
           type: "POST",
           url: "/message/",
     
           data: $("#message-form").serialize(),
           success: function (response) {
             // do something with response
             response["result"]; // equals 'Success or failed';
             response["message"]; // equals 'you"re logged in or You messed up';
     
             if (response["type"] === "success") {
               $("#message-form").trigger("reset");
               $("#message-dialog").show();
                
              //  $("#mobile-success").text(response["message"]);
              //  $("#mobile-success").css({ display: "block" });
               console.log("data saved");
               
              //  window.location.replace("/user/");
             } else if (response["type"] === "error") {
              // console.log("Something went wrong! Try again.");
               $("#message-error").text(response["message"]);
               $("#message-error").css({ display: "block" });
               console.log("saving denied");
     
             }
           },
           error: function (response) {
             // do something with response
             console.log("Something went wrong! Try again.");
             $("#message-error").text("Something went wrong! Try again.");
             $("#message-error").css({ display: "block" });
           },
         });
     
         setTimeout(function () {
           $("#message-success").css({ display: "none" });
           $("#message-error").css({ display: "none" });
         }, 40000);
       });


})();
