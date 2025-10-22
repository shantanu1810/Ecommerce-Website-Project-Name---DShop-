function account(d){
    if(d==0){
        document.getElementsByClassName('personala')[0].style.display="flex";
        document.getElementsByClassName('personalb')[0].style.display="none";
        document.getElementsByClassName('paccount')[0].style.background="rgb(196, 195, 195)";
        document.getElementsByClassName('baccount')[0].style.background="white";
    }else{
        document.getElementsByClassName('personala')[0].style.display="none";
        document.getElementsByClassName('personalb')[0].style.display="flex";
        document.getElementsByClassName('paccount')[0].style.background="white";
        document.getElementsByClassName('baccount')[0].style.background="rgb(196, 195, 195)";
    }
}