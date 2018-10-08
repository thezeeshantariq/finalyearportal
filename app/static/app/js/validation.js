$(document).ready(function () {

    var buttonSubmit = $('#btn_submit');

    isStudentSignup = false;

    /*********************************/
    /*                               */
    /*        Name Validation        */
    /*                               */
    /*********************************/
    var isNameValid = false;
    var isName3Digit = false;
    var isNameOnlyAlphabet = false;
    var $nameRegx = /^([a-zA-Z ]{3,30})$/;

    $('#input_name').on('keypress keydown keyup', function () {
        var name = $(this).val();
        if (name.length >= 3) {
            isName3Digit = true;
            $('#validator_name_checklist #validator_option_gte_3 .msg').removeClass("text-muted");
            $('#validator_name_checklist #validator_option_gte_3 .msg').removeClass("text-danger");
            $('#validator_name_checklist #validator_option_gte_3 .msg').addClass("text-success");
            $('#validator_name_checklist #validator_option_gte_3 .times').addClass("hidden");
            $('#validator_name_checklist #validator_option_gte_3 .check').removeClass("hidden");
        } else {
            isName3Digit = false;
            $('#validator_name_checklist #validator_option_gte_3 .msg').removeClass("text-muted");
            $('#validator_name_checklist #validator_option_gte_3 .msg').removeClass("text-success");
            $('#validator_name_checklist #validator_option_gte_3 .msg').addClass("text-danger");
            $('#validator_name_checklist #validator_option_gte_3 .times').removeClass("hidden");
            $('#validator_name_checklist #validator_option_gte_3 .check').addClass("hidden");
        }

        if (hasSpecialCharacter(name) || hasDigit(name)) {
            isNameOnlyAlphabet = false;
            $('#validator_name_checklist #validator_option_no_alphanumeric .msg').removeClass("text-muted");
            $('#validator_name_checklist #validator_option_no_alphanumeric .msg').removeClass("text-success");
            $('#validator_name_checklist #validator_option_no_alphanumeric .msg').addClass("text-danger");
            $('#validator_name_checklist #validator_option_no_alphanumeric .times').removeClass("hidden");
            $('#validator_name_checklist #validator_option_no_alphanumeric .check').addClass("hidden");
        } else {
            isNameOnlyAlphabet = true;
            $('#validator_name_checklist #validator_option_no_alphanumeric .msg').removeClass("text-muted");
            $('#validator_name_checklist #validator_option_no_alphanumeric .msg').removeClass("text-danger");
            $('#validator_name_checklist #validator_option_no_alphanumeric .msg').addClass("text-success");
            $('#validator_name_checklist #validator_option_no_alphanumeric .times').addClass("hidden");
            $('#validator_name_checklist #validator_option_no_alphanumeric .check').removeClass("hidden");
        }

        if (isName3Digit && isNameOnlyAlphabet)
            isNameValid = true;
        else
            isNameValid = false;


        enableOrDisableSubmitButton();
    });


    /*********************************/
    /*                               */
    /*       Email Validation        */
    /*                               */
    /*********************************/
    var isEmailValid = false;

    $('#input_email').on('keypress keydown keyup', function () {
        var email = $(this).val();
        if (isValidEmail(email)) {
            isEmailValid = true;
            $('#validator_email_checklist #validator_option_valid_email .msg').removeClass("text-muted");
            $('#validator_email_checklist #validator_option_valid_email .msg').addClass("text-success");
            $('#validator_email_checklist #validator_option_valid_email .msg').removeClass("text-danger");
            $('#validator_email_checklist #validator_option_valid_email .times').addClass("hidden");
            $('#validator_email_checklist #validator_option_valid_email .check').removeClass("hidden");
        } else {
            isEmailValid = false;
            $('#validator_email_checklist #validator_option_valid_email .msg').removeClass("text-muted");
            $('#validator_email_checklist #validator_option_valid_email .msg').removeClass("text-success");
            $('#validator_email_checklist #validator_option_valid_email .msg').addClass("text-danger");
            $('#validator_email_checklist #validator_option_valid_email .times').removeClass("hidden");
            $('#validator_email_checklist #validator_option_valid_email .check').addClass("hidden");
        }

        enableOrDisableSubmitButton();
    });


    /*********************************/
    /*                               */
    /*     Password Validation       */
    /*                               */
    /*********************************/
    var isPasswordValid = false;
    var isPasswordContainsLowerCase = false;
    var isPasswordContainsUpperCase = false;
    var isPasswordContainsNumber = false;
    var isPasswordContainsSpecialCharacter = false;
    var isPassword8Characters = false;
    var $regxPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    $('#input_password').on('keypress keydown keyup', function () {

        isPasswordValid = false;

        if ($(this).val().length >= 8) {
            isPassword8Characters = true;
            $('#validator_password_checklist #validation_option_gte_8 .msg').removeClass("text-muted");
            $('#validator_password_checklist #validation_option_gte_8 .msg').removeClass("text-danger");
            $('#validator_password_checklist #validation_option_gte_8 .msg').addClass("text-success");
            $('#validator_password_checklist #validation_option_gte_8 .times').addClass("hidden");
            $('#validator_password_checklist #validation_option_gte_8 .check').removeClass("hidden");
        } else {
            isPassword8Characters = false;
            $('#validator_password_checklist #validation_option_gte_8 .msg').removeClass("text-muted");
            $('#validator_password_checklist #validation_option_gte_8 .msg').removeClass("text-success");
            $('#validator_password_checklist #validation_option_gte_8 .msg').addClass("text-danger");
            $('#validator_password_checklist #validation_option_gte_8 .times').removeClass("hidden");
            $('#validator_password_checklist #validation_option_gte_8 .check').addClass("hidden");
        }

        var str = $(this).val();
        if (hasLowerCase(str)) {
            isPasswordContainsLowerCase = true;
            $('#validator_password_checklist #validation_option_lower_case .msg').removeClass("text-muted");
            $('#validator_password_checklist #validation_option_lower_case .msg').removeClass("text-danger");
            $('#validator_password_checklist #validation_option_lower_case .msg').addClass("text-success");
            $('#validator_password_checklist #validation_option_lower_case .times').addClass("hidden");
            $('#validator_password_checklist #validation_option_lower_case .check').removeClass("hidden");
        } else {
            isPasswordContainsLowerCase = false;
            $('#validator_password_checklist #validation_option_lower_case .msg').removeClass("text-muted");
            $('#validator_password_checklist #validation_option_lower_case .msg').addClass("text-danger");
            $('#validator_password_checklist #validation_option_lower_case .msg').removeClass("text-success");
            $('#validator_password_checklist #validation_option_lower_case .times').removeClass("hidden");
            $('#validator_password_checklist #validation_option_lower_case .check').addClass("hidden");
        }

        if (hasUpperCase(str)) {
            isPasswordContainsUpperCase = true;
            $('#validator_password_checklist #validation_option_uppercase .msg').removeClass("text-muted");
            $('#validator_password_checklist #validation_option_uppercase .msg').removeClass("text-danger");
            $('#validator_password_checklist #validation_option_uppercase .msg').addClass("text-success");
            $('#validator_password_checklist #validation_option_uppercase .times').addClass("hidden");
            $('#validator_password_checklist #validation_option_uppercase .check').removeClass("hidden");
        } else {
            isPasswordContainsUpperCase = false;
            $('#validator_password_checklist #validation_option_uppercase .msg').removeClass("text-muted");
            $('#validator_password_checklist #validation_option_uppercase .msg').addClass("text-danger");
            $('#validator_password_checklist #validation_option_uppercase .msg').removeClass("text-success");
            $('#validator_password_checklist #validation_option_uppercase .times').removeClass("hidden");
            $('#validator_password_checklist #validation_option_uppercase .check').addClass("hidden");
        }

        if (hasDigit(str)) {
            isPasswordContainsNumber = true;
            $('#validator_password_checklist #validation_option_numeric .msg').removeClass("text-muted");
            $('#validator_password_checklist #validation_option_numeric .msg').removeClass("text-danger");
            $('#validator_password_checklist #validation_option_numeric .msg').addClass("text-success");
            $('#validator_password_checklist #validation_option_numeric .times').addClass("hidden");
            $('#validator_password_checklist #validation_option_numeric .check').removeClass("hidden");
        } else {
            isPasswordContainsNumber = false;
            $('#validator_password_checklist #validation_option_numeric .msg').removeClass("text-muted");
            $('#validator_password_checklist #validation_option_numeric .msg').addClass("text-danger");
            $('#validator_password_checklist #validation_option_numeric .msg').removeClass("text-success");
            $('#validator_password_checklist #validation_option_numeric .times').removeClass("hidden");
            $('#validator_password_checklist #validation_option_numeric .check').addClass("hidden");
        }

        if (hasSpecialCharacter(str)) {
            isPasswordContainsSpecialCharacter = true;
            $('#validator_password_checklist #validation_option_alphanumeric .msg').removeClass("text-muted");
            $('#validator_password_checklist #validation_option_alphanumeric .msg').removeClass("text-danger");
            $('#validator_password_checklist #validation_option_alphanumeric .msg').addClass("text-success");
            $('#validator_password_checklist #validation_option_alphanumeric .times').addClass("hidden");
            $('#validator_password_checklist #validation_option_alphanumeric .check').removeClass("hidden");
        } else {
            isPasswordContainsSpecialCharacter = false;
            $('#validator_password_checklist #validation_option_alphanumeric .msg').removeClass("text-muted");
            $('#validator_password_checklist #validation_option_alphanumeric .msg').addClass("text-danger");
            $('#validator_password_checklist #validation_option_alphanumeric .msg').removeClass("text-success");
            $('#validator_password_checklist #validation_option_alphanumeric .times').removeClass("hidden");
            $('#validator_password_checklist #validation_option_alphanumeric .check').addClass("hidden");
        }

        if (str.length > 0) {

            if (isPassword8Characters) {
                $('#strength-very-low').removeClass('hidden');
                $('#strength-low').addClass('hidden');
                $('#strength-medium').addClass('hidden');
                $('#strength-strong').addClass('hidden');
                $('#strength-very-strong').addClass('hidden');
            }

            if (isPassword8Characters && isPasswordContainsLowerCase && isPasswordContainsUpperCase ||
                str.length > 15) {
                $('#strength-very-low').removeClass('hidden');
                $('#strength-low').removeClass('hidden');
                $('#strength-medium').addClass('hidden');
                $('#strength-strong').addClass('hidden');
                $('#strength-very-strong').addClass('hidden');
            }

            if (isPassword8Characters &&
                isPasswordContainsLowerCase &&
                isPasswordContainsUpperCase &&
                isPasswordContainsNumber) {
                $('#strength-very-low').removeClass('hidden');
                $('#strength-low').removeClass('hidden');
                $('#strength-medium').removeClass('hidden');
                $('#strength-strong').addClass('hidden');
                $('#strength-very-strong').addClass('hidden');
            }

            if (isPassword8Characters &&
                isPasswordContainsLowerCase &&
                isPasswordContainsUpperCase &&
                isPasswordContainsNumber &&
                isPasswordContainsSpecialCharacter) {
                $('#strength-very-low').removeClass('hidden');
                $('#strength-low').removeClass('hidden');
                $('#strength-medium').removeClass('hidden');
                $('#strength-strong').removeClass('hidden');
                $('#strength-very-strong').addClass('hidden');

                isPasswordValid = true;
            }

            if (isPassword8Characters &&
                isPasswordContainsLowerCase &&
                isPasswordContainsUpperCase &&
                isPasswordContainsNumber &&
                isPasswordContainsSpecialCharacter &&
                str.length > 12) {
                $('#strength-very-low').removeClass('hidden');
                $('#strength-low').removeClass('hidden');
                $('#strength-medium').removeClass('hidden');
                $('#strength-strong').removeClass('hidden');
                $('#strength-very-strong').removeClass('hidden');

                isPasswordValid = true;
            }

            enableOrDisableSubmitButton()

        } else {
            $('#strength-very-low').addClass('hidden');
            $('#strength-low').addClass('hidden');
            $('#strength-medium').addClass('hidden');
            $('#strength-strong').addClass('hidden');
            $('#strength-very-strong').addClass('hidden');
        }

    });


    /*********************************/
    /*                               */
    /*     Password Confirmation     */
    /*                               */
    /*********************************/
    var isPasswordMathced = false;

    $('#input_password_confirm').on('keypress keydown keyup', function () {
        var provided_password = $('#input_password').val();

        if (provided_password.length > 0) {
            var current_password = $('#input_password_confirm').val();
            if (provided_password === current_password) {
                isPasswordMathced = true;
                $('#confirm_password_error').text("Match Confirmed");
                $('#validator_confirm_password_checklist #validator_option_match_password .msg').removeClass("text-muted");
                $('#validator_confirm_password_checklist #validator_option_match_password .msg').removeClass("text-danger");
                $('#validator_confirm_password_checklist #validator_option_match_password .msg').addClass("text-success");
                $('#validator_confirm_password_checklist #validator_option_match_password .times').addClass("hidden");
                $('#validator_confirm_password_checklist #validator_option_match_password .check').removeClass("hidden");

            } else {
                isPasswordMathced = false;
                $('#confirm_password_error').text("Your password must match with provided password")
            }

        } else {
            $('#confirm_password_error').text("You didn't enter password.");
            $('#validator_confirm_password_checklist #validator_option_match_password .msg').removeClass("text-muted");
            $('#validator_confirm_password_checklist #validator_option_match_password .msg').addClass("text-danger");
            $('#validator_confirm_password_checklist #validator_option_match_password .msg').removeClass("text-success");
            $('#validator_confirm_password_checklist #validator_option_match_password .times').removeClass("hidden");
            $('#validator_confirm_password_checklist #validator_option_match_password .check').addClass("hidden");
        }

        enableOrDisableSubmitButton();
    });


    /*********************************/
    /*                               */
    /*     RegNo Validation          */
    /*                               */
    /*********************************/

    var isBatchSelected = false;
    var isProgramSelected = false;
    var isNumberValid = false;

    $("#student_batch").change(function () {
        isBatchSelected = true;
        $('#validator_number_checklist #validator_option_valid_batch .msg').removeClass("text-muted");
        $('#validator_number_checklist #validator_option_valid_batch .msg').removeClass("text-danger");
        $('#validator_number_checklist #validator_option_valid_batch .msg').addClass("text-success");
        $('#validator_number_checklist #validator_option_valid_batch .times').addClass("hidden");
        $('#validator_number_checklist #validator_option_valid_batch .check').removeClass("hidden");
    });

    $("#student_program").change(function () {
        isProgramSelected = true;
        $('#validator_number_checklist #validator_option_valid_program .msg').removeClass("text-muted");
        $('#validator_number_checklist #validator_option_valid_program .msg').removeClass("text-danger");
        $('#validator_number_checklist #validator_option_valid_program .msg').addClass("text-success");
        $('#validator_number_checklist #validator_option_valid_program .times').addClass("hidden");
        $('#validator_number_checklist #validator_option_valid_program .check').removeClass("hidden");
    });

    $('#input_number').on('keypress keydown keyup', function () {

        var num = $(this).val();
        if (num.length == 3) {
            if (hasSpecialCharacter(num) || hasAlphabets(num))
                isNumberValid = false;
            else
                isNumberValid = true;

        } else {
            isNumberValid = false;
            $('#number_error').text("Number must be of 3 digits")
        }

        if (isNumberValid) {
            $('#validator_number_checklist #validator_option_valid_number .msg').removeClass("text-muted");
            $('#validator_number_checklist #validator_option_valid_number .msg').removeClass("text-danger");
            $('#validator_number_checklist #validator_option_valid_number .msg').addClass("text-success");
            $('#validator_number_checklist #validator_option_valid_number .times').addClass("hidden");
            $('#validator_number_checklist #validator_option_valid_number .check').removeClass("hidden");
        } else {
            $('#validator_number_checklist #validator_option_valid_number .msg').removeClass("text-muted");
            $('#validator_number_checklist #validator_option_valid_number .msg').addClass("text-danger");
            $('#validator_number_checklist #validator_option_valid_number .msg').removeClass("text-success");
            $('#validator_number_checklist #validator_option_valid_number .times').removeClass("hidden");
            $('#validator_number_checklist #validator_option_valid_number .check').addClass("hidden");
        }

        enableOrDisableSubmitButton();
    });



    /*********************************/
    /*                               */
    /*      Validation Method        */
    /*                               */
    /*********************************/
    function hasLowerCase(str) {
        return (/[a-z]/.test(str));
    }

    function hasUpperCase(str) {
        return (/[A-Z]/.test(str));
    }

    function hasAlphabets(str) {
        return (/[a-zA-Z ]/.test(str));
    }

    function hasDigit(str) {
        return (/[0-9]/.test(str));
    }

    function hasSpecialCharacter(str) {
        return (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>]/).test(str);
    }

    function isValidEmail(email) {
        return (/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/).test(email);
    }


    /**********************************************************************/
    /*                                                                    */
    /*      Enable/Disable Signup button based on right validation        */
    /*                                                                    */
    /**********************************************************************/
    function enableOrDisableSubmitButton() {

        if (isNameValid &&
            isEmailValid &&
            isPasswordValid &&
            isPasswordMathced) {

            if (isStudentSignup) {
                if (isBatchSelected &&
                    isProgramSelected &&
                    isNumberValid) {

                    buttonSubmit.prop('disabled', false);
                }
            } else {
                buttonSubmit.prop('disabled', false);
            }

        } else {
            buttonSubmit.prop('disabled', true);
        }

    }

    function setStudentSignup(stdSignup) {
        isStudentSignup = stdSignup;
    }

});
