// event lisneter for showing save btn
const linkCollection = document.getElementsByClassName("link");
const addlinkBtn = document.getElementById('addnewlink');

for (let i = 0; i < linkCollection.length; i++) {
    console.log(linkCollection[i].value)
    linkCollection[i].addEventListener("keyup",
      function validationPassword(){
        document.getElementById('savebtn').style.display = 'block';


      })
}

// addlinkBtn.addEventListener("keyup",
//       function validationPassword(){
//         document.getElementById('savebtn').style.display = 'block';
//       })


// remove item in edit tab
function removeLink(id){
    var item = document.getElementById(id);
    const str = item.innerText.toLowerCase();
    const linkName = str.charAt(0).toUpperCase() + str.slice(1);

Swal.fire({
  title: `Do you want to delete ${linkName}?`,
  showDenyButton: true,
  showCancelButton: false,
  confirmButtonText: 'No',
  denyButtonText: `Yes`,
}).then((result) => {
  /* Read more about isConfirmed, isDenied below */
  if (result.isConfirmed) {
  } else if (result.isDenied) {

            var entry = {'name':linkName
                };  

            fetch(`${window.origin}/delete/link`, {
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
                    item.style.display = 'none';
                    Swal.fire(
                          'Deleted!',
                           data.message,
                          'success'
                        )

                    }else{
                Swal.fire(
                          'Sorry',
                          data.error,
                          'error'
                        )                      
                }

                })
            })



  }
})
}



function saveLink() {
  console.log('saveLink');
}