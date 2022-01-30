   function copyText() {
                        /* Get the text field */
                        var copyText = document.getElementById("myInput ");

                        /* Select the text field */
                        copyText.select();
                        copyText.setSelectionRange(0, 99999); /* For mobile devices */

                        /* Copy the text inside the text field */
                        document.execCommand("copy ");

                        /* Alert the copied text */
                        // alert("Copied the text: " + copyText.value);
                        // Get the snackbar DIV
                        var x = document.getElementById("snackbar ");

                        // Add the "show " class to DIV
                        x.className = "show ";

                        // After 3 seconds, remove the show class from DIV
                        setTimeout(function () {
                            x.className = x.className.replace("show ", " ");
                        }, 3000);
                    }

var otpfield = document.getElementById('otpEntry'); 

otpfield.addEventListener("keyup",
    function removeotpError(){
    var otpError = document.getElementById('otpError'); 

        otpError.innerText = '';

    })

var phonefield = document.getElementById('phoneEntry');
phonefield.addEventListener("keyup",
    function removeError(){
        var phoneError = document.getElementById('phoneError');

        phoneError.innerText = '';

    })


// sendOTP

function sendOTP() {
    var country = document.getElementById('countryEntry');
    var phone = document.getElementById('phoneEntry');
    var sendotpBtn = document.getElementById("sendotpBtn");
    var sendOTPDiv = document.getElementById('sendOTPDiv');
    var verifyOTPDiv = document.getElementById('verifyOTPDiv');
    var phoneError = document.getElementById('phoneError');

    var country = country.value;
    var phone = phone.value;

    sendotpBtn.classList.add('btnactive');
    sendotpBtn.disabled = true;

    var entry = {'country': country,
                'phone': phone,
                };  

                 fetch(`${window.origin}/verifyPhone`, {
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

                        sendOTPDiv.style.display = 'none'
                        verifyOTPDiv.style.display = 'block'
                        document.getElementById('phoneNumber').innerText = data.phone;


                    }else{
                        sendotpBtn.classList.remove('btnactive');
                        sendotpBtn.disabled = false;
                        phoneError.innerText = data.error;

                }

                })
            })
}

        // verify otp
function verifyOTP(){

  var otpEntry = document.getElementById('otpEntry'); 
  var verifyotpBtn = document.getElementById('verifyotpBtn');
  var otpError = document.getElementById('otpError'); 
    var phone = document.getElementById('phoneEntry').value;
    var parentphoneEntry =document.getElementById('parentphoneEntry');
    var verify = document.getElementById('verify');
    var username = document.getElementById('username');


  verifyotpBtn.disabled = true;
  verifyotpBtn.classList.add('btnactive');

  otp = otpEntry.value

  var entry = { 'otp':otp,
  'phone':phone,
  'username':username.value
                };  

            fetch(`${window.origin}/verifyOTP`, {
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

                        parentphoneEntry.value = data.phone;
                        verify.style.display = 'none';


                    }else{
                          verifyotpBtn.disabled = false;
                        verifyotpBtn.classList.remove('btnactive');
                      otpError.innerText = data.error;

                }

                })
            })


}
        document.onreadystatechange = function() {
            if (document.readyState !== "complete") {
                document.querySelector(
                  "body").style.visibility = "hidden";
                document.querySelector(
                  "#loader").style.visibility = "visible";
            } else {
                document.querySelector(
                  "#loader").style.display = "none";
                document.querySelector(
                  "body").style.visibility = "visible";
            }
        };
        function goBack() {
            window.history.back();
        }