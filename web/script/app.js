addLoadEvent(() => {
    var rsa_data = fetch("/rsa-data", {
        method: "POST",
        body: ""
    });

    window.server_key = rsa_data.key;

    window.cipher ??= new Cipher(rsa_data.separator, false);

    if (!(window.localStorage.getItem('public_key') && window.localStorage.getItem('private_key') && window.localStorage.getItem('chunk_length'))) {
        window.cipher.generate_keys(rsa_data.key_length);

        window.localStorage.setItem('private_key', window.cipher.private_key);        
        window.localStorage.setItem('public_key', window.cipher.public_key[0]);        
        window.localStorage.setItem('chunk_length', window.cipher.public_key[1]);  

    } else {
        window.cipher.import_public_key(window.localStorage.getItem('public_key'), parseInt(window.localStorage.getItem('chunk_length')));
        window.cipher.import_private_key(window.localStorage.getItem('private_key'));
    }
})

addLoadEvent(() => {
    var search_box = document.getElementById('search-box');
    var search_query_input = document.getElementById('search-query');
    var clear_button_box = document.getElementById('search-clear-btn');

    search_query_input.oninput = () => {
        if (search_query_input.value !== '') {
            clear_button_box.style.display = '';
        } else {
            clear_button_box.style.display = 'none';
        }
    }

    document.onclick = (event) => {
        if (event.target != search_box && !search_box.contains(event.target) && event.target != document.getElementById('search-btn')) {
            close_search();
        }
    }
})

function change_subpage(subpage) {
    var subpages = ['home', 'explore', 'library'];
    subpages.forEach((page) => {
        if (page != subpage) {
            document.getElementById(`${page}-page`).style.display = 'none';
        }
    })

    document.getElementById(`${subpage}-page`).style.display = '';
}

function open_search() {
    document.getElementById('search-box').style.display = '';
    document.getElementById('search-query').focus();
}

function close_search() {
    document.getElementById('search-box').style.display = 'none';
}

function logout() {
    fetch("/logout", {
        method: "POST",
        body: window.cipher.encrypt(JSON.stringify({token: window.localStorage.getItem('token')}) ,{key: window.server_key})
    });
}