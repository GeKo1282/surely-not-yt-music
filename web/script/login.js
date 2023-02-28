addLoadEvent(() => {
    let email_field = document.getElementById("email-field");
    let password_field = document.getElementById("password-field");

    const mail_regex = new RegExp("^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$");
    const phone_regex = new RegExp("^[0-9]{9,10}$");
    const pass_regex = new RegExp("^[a-zA-Z0-9.!@#$%&*]{8,64}$");

    email_field.oninput = () => {        
        if((mail_regex.test(email_field.value) || phone_regex.test(email_field.value)) && !email_field.classList.contains("correct")) {
            email_field.classList.add("correct");
            email_field.classList.remove("incorrect");
        } else if (!mail_regex.test(email_field.value) && !phone_regex.test(email_field.value)) {
            email_field.classList.remove("correct");
            email_field.classList.add("incorrect");
        }
    }

    password_field.oninput = () => {
        if(pass_regex.test(password_field.value) && !password_field.classList.contains("correct")) {
            password_field.classList.add("correct");
            password_field.classList.remove("incorrect");
        } else if (!pass_regex.test(password_field.value)) {
            password_field.classList.remove("correct");
            password_field.classList.add("incorrect");
        }
    }
})

async function login() {
    let data = JSON.parse(await (await (await fetch("/rsa-data")).text()));
    let chunk_length = (data.key_length / 8 - (2 * 256 / 8) - 2);
    let res = Cipher.static_encrypt(JSON.stringify({}), data.key, data.separator,
    chunk_length);
    
    console.log(res);
}