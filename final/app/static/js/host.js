
/* searchhistory pop out */
/* the signal whether searchHistory should be shown is in the header .before-half-radius 's attribute named "show-flag"*/
(function searchHistoryPopOut(){
    before_half_radius = document.querySelector('.main > article .before-half-radius');

    closeHistory = document.querySelector('.main > article .searchHistoryItems li[role="closure"]');
    closeHistory.onclick = function(){
        before_half_radius.setAttribute('show-flag', 0);
        searchH = document.querySelector('.main > article ul.searchHistoryItems');
        searchH.style.display = 'none';
        before_half_radius.style.borderBottomLeftRadius = '22px';
        rear_half_radius = document.querySelector('.main > article .rear-half-radius');
        rear_half_radius.style.borderBottomRightRadius = '22px';
    }

    inputQuery = document.querySelector('.searchPart > .searchInput');

    rear_half_radius = document.querySelector('.main > article .rear-half-radius');
    searchH = document.querySelector('.main > article ul.searchHistoryItems');
    inputQuery.onclick = function(event){
        if (before_half_radius.getAttribute('show-flag') == 1){
            console.log(event);
            event.preventDefault();
            if (inputQuery.getAttribute('historyOn') == '1'){
                before_half_radius.style.borderBottomLeftRadius = '22px';
                searchH.style.display = "none";
                rear_half_radius.style.borderBottomRightRadius = '22px';
                inputQuery.setAttribute('historyOn','0');
            }
            else{
                before_half_radius.style.borderBottomLeftRadius = '0px';
                searchH.style.display = "flex";
                rear_half_radius.style.borderBottomRightRadius = '0px';
                inputQuery.setAttribute('historyOn','1');
            }
        }
    }
})();




/* prompt bar:google apps */
(function (){
    promptbarleft = document.querySelector('header .headercontainer .settingsBarpic');
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
})();

(function(){
    /* backslash in the query box*/
    backslash = document.querySelector('article .queryBox .backslash');
    backslash.onclick = function(){
        backslash.previousElementSibling.firstElementChild.value = '';
    }
})();

/* shortcut setting button*/
(function (){
    for(let shortcutsetting of document.querySelectorAll('.main > article .shortcutitem .shortcutsetting button')){
        href = shortcutsetting.parentElement;
        console.log(href);
        
        href.onclick = function(event){
            event.preventDefault();
        }

        shortcutsetting.onclick = function(event){
            console.log(event);
            if (shortcutsetting.getAttribute('show-flag') == '0'){
                shortcutsetting.parentElement.children[1].style.display = 'inline-block';
                shortcutsetting.setAttribute('show-flag', '1');
            }
            else{
                shortcutsetting.parentElement.children[1].style.display = 'none';
                shortcutsetting.setAttribute('show-flag', '0');
            }
            edit = shortcutsetting.parentElement.children[1].children[0];
            remove = shortcutsetting.parentElement.children[1].children[1];
            edit.onclick = function(){
                shortcutsetting.parentElement.children[1].style.display = 'none';
                shortcutsetting.setAttribute('show-flag', '0');
                
                var name = window.prompt("please enter the new name", "");
                shortcutsetting.parentElement.parentElement.children[2].firstElementChild.innerHTML = name;
                
            }
            remove.onclick = function(){
                shortcutsetting.parentElement.parentElement.parentElement.style.display = 'none';
            }
            /* pop up the window */
        }
    }
})()


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