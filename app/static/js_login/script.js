// password validation listener

var submitButton =  document.getElementById("submitButton");
var showPass  = document.getElementById("showPass");
var pass = document.getElementById("passInput");
var loginLoader =   document.getElementById("loginLoader");
var error = document.getElementById("error");
var userInput = document.getElementById("userInput");



      pass.addEventListener("keyup",
      function validationPassword(){

        pass.style.marginBottom = "0px";
        showPass.style.display = 'block'

        let strongPassword1 = new RegExp('(?=.*[a-z])(?=.*[0-9])(?=.{6,})')
        if(strongPassword1.test(pass.value)){
          submitButton.disabled = false;
          submitButton.style.opacity = 1.0;
        }
        else{
          submitButton.disabled = true;
          submitButton.style.opacity = 0.7;
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

function submitData() {
    if (userInput.value == "" || pass.value == "" ) {
      error.innerText = "All fields are required"
    }
    else{
  submitButton.style.display = 'none';
  loginLoader.style.display = 'block';

  var entry = {
                username: userInput.value,
                userpass: pass.value
            };   

            console.log(entry);

  var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + `?user=${userInput.value}`;
  window.history.pushState({ path: newurl }, '', newurl); 
  

    }
  
  
}