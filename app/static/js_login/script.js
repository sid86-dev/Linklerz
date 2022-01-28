// password validation listener

var submitButton =  document.getElementById("submitButton");
var showPass  = document.getElementById("showPass");
var pass = document.getElementById("passInput");

      pass.addEventListener("keyup",
      function validationPassword(){

        pass.style.marginBottom = "0px";
        showPass.style.display = 'block'

        let strongPassword1 = new RegExp('(?=.*[a-z])(?=.*[0-9])(?=.{6,})')
        if(strongPassword1.test(pass.value)){
          document.getElementById("submitButton").disabled = false;
        }
        else{
          document.getElementById("submitButton").disabled = true;
        }
      }
      
      )


      // to show password
        function showPassword() {
            var x = document.getElementById("passInput");
            var showPass  = document.getElementById("showPass");


              if (x.type === "password") {
                x.type = "text";
                showPass.innerText = "Hide";
              } else {
                showPass.innerText = "Show";
                x.type = "password";
              }
            }
