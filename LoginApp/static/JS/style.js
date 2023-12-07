
const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);
var formIn = $('.container-FormIn');
var signupbt = document.querySelectorAll('.form-info .btn')[1];
var formItem = formIn.querySelectorAll('.form-item');
var checkform = '#form2';
var loginbt = $('.form-info .btn');
// on log
// signupbt.onclick = function (e) {
//     formItem[1].classList.remove('active');
//     formItem[0].classList.add('active');
//     formIn.classList.remove("log");
//     formIn.classList.add("regis");
// }
// // on register
// var loginbt = $('.form-info .btn');
// loginbt.onclick = () => {
//     formItem[0].classList.remove('active');
//     formItem[1].classList.add('active');
//     formIn.classList.remove("regis");
//     formIn.classList.add("log")
// }
const slide = {
    onslideright: function () {
        signupbt.onclick = function (e) {
            formItem[1].classList.remove('active');
            formItem[0].classList.add('active');
            formIn.classList.remove("log");
            formIn.classList.add("regis");
        }
    },
    onslideleft: function () {
        loginbt.onclick = () => {
            formItem[0].classList.remove('active');
            formItem[1].classList.add('active');
            formIn.classList.remove("regis");
            formIn.classList.add("log")
        }

    },
    runn: function () {
        this.onslideleft();
        this.onslideright();
    }
}
slide.runn();