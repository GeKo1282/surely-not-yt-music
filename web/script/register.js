addLoadEvent(() => {
    let nickname_field = document.getElementById("nickname-field");
    let password_field = document.getElementById("register-password-field");
    let repeat_password_field = document.getElementById("repeat-password-field");

    const one_letter_regEx = new RegExp("[a-zA-Z]");
    const one_digit_regEx = new RegExp("[0-9]");
    const valid_regEx = new RegExp("^[a-zA-Z0-9.!@#$%&*]+$");
    const num_sym_up_regex = new RegExp("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[.!@#$%&*])");
    const num_up_regex = new RegExp("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])");
    const num_or_up_regex = new RegExp("(?=.*[a-z])(?=.*[A-Z0-9])");

    let min_8_div = document.getElementById("min-8-check");
    let max_64_div = document.getElementById("max-64-check");
    let one_letter_check = document.getElementById("one-letter-check");
    let one_digit_check = document.getElementById("one-digit-check");
    let valid_check = document.getElementById("valid-check");

    let yellow_bar = document.getElementById("yellow-bar");
    let green_bar = document.getElementById("green-bar");
    let blue_bar = document.getElementById("blue-bar");
    let text_span = document.getElementById("text-span");

    nickname_field.oninput = () => {
        if ((4 <= nickname_field.value.length && nickname_field.value.length <= 64) && !nickname_field.classList.contains("correct")) {
            nickname_field.classList.add("correct")
            nickname_field.classList.remove("incorrect")
        } else if (!(4 <= nickname_field.value.length && nickname_field.value.length <= 64) && !nickname_field.classList.contains("incorrect")) {
            nickname_field.classList.remove("correct")
            nickname_field.classList.add("incorrect")
        }
    }

    password_field.oninput = () => {
        let valid = true;

        if (password_field.value.length >= 8) {
            min_8_div.classList.add("correct");
        } else {
            valid = false;
            min_8_div.classList.remove("correct");
        }

        if (password_field.value.length <= 64) {
            max_64_div.classList.add("correct");
        } else {
            valid = false;
            max_64_div.classList.remove("correct");
        }
        
        if (one_letter_regEx.test(password_field.value)) {
            one_letter_check.classList.add("correct");
        } else {
            valid = false;
            one_letter_check.classList.remove("correct");
        }
        if (one_digit_regEx.test(password_field.value)) {
            one_digit_check.classList.add("correct");
        } else {
            valid = false;
            one_digit_check.classList.remove("correct");
        }

        if (valid_regEx.test(password_field.value)) {
            valid_check.classList.add("correct");
        } else {
            valid = false;
            valid_check.classList.remove("correct");
        }

        if(valid) {
            password_field.classList.add("correct");
            password_field.classList.remove("incorrect");
        } else {
            password_field.classList.remove("correct");
            password_field.classList.add("incorrect");
        }

        let points = 0;
        let value = password_field.value;

        if (num_sym_up_regex.test(value)) {
            if (value.length >= 10) {
                points = 3;
            } else if (value.length >= 9) {
                points = 2;
            } else if (value.length >= 8) {
                points = 1;
            }
        } else if (num_up_regex.test(value)) {
            if (value.length >= 11) {
                points = 3;
            } else if (value.length >= 10){
                points = 2;
            }  else if (value.length >= 9){
                points = 1;
            }
        } else if (num_or_up_regex.test(value)) {
            if (value.length >= 12) {
                points = 3;
            } else if (value.length >= 11){
                points = 2;
            }  else if (value.length >= 10){
                points = 1;
            }
        } else {
            if (value.length > 12) {
                points = 2;
            } else if (value.length > 11) {
                points = 1;
            }
        }


        if(points == 0) {
            yellow_bar.style.display = "none";
            green_bar.style.display = "none";
            blue_bar.style.display = "none";

            text_span.innerText = "Very weak";
            text_span.style.color = "#ff0505";
        } else if (points == 1) {
            yellow_bar.style.display = "block";
            green_bar.style.display = "none";
            blue_bar.style.display = "none";

            text_span.innerText = "Weak";
            text_span.style.color = "#fcba03";
        } else if (points == 2) {
            yellow_bar.style.display = "block";
            green_bar.style.display = "block";
            blue_bar.style.display = "none";

            text_span.innerText = "Medium";
            text_span.style.color = "#33ff05";
        } else if (points == 3) {
            yellow_bar.style.display = "block";
            green_bar.style.display = "block";
            blue_bar.style.display = "block";

            text_span.innerText = "Veri gut";
            text_span.style.color = "#056dff";
        }        
    }
    
    repeat_password_field.oninput = () => {
        if (repeat_password_field.value == password_field.value) {
            repeat_password_field.classList.add("correct");
            repeat_password_field.classList.remove("incorrect");
        } else {
            repeat_password_field.classList.remove("correct");
            repeat_password_field.classList.add("incorrect");
        }
    }
})


