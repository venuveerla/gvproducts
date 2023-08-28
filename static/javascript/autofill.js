document.getElementById('mobileno').addeventListener('onkeyup');
   let mobile=document.getElementById('mobileno');
    if(mobile.textContent.length()!=10)
    {
          mobile.style.backgroundColor=" red";
    }

