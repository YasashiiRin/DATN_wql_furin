
const form_text= document.querySelectorAll(".main__cta__card");
const conten= document.querySelectorAll(".main__cta__text");
const containBg = document.querySelector('#main__cta');
console.log(form_text)
console.log(conten)
const changaeContent ={
    // giao diện mặc định 
    clickTitle1: function (){
        form_text[0].onclick = function (){
            containBg.style.backgroundImage= "url('/static/images/bg10.jpg')";
            conten[0].classList.add("active");
            conten[1].classList.remove("active");
        }
    },
    clickTitle2: function (){
        // giao diện chuyển đổi 
        form_text[2].onclick= function (){
            containBg.style.backgroundImage = "url('/static/images/bg15.jpg')";
            conten[0].classList.remove("active");
            conten[1].classList.add("active");
        } 
    },
    run:function(){
        this.clickTitle1();
        this.clickTitle2();
    }
}
changaeContent.run();

const tabitem = document.querySelectorAll('.tab-item');
const act = document.querySelector('.main__cta__card.tab-item.active');
const line = document.querySelector('.split .main__cta__options .line');
const containLine = document.querySelector('.split .main__cta__options');
line.style.left = act.offsetLeft + 'px';
line.style.width = act.offsetWidth + 'px';
console.log(containLine)
console.log(tabitem)
console.log([act])
tabitem.forEach((element, index) => {
    element.onmouseover = function () {
        line.style.opacity='1';
        document.querySelector('.tab-item.active').classList.remove('active');

        line.style.left = this.offsetLeft + 'px';
        line.style.width = this.offsetWidth + 'px';
        this.classList.add('active');


    }
})
containLine.onmouseleave = function (){
        line.style.opacity = '0';
}
