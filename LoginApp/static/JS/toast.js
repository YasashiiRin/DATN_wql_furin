function toast({
    title = '',
    content = '',
    typeicon = 'Success',
    duration = 4000
}) {
    const main = $('#tagtoast');
    const icons = {
        success: "fa-solid fa-circle-check",
        error: "fa-solid fa-circle-exclamation"
    }
    const delay = (duration / 1000).toFixed(2);
    const icon = icons[typeicon];
    if (main) {
        const toast = document.createElement('div');
        toast.classList.add('toast', `toast--${typeicon}`);
        toast.style.animation = `slidetoast ease 1s, opc linear 1s ${delay}s forwards`;
        toast.innerHTML = `
          
            <div class="toast-icon toast_icon-success">
                  <i class="${icon}"></i>
             </div>
            <div class="toast-body">
                  <h3 class="title">
                            ${title}
                         </h3>
                  <p class="conten">
                     ${content}
                  </p>

            </div>
           <div class="toast-exit">
             <i class="fa-solid fa-xmark"></i>
         </div>
   
          `;
        main.appendChild(toast);
        setTimeout(function() {
            main.removeChild(toast);
        }, duration)
    }
}

  