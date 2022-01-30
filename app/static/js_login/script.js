// password validation listener

var submitButton =  document.getElementById("submitButton");
var showPass  = document.getElementById("showPass");
var pass = document.getElementById("passInput");
var loginLoader =   document.getElementById("loginLoader");
var error = document.getElementById("error");
var userInput = document.getElementById("userInput");
var topDiv = document.getElementById("topDiv");


      userInput.addEventListener("keyup",
      function removeError(){
        topDiv.style.paddingBottom = "35px"
        error.innerText = ''

      })




      pass.addEventListener("keyup",
      function validationPassword(){
        topDiv.style.paddingBottom = "35px"
        error.innerText = ''
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

// verify otp
function verifyOTP(){
  var i1 = document.getElementById('otpinput1').value;
  var i2 = document.getElementById('otpinput2').value;
  var i3 = document.getElementById('otpinput3').value;
  var i4 = document.getElementById('otpinput4').value;
  var verifybtn = document.getElementById('verifybtn'); 
  var otpError = document.getElementById('otpError'); 


  verifybtn.disabled = true;
  otpError.innerText = '';
  verifybtn.style.opacity = '0.7';
  otp = i1+i2+i3+i4;


  data = getParameters();
  var entry = {'authid': data.authid,
                'userid': data.userid,
                'otp':otp
                };  

            fetch(`${window.origin}/authUser`, {
                method: "POST",
                credentials: "include",
                body: JSON.stringify(entry),
                cache: "no-cache",
                headers: new Headers({
                    "content-type": "application/json"
                })
            })
            .then(function (response){
                if (response.status !== 200){
                    console.log("Response Status was not 200");
                    return ;
                }

                response.json().then(function (data) {

                    if (data.error == 'no-error'){

                        url = `${window.origin}/home/${data.username}`
                        location.replace(url)

                    }else{
                      otpError.innerText = data.error;
                      verifybtn.disabled = false;
                      verifybtn.style.opacity = '1.0';


                }

                })
            })


}


// get url params
function getParameters() {
      let urlString = window.location.href;

      var url = new URL(urlString);
      var authid = url.searchParams.get("auth");
      var userid = url.searchParams.get("user");

      let data = {'authid':authid, 'userid':userid}
      return data;
    }


// submit login data
function submitData() {
    if (userInput.value == "" || pass.value == "" ) {
      error.innerText = "All fields are required"
    }
    else{
  submitButton.style.display = 'none';
  loginLoader.style.display = 'block';
  error.innerText = '';

            var entry = {
                        username: userInput.value,
                        userpass: pass.value
                    };   

                fetch(`${window.origin}/login/data`, {
                method: "POST",
                credentials: "include",
                body: JSON.stringify(entry),
                cache: "no-cache",
                headers: new Headers({
                    "content-type": "application/json"
                })
            })
            .then(function (response){
                if (response.status !== 200){
                    console.log("Response Status was not 200");
                    return ;
                }

                response.json().then(function (data) {

                    if (data.error == 'no-error'){
                        if (data.auth == 'yes'){

                          document.getElementById("authwindow").click(); // Click on the checkbox
                          submitButton.style.display = 'block';
                          loginLoader.style.display = 'none';

                          // url params
                            var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + `?auth=${data.authid}&user=${data.userid}`;
                            window.history.pushState({ path: newurl }, '', newurl);

                            document.getElementById("userphone").innerText = data.phone

                        }
                        else if(data.auth == 'no'){
                          url = `${window.origin}/home/${data.username}`;
                          location.replace(url);
                        }
                    else{
                        error.innerText = data.error;
                        topDiv.style.paddingBottom = '12px'
                        submitButton.style.display = 'block';
                        loginLoader.style.display = 'none';
                    }

                    }else{
                    error.innerText = data.error;
                    topDiv.style.paddingBottom = '12px'

                    submitButton.style.display = 'block';
                    loginLoader.style.display = 'none';
                }

                })
            })

    } 
}