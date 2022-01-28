// qrpopu

function showQR(){
    var myBody = document.getElementById("myBody");
    var qrPopup = document.getElementById("qrPopup");

    qrPopup.style.display = "block";
    myBody.classList.toggle('blur');

}

$(document).mouseup(function (e) {
            if ($(e.target).closest("#qrPopup").length
                        === 0) {
                $("#qrPopup").hide();
                document.getElementById("myBody").classList.remove('blur');
            }
});


// download qrcode
const btn = document.getElementById('downloadQR');
const url =  document.getElementById('qrcode').src;


btn.addEventListener('click', (event) => {
  event.preventDefault();
  downloadImage(url);
})


function downloadImage(url) {
  fetch(url, {
    mode : 'no-cors',
  })
    .then(response => response.blob())
    .then(blob => {
    let blobUrl = window.URL.createObjectURL(blob);
    let a = document.createElement('a');
    a.download = url.replace(/^.*[\\\/]/, '');
    a.href = blobUrl;
    document.body.appendChild(a);
    a.click();
    a.remove();
  })
}






// logout popup
 function confirmbox() {
                        Swal.fire({
                            title: 'Do you want to logout?',
                            text: "you may need to login again",
                            showCancelButton: true,
                            confirmButtonColor: '#2EE59D',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'Yes'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                Swal.fire(
                                    'Logged out!',
                                    'Your have been logged out',
                                    'success'
                                )
                                window.location.replace("/logout");
                            }
                        })
                    }


// go back

        function goBack() {
            window.history.back();
        }


// show Settings
        function showSettings() {
            var homeContent = document.getElementById("homeContent");
            var settingsContent = document.getElementById("settingsContent");
            var settingsButton = document.getElementById("settingsButton");
            var hideButton = document.getElementById("hideButton");

            homeContent.style.display = 'none';
            settingsContent.style.display = 'block';

            settingsButton.style.display = "none";
            hideButton.style.display = "block"

        }

        function hideSettings() {
            var homeContent = document.getElementById("homeContent");
            var settingsContent = document.getElementById("settingsContent");
            var hideButton = document.getElementById("hideButton");
            var settingsButton = document.getElementById("settingsButton");

            hideButton.style.display = "none";
            settingsButton.style.display = "block"

            homeContent.style.display = 'block';
            settingsContent.style.display = 'none';

        }

// loader
    document.onreadystatechange = function () {
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


// copytext

 function copyText() {
                /* Get the text field */
                var copyText = document.getElementById("copyText");

                copyText.disabled = false;

                /* Select the text field */
                copyText.select();
                copyText.setSelectionRange(0, 99999); /* For mobile devices */

                /* Copy the text inside the text field */
                document.execCommand("copy");

                /* After the copied text */

                copyText.disabled = true;

                // Get the snackbar DIV
                var x = document.getElementById("snackbar");

                // Add the "show" class to DIV
                x.className = "show";

                // After 3 seconds, remove the show class from DIV
                setTimeout(function () {
                    x.className = x.className.replace("show", "");
                }, 3000);
            }



// share link
const shareButton = document.querySelector('.share-button');
const shareDialog = document.querySelector('.share-dialog');
const closeButton = document.querySelector('.close-button');
const username = document.getElementById('datauserName').innerText;

shareButton.addEventListener('click', event => {
  if (navigator.share) { 
   navigator.share({
      title: `Linklerz-${username}`,
      url: `https://shwt.xyz/${username}`
    }).then(() => {
      console.log('Thanks for sharing!');
    })
    .catch(console.error);
    } else {
        shareDialog.classList.add('is-open');
    }
});

closeButton.addEventListener('click', event => {
  shareDialog.classList.remove('is-open');
});