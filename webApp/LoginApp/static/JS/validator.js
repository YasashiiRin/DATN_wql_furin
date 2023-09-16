
function validator(options) {
    function getparent(element, selector) {
        while (element.parentElement) {
            if (element.parentElement.matches(selector)) {
                return element.parentElement;
            }
            element = element.parentElement;
        }
    }
    var selectorOBJ = {}
    function valida(inputElement, element) {
        var NotifyEmail = element.test(inputElement.value);
        var MessageNotify;
        var errElement = getparent(inputElement, options.formGroup).querySelector(options.errSelector);
        // lấy ra rules đang blur
        var ru = selectorOBJ[element.selector];
        for (var i = 0; i < ru.length; ++i) {
            switch (inputElement.type) {
                case 'radio':
                case 'checkbox':
                    MessageNotify = ru[i](
                        formElement.querySelector(element.selector + ':checked')
                    );

                    break;
                default:
                    MessageNotify = ru[i](inputElement.value);
            }

            if (MessageNotify) break;
        }
        if (MessageNotify) {
            errElement.innerHTML = MessageNotify;
            getparent(inputElement, options.formGroup).classList.add('invalid');
            document.querySelector(element.selector).classList.add('invalid');
            document.querySelector(element.selector).classList.remove('valid');
        } else {
            errElement.innerHTML = '';
            getparent(inputElement, options.formGroup).classList.remove('invalid');
            document.querySelector(element.selector).classList.remove('invalid');
            document.querySelector(element.selector).classList.add('valid');
        }
        console.log(!MessageNotify);
        return !MessageNotify;


    }
    var formElement = document.querySelector(options.form);
    if (formElement) {
        formElement.onsubmit = function (e) {
            e.preventDefault();
            var isFormValid = true;
            //for rules
            options.rules.forEach(element => {
                var inputElement = formElement.querySelector(element.selector)
                console.log(inputElement)
                var isvalid = valida(inputElement, element);
                if (!isvalid) {
                    isFormValid = false;
                }
            });
            if (isFormValid) {
                formElement.submit();
                // if (typeof options.onsubmit === 'function') {
                //     var enableinput = formElement.querySelectorAll('[name]')
                //     var formvalue = Array.from(enableinput).reduce(function (values, input) {

                //         switch (input.type) {
                //             case 'radio':
                //                 values[input.name] = formElement.querySelector('input[name="' + input.name + '"]:checked').value;
                //                 break;
                //             case 'checkbox':

                //                 if (!Array.isArray(values[input.name])) {
                //                     values[input.name] = [];
                //                 }
                //                 if (input.matches(':checked')) {
                //                     values[input.name].push(input.value);
                //                     return values;
                //                 }
                //                 if (values[input.name].length === 0) {
                //                     values[input.name] = '';
                //                 }
                //                 break;
                //             case 'file':
                //                 values[input.name] = input.files;
                //                 break;
                //             default:
                //                 values[input.name] = input.value;

                //         }
                //         return values;
                //     }, {})
                //     options.onsubmit(formvalue);
                // }

            } else {
                console.log("co loi");
            }
        }
    }
    options.rules.forEach(element => {

        if (Array.isArray(selectorOBJ[element.selector])) {
            selectorOBJ[element.selector].push(element.test);
        } else {
            selectorOBJ[element.selector] = [element.test]
        }
        var inputElements = formElement.querySelectorAll(element.selector);
        Array.from(inputElements).forEach(function (inputElement) {
            inputElement.onblur = () => {
                valida(inputElement, element);
            }
            //handling on input change 
            inputElement.oninput = function () {
                //remove notify error
                var errElement = getparent(inputElement, options.formGroup).querySelector(options.errSelector);
                errElement.innerHTML = '';
                getparent(inputElement, options.formGroup).classList.remove('invalid');
                document.querySelector(element.selector).classList.remove('invalid');
            }
        });
    });

}
validator.isRequired = function (selector, message) {
    return {
        selector: selector,
        test: function (value) {
            return value ? undefined : message || 'vui long nhap truong nay'
        }
    }
}
validator.isEmail = function (selector) {
    return {
        selector: selector,
        test: function (inputText) {
            if (inputText == '') {
                return inputText.trim() ? undefined : 'vui long nhap truong nay';

            } else {
                var regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
                return regex.test(inputText) ? undefined : 'email khong hop le';
            }

        }
    }
}
validator.minlength = function (selector, min) {
    return {
        selector: selector,
        test: function (inputText) {
            return inputText.length >= min ? undefined : `vui longf nhap toi thieu ${min} ky tu `
        }
    }
}
validator.isconfirmvalue = function (selector, callback, message) {
    return {
        selector: selector,
        test: function (value) {
            return value === callback() ? undefined : message || 'password khong giong';
        }
    }
}