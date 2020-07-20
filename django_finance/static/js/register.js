// console.log('register working')
// For username Validation
const usernameField = document.querySelector('#usernameField');
const feedbackArea = document.querySelector('.invalid-username');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');

// For Email Validation
const emailField = document.querySelector('#emailField');
const emailArea = document.querySelector('.invalid-email');


// For Password Toggle
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const passwordField = document.querySelector('#passwordField');

// For disabling Submit button when there's error
const submitBtn = document.querySelector('.submit-btn');



// username validation starts here
usernameField.addEventListener('keyup', (e) => {
    // console.log('Username Event');
    const usernameVal = e.target.value; //Getting the event value

    usernameSuccessOutput.style.display = "block";

    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;

    //Disable Submit button
    submitBtn.removeAttribute("disabled", "disabled");

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
            console.log('data', data);
            
            usernameSuccessOutput.style.display = "none";

            if(data.username_error){
                //Disable Submit button
                submitBtn.setAttribute("disabled", "disabled");
                // Adding Error CSS and Message
                usernameField.classList.add("is-invalid")
                feedbackArea.style.display = 'block'
                feedbackArea.innerHTML = `<p>${data.username_error}</p>`
            }
        });
    }
     
});


// Email Validation Starts Here
emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value; //Getting the event value

    //Enable Submit button
    submitBtn.removeAttribute("disabled", "disabled");
    // Adding Default value on CSS properties
    emailField.classList.remove("is-invalid")
    emailArea.style.display = 'none'

    // Check whether the username is Available or not
    if(emailVal.length>0)
    {
        // Making an API call
        fetch('/authentication/validate-email/', {
            body: JSON.stringify({email: emailVal}), 
            method: 'POST',
        })
        .then(res=>res.json())
        .then(data=>{
            console.log('data', data)
            if(data.email_error){
                //Disable Submit button
                submitBtn.setAttribute("disabled", "disabled");
                // Adding Error CSS and Message
                emailField.classList.add("is-invalid");
                emailArea.style.display = 'block';
                emailArea.innerHTML = `<p>${data.email_error}</p>`;
            }
        });
    }
});


// Password SHOW/HIDE Toggle
//New Method
const handleToggleInput = (e)=>{
    if(showPasswordToggle.textContent === 'SHOW'){
        showPasswordToggle.textContent = 'HIDE';
        passwordField.setAttribute("type","text");
    } else {
        showPasswordToggle.textContent = 'SHOW';
        passwordField.setAttribute("type","password");
    }
};

showPasswordToggle.addEventListener('click', handleToggleInput);

//Earlier Method

// showPasswordToggle.addEventListener('click', (e) => {
//     // console.log('mouse found');
//     if(showPasswordToggle.textContent === 'SHOW'){
//         showPasswordToggle.textContent = 'HIDE';
//         passwordField.setAttribute("type","text");
//     } else {
//         showPasswordToggle.textContent = 'SHOW';
//         passwordField.setAttribute("type","password");
//     }
// });




