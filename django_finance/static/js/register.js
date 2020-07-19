// console.log('register working')

const usernameField = document.querySelector('#usernameField');
const feedbackArea = document.querySelector('.invalid-feedback')

usernameField.addEventListener('keyup', (e) => {
    // console.log('Username Event');
    const usernameVal = e.target.value; //Getting the event value

    // Adding Default value on CSS properties
    usernameField.classList.remove("is-invalid")
    feedbackArea.style.display = 'none'

    // Check whether the username is Available or not
    if(usernameVal.length>0)
    {
        // Making an API call
        fetch('/authentication/validate-username/', {
            body: JSON.stringify({username: usernameVal}), 
            method: 'POST',
        })
        .then(res=>res.json())
        .then(data=>{
            console.log('data', data)
            if(data.username_error){
                // Adding Error CSS and Message
                usernameField.classList.add("is-invalid")
                feedbackArea.style.display = 'block'
                feedbackArea.innerHTML = `<p>${data.username_error}</p>`
            }
        });
    }
     
});