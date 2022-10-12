/* prompt bar:google apps */
promptbarleft = document.querySelector('header .headercontainer .settingsBarpic')
promptbarleft.onmouseover=function(){
    promptbarleft.parentElement.parentElement.parentElement.nextElementSibling.style.display = 'flex';
}
promptbarleft.onmouseout=function(){
    promptbarleft.parentElement.parentElement.parentElement.nextElementSibling.style.display = 'none';
}
/* prompt bar:account*/
promptbarright = document.querySelector('header .headercontainer .settingsBaraccount')
promptbarright.onmouseover=function(){
    target = promptbarright.parentElement.parentElement.parentElement.nextElementSibling.nextElementSibling;
    target.style.display="flex";

}
promptbarright.onmouseout=function(){
    promptbarright.parentElement.parentElement.parentElement.nextElementSibling.nextElementSibling.style.display = 'none';
}
/* backslash in the query box*/
backslash = document.querySelector('article .queryBox .backslash');
backslash.onclick = function(){
    backslash.previousElementSibling.firstElementChild.value = '';
}
/* shortcut setting button*/
shortcutsetting = document.querySelector('.main > article .shortcutitem .shortcutsetting button')
shortcutsetting.onclick = function(){
    href = shortcutsetting.parentElement.parentElement;
    href.onclick = (function(event){
        stopDefault(event);
    })();
    /* pop up the window */
}

/* backgroung image changing */
bgim =  document.querySelector('body iframe');
function changeBackground(element, maxSize){
    bgimURL = element.style.backgroundImage;
    regex = /wallpaper\.(?<num>[\d]+?)\.jpg/;
    index = parseInt(regex.exec(bgimURL).groups.num);
    if (index < maxSize){
        index += 1;
    }
    else{
        index = 0;
    }
    path = `url(../static/image/pexels-wallpaper/wallpaper.${index}.jpg)`;
    element.style.backgroundImage = path;
}
timer = setInterval(changeBackground, 1000*300, bgim, 9);

/* remove Event Listener*/
function removeEventListener(element, event, fnName){
    if (element.removeEventListener){
        element.removeEventListener(event, fnName, false);
    }else if(element.detachEvent){
        element.detachEvent("on" + event, fnName);
    }else{
        element["on" + event] = null;
    }
}
/* add event listener*/
function addEventListener(element, event, fnName){
    if (element.addEventListener){
        element.addEventListener(event, fnName, false);
    }else if(element.attachEvent){
        element.attachEvent("on" + event, fnName);
    }else{
        element["on" + event] = null;
    }
}

/* stop Default event */
function stopDefault(event){
    if (event && event.preventDefault){
        event.preventDefault;
    }else{
        window.event.returnValue = false;
    }
    return false;
}