let i=0;
var clk;
let alter=0;
a=['a1','a2','a3','a4'];
function display(){
    const c=document.getElementsByClassName(a[i]);
    c[0].style.display="block";
    const cl=document.getElementsByClassName('cb')[1];
    cl.innerHTML="&#9616;&#9616;";
    clk=setInterval(function(){
        if(i==0)
        document.getElementsByClassName(a[3])[0].style.display='none';
        else
        document.getElementsByClassName(a[i-1])[0].style.display='none';
        document.getElementsByClassName(a[i])[0].style.display="block";
        i=((i+1)%4);
    },2000
)
}
function condition(){
    if(alter==0){
        alter=1;
        stop();
    }else{
        alter=0;
        display();
    }
}
function stop(){
    const cl=document.getElementsByClassName('cb')[1];
    cl.innerHTML="&#9654;";
    clearInterval(clk);
}
function moveleft(){
    if(i==0)
    i=3;
    else
    i=i-1;
    document.getElementsByClassName(a[i])[0].style.display="none";
    if(i==0)
    i=3;
    else
    i=i-1;
    document.getElementsByClassName(a[i])[0].style.display="block";
    i=((i+1)%4);
}
function moveright(){
    const c=document.getElementsByClassName('indi');
    let j;
    if(i==0)
    j=3;
    else
    j=i-1;
    document.getElementsByClassName(a[j])[0].style.display="none";
    document.getElementsByClassName(a[i])[0].style.display="block";
    i=((i+1)%4);
}
function signin_direct(e){
    const c=document.getElementsByClassName('main')[0];
    const d=document.getElementsByClassName('blurbg')[0];
    if(e==0){
        d.style.display='block';
        c.style.filter='blur(2px)';
    }else{
        d.style.display='none';
        c.style.filter='none';
    }
}
let display_id=0;
function display_user_details(){
        const ele=document.getElementsByClassName("user_details")[0];
        if(display_id==0){
            ele.style.display="block";
            display_id=1;
        }else{
            ele.style.display="none";
            display_id=0;
        }
    }
