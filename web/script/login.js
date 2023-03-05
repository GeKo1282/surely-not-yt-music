addLoadEvent(async () => {
    var data = await (await fetch("/rsa-data", {body: "", method: "POST"})).json();
    var cipher = new Cipher(data.separator, false);

    window.cipher = cipher;
    window.data = data;

    if(!(window.localStorage.getItem('public_key') && window.localStorage.getItem('private_key') && window.localStorage.getItem('chunk_length'))) {
        window.cipher.generate_keys(window.data.key_length);
        window.localStorage.setItem('public_key', window.cipher.public_key[0]);
        window.localStorage.setItem('chunk_length', window.cipher.public_key[1]);
        window.localStorage.setItem('private_key', window.cipher.private_key);
    } else {
        window.cipher.import_public_key(window.localStorage.getItem('public_key'), parseInt(window.localStorage.getItem('chunk_length')))
        window.cipher.import_private_key(window.localStorage.getItem('private_key'));
    }

    if(window.localStorage.getItem('token')) {
        var resposne = await (await fetch("/login", {
            method: "POST",
            body: window.cipher.encrypt(JSON.stringify({
                token: window.localStorage.getItem('token')
            }), {key: window.data.key})
        })).json()

        if (resposne.hasOwnProperty('success') && resposne.success) {
            window.location.replace("/app");
        }
    }

    var email_field = document.getElementById("email-field");
    var password_field = document.getElementById("password-field");

    const mail_regex = new RegExp("^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$");
    const phone_regex = new RegExp("^[0-9]{9,10}$");
    const pass_regex = new RegExp("^[a-zA-Z0-9.!@#$%&*]{8,64}$");

    email_field.oninput = () => {        
        if(mail_regex.test(email_field.value) || phone_regex.test(email_field.value)) {
            email_field.classList.add("correct");
            email_field.classList.remove("incorrect");
        } else {
            email_field.classList.remove("correct");
            email_field.classList.add("incorrect");
        }
    }

    if(password_field) { //That's 'cause on register page this script is loaded, but there is no field ID'd 'password-field'. Just removes error from console
        password_field.oninput = () => {
            if(pass_regex.test(password_field.value)) {
                password_field.classList.add("correct");
                password_field.classList.remove("incorrect");
            } else {
                password_field.classList.remove("correct");
                password_field.classList.add("incorrect");
            }
        }
    }
})

async function login() {
    var login = document.getElementById("email-field").value;
    var password_hash = sha512(document.getElementById("password-field").value);
    var invalid_text = document.getElementById('invalid-text');
    
    if (login == "" || password_hash == "") {
        invalid_text.style.display = 'flex';
        setTimeout(() => {
            invalid_text.style.display = 'none';
        }, 5000);
        return;
    }

    var encrypted = cipher.encrypt(JSON.stringify({"email": login, "password_hash": password_hash, key: window.cipher.public_key[0]}), {key: window.data.key});
    
    var token = JSON.parse(window.cipher.decrypt(await(await fetch("/get-token", {body: encrypted, method: "POST"})).text()));

    if (!token.hasOwnProperty('token')) {
        invalid_text.style.display = 'flex';
        setTimeout(() => {
            invalid_text.style.display = 'none';
        }, 5000);
        return;
    }

    var resposne = await (await fetch("/login", {
        method: "POST",
        body: cipher.encrypt(JSON.stringify({
            token: token.token
        }), {key: window.data.key})
    })).json()

    if (resposne.hasOwnProperty('success') && resposne.success) {
        window.localStorage.setItem('token', token.token);
        window.location.replace("/app");
    }    
}