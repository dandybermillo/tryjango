(function () {
  //   Handle Login
  $("#login-form").submit(function (e) {
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
})();
