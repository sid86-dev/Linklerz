        var pass = document.getElementById("passInput");
        var email = document.getElementById("emailInput")

        var passError = document.getElementById("passError");
        var passDiv = document.getElementById('passDiv');
        var emailDiv = document.getElementById("emailDiv");
        var emailError = document.getElementById("myError");
        var fullnameDiv = document.getElementById("fullnameDiv")
        var belowLoader = document.getElementById("belowLoader")
      

// email validation listener
           email.addEventListener("keyup",
      function validationEmail(){
          emailDiv.style.border = '1px solid #e6e6e6';
          emailError.style.display = 'none';
            document.getElementById("submitButton").disabled = false;
            fullnameDiv.style.marginTop = '22px'


      })


// password validation listener

      pass.addEventListener("keyup",
      function validationPassword(){

        passError.style.display = 'block';
        
        let strongPassword1 = new RegExp('(?=.*[a-z])(?=.*[0-9])(?=.{6,})')
        if(strongPassword1.test(pass.value)){
          passError.style.display="none";
          passDiv.style.border = '1px solid #e6e6e6';
          submitButton.style.opacity = 1.0;
          submitButton.disabled = false;
          passDiv.style.marginBottom = '40px';


        }
        else{
          passError.style.color="red";
          passError.innerHTML = "Password must contain at least 6 characters and a number";
          passDiv.style.border = '2px solid red';
          submitButton.style.opacity = 0.7;
          submitButton.disabled = true;
          passDiv.style.marginBottom = '15px';


        }
      }
      
      )



// signup entry to backend

        function submit_entry(){

            var fullnameInput = document.getElementById("fullnameInput");
            var useremailInput = document.getElementById("emailInput");
            var userpassInput = document.getElementById("passInput");
            var emailError = document.getElementById("myError");
            var submitButton = document.getElementById("submitButton"); 
            var loader = document.getElementById("loader-line");

            if (fullnameInput.value == "" || useremailInput.value == "" || userpassInput.value == "") {

            document.getElementById("myError").innerHTML = "All fields are required";
            document.getElementById("myError").style.display = 'block';
            fullnameDiv.style.marginTop = '0px'


            } else{

            // to be done before fetching
            emailError.innerHTML = '';
            userpassInput.type = 'password';
            submitButton.disabled = true;
            loader.style.display = 'block';
            submitButton.style.opacity = 0.5;
            submitButton.style.backgroundColor = 'black'
            belowLoader.style.marginTop = '0px'


            var entry = {
                fullname: fullnameInput.value,
                useremail: useremailInput.value,
                userpass: userpassInput.value
            };

            fetch(`${window.origin}/signup/data`, {
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

                    if (data.error == 'No-error'){

                        url = `${window.origin}/newaccount/${data.email}`
                        location.replace(url)

                    }else{
                    document.getElementById("submitButton").disabled = true;
                    document.getElementById("loader-line").style.display = 'none';

                    document.getElementById("myError").innerHTML = data.error;
                    document.getElementById("myError").style.display = 'block';
                    document.getElementById("emailDiv").style.border = '2px solid red';
                    fullnameDiv.style.marginTop = '0px'
                    belowLoader.style.marginTop = '3.5px'
                    submitButton.style.opacity = 1;
                    submitButton.style.backgroundColor = '#2EE59D';
                }

                })
            })


}
        }




        // to show password
        function showPass() {
            var x = document.getElementById("passInput");
            var eyeShow = document.getElementById("eyeShow");
            var eyeHide = document.getElementById("eyeHide");

              if (x.type === "password") {

                eyeShow.style.display = 'none';
                eyeHide.style.display = 'block';
                x.type = "text";
              } else {
                eyeShow.style.display = 'block';
                eyeHide.style.display = 'none';
                x.type = "password";
              }
            }


        // to copy text
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
            setTimeout(function() {
                x.className = x.className.replace("show ", " ");
            }, 3000);
        }