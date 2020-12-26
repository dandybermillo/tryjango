(function () {
  //   Handle Login
  $("#login-btn").click(function(e) {
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
    }, 40000);
  });

  $("#join-btn").click(function(e) {
    // $("#login-form").submit(function (e) {
       console.log("submit form joins");
       e.preventDefault();
   //  url: "/sign_in_url/",url: "{% url 'fx:sign_in_url' %}",
       $.ajax({
         type: "POST",
         url: "/join/",
   
         data: $("#join-form").serialize(),
         success: function (response) {
           // do something with response
           response["result"]; // equals 'Success or failed';
           response["message"]; // equals 'you"re logged in or You messed up';
   
           if (response["type"] === "success") {
             $("#join-form").trigger("reset");
             $("#join-success").text(response["message"]);
             $("#join-success").css({ display: "block" });
             console.log("data saved");
             
            //  window.location.replace("/user/");
           } else if (response["type"] === "error") {
            // console.log("Something went wrong! Try again.");
             $("#join-error").text(response["message"]);
             $("#join-error").css({ display: "block" });
             console.log("saving denied");
   
           }
         },
         error: function (response) {
           // do something with response
           console.log("Something went wrong! Try again.");
           $("#join-error").text("Something went wrong! Try again.");
           $("#join-error").css({ display: "block" });
         },
       });
   
       setTimeout(function () {
         $("#join-success").css({ display: "none" });
         $("#join-error").css({ display: "none" });
       }, 40000);
     });

     $("#mobile-btn").click(function(e) {
      // $("#login-form").submit(function (e) {
         console.log("submit form joins");
         e.preventDefault();
     //  url: "/sign_in_url/",url: "{% url 'fx:sign_in_url' %}",
         $.ajax({
           type: "POST",
           url: "/mobile/",
     
           data: $("#mobile-form").serialize(),
           success: function (response) {
             // do something with response
             response["result"]; // equals 'Success or failed';
             response["message"]; // equals 'you"re logged in or You messed up';
     
             if (response["type"] === "success") {
               $("#mobile-form").trigger("reset");
               $("#mobile-dialog").show();
                
              //  $("#mobile-success").text(response["message"]);
              //  $("#mobile-success").css({ display: "block" });
               console.log("data saved");
               
              //  window.location.replace("/user/");
             } else if (response["type"] === "error") {
              // console.log("Something went wrong! Try again.");
               $("#mobile-error").text(response["message"]);
               $("#mobile-error").css({ display: "block" });
               console.log("saving denied");
     
             }
           },
           error: function (response) {
             // do something with response
             console.log("Something went wrong! Try again.");
             $("#mobile-error").text("Something went wrong! Try again.");
             $("#mobile-error").css({ display: "block" });
           },
         });
     
         setTimeout(function () {
           $("#mobile-success").css({ display: "none" });
           $("#mobile-error").css({ display: "none" });
         }, 40000);
       });


$("#message-btn").click(function(e) {
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
