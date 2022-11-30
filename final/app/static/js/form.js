/* toolsBar about the timeRange and the precision of the query */ 
(function ToolBar(){

    toolsBar = document.querySelector("nav div.Navigationitem[data-vid='5']");
    extabar = document.querySelector('.main > article #extabar');
    tmp = extabar.children[1].children[0].children[0];
    gMenu = tmp.nextElementSibling.children[0];
    tmp2 = extabar.children[1].children[1].children[0];
    gMenu2 = tmp2.nextElementSibling.children[0];

    toolsBar.onclick = function(){
        
        var click = toolsBar.getAttribute('click-on');
        if (click == 1){
            extabar.children[0].style.display="block";
            extabar.children[1].style.display="none";
            toolsBar.setAttribute('click-on', 0);
        }
        else{
            extabar.children[0].style.display="none";
            extabar.children[1].style.display="flex";
            if (tmp2.getAttribute('jsaction') == 1){
                gMenu2.style.display = 'none';
                tmp2.setAttribute('jsaction', 0);
            }
            if (tmp.getAttribute('jsaction') == 1){
                gMenu.style.display = 'none';
                tmp.setAttribute('jsaction', 0);
            }
            toolsBar.setAttribute('click-on', 1);
        }
    }
    tmp.onclick = function(){
        if (tmp.getAttribute('jsaction') == 1){
            gMenu.style.display = 'none';
            tmp.setAttribute('jsaction', 0);
        }
        else{
            if (tmp2.getAttribute('jsaction') == 1){
                gMenu2.style.display = 'none';
                tmp2.setAttribute('jsaction', 0);
            }
            gMenu.style.display = 'block';
            tmp.setAttribute('jsaction', 1);
        }
    }

    tmp2.onclick = function(){
        if (tmp2.getAttribute('jsaction') == 1){
            gMenu2.style.display = 'none';
            tmp2.setAttribute('jsaction', 0);
        }
        else{
            if (tmp.getAttribute('jsaction') == 1){
                gMenu.style.display = 'none';
                tmp.setAttribute('jsaction', 0);
            }
            gMenu2.style.display = 'block';
            tmp2.setAttribute('jsaction', 1);
        }
    }
    /* Change the precision toolbar */
    g_item2 = gMenu2.children[parseInt(gMenu2.getAttribute('pre'))];

    /* 1. modify the innerHTML of the first presentation */
    timeText = String(g_item2.innerText).replace(/^\s\s*/, '').replace(/\s\s*$/, '');
    
    g_item2.parentElement.parentElement.previousElementSibling.children[0].children[0].innerText = timeText;
    /* 2. modify whichever is div to 'a' Tag */
    /* 3. modify the nodeType from 'a' Tag to div */
    var divindex = 0;
    var index = 0;
    for(let child of g_item2.parentElement.children){
        tar = child.children[0].children[0];
        if (tar.nodeName == 'DIV'){
            divindex = index;
            tar.parentElement.innerHTML = `<a href="#" aria-checked="false">${tar.innerText}</a>`;
        }
        index++;
    }
    /* divtar is the original being focused node, atar is the node to be focused */
    divtar = g_item2.parentElement.children[divindex];
    divtar.children[0].innerHTML = `<a href="#" aria-checked="false">${divtar.children[0].children[0].innerText}</a>`;
    g_item2.children[0].innerHTML = `<div class="y0fQ9c" aria-checked="true">${g_item2.children[0].children[0].innerText}</div>`;

    /* Change the freshness toolbar*/
    g_item = gMenu.children[gMenu.getAttribute('fresh')]
    /* 1. modify the innerHTML of the first presentation */
    if (gMenu.getAttribute('fresh') != '6'){
        timeText = String(g_item.innerText).replace(/^\s\s*/, '').replace(/\s\s*$/, '');
    }
    else{
        timeText = String(g_item.getAttribute('daterange')).replaceAll('_', ' ');
    }
    g_item.parentElement.parentElement.previousElementSibling.children[0].children[0].innerText = timeText;
    /* 2. modify whichever is div to 'a' Tag */
    /* 3. modify the nodeType from 'a' Tag to div */
    divindex = index = 0;
    for(let child of g_item.parentElement.children){
        tar = child.children[0].children[0];
        if (tar.nodeName == 'DIV'){
            divindex = index;
            tar.parentElement.innerHTML = `<a href="#" aria-checked="false">${tar.innerText}</a>`;
        }
        index++;
    }
    /* divtar is the original being focused node, atar is the node to be focused */
    divtar = g_item.parentElement.children[divindex];
    divtar.children[0].innerHTML = `<a href="#" aria-checked="false">${divtar.children[0].children[0].innerText}</a>`;
    g_item.children[0].innerHTML = `<div class="y0fQ9c" aria-checked="true">${g_item.children[0].children[0].innerText}</div>`;

    for (let g_item of document.querySelectorAll('.main > article #tn_1 div.EwsJzb g-menu-item')){
        
        g_item.onclick = function(event){
            event.preventDefault();
            if (g_item.children[0].children[0].nodeName != 'DIV'){
                
                /* redirectURL */
                newl = String(location.href).replace(RegExp('&fresh=[0-9]'),'').replace(RegExp('&pre=[0-9]'), '').replace(/&start=.*?end=.*?(?=($|&))/,'');
                /* If the g_item belongs to the precision section */
                if (g_item.parentElement.getAttribute('class') == 'cF4c'){
                    location.replace(`${newl}&pre=${g_item.getAttribute('rank')}`);
                    return;
                }
                console.log(`${newl}&fresh=${g_item.getAttribute('rank')}`);
                location.replace(`${newl}&fresh=${g_item.getAttribute('rank')}`);
                return;
            }
        }
    }
})();
/* websitesetting button handling */
/* 1. website setting pop out */
for(let webcha of document.querySelectorAll('.main > article .searchResult .websitesetting button')){
    webcha.onclick = function(){
        webmod = webcha.nextElementSibling;
        if (webmod.style.display=='flex'){
            webmod.style.display='none';
        }
        else{
            webmod.style.display='flex';
        }
    }
};
/* 2. websitesetting modifiacion */
function websetMod(){
    for (let mod1 of document.querySelectorAll(".main > article .searchResult .websitesetting .webchange ul > li[vid='0']")){
        mod1.onclick = function(){
            ul = mod1.parentElement;
            ul.style.display = 'none';
            prev = ul.previousElementSibling;
            prev.children[0].children[0].innerText = 'We will recommend it less';
            prev.style.display = 'flex';
            setTimeout(function(){prev.style.display = 'none'; ul.parentElement.style.display = 'none'; ul.style.display = 'flex';}, 1000);
        }
    }

    for(let mod2 of document.querySelectorAll(".main > article .searchResult .websitesetting .webchange ul > li[vid='1']")){
        mod2.onclick = function(){
            ul = mod2.parentElement;
            ul.style.display = 'none';
            prev = ul.previousElementSibling;
            prev.children[0].style.height = '40%';
            prev.children[0].children[0].innerText = 'Ready to give your more \n refreshing experience!';
            prev.style.display = 'flex';
            setTimeout(function(){prev.children[0].style.height = '20%'; prev.style.display = 'none'; ul.parentElement.style.display = 'none'; ul.style.display = 'flex';}, 1000);
        }
    }

    for(let mod3 of document.querySelectorAll(".main > article .searchResult .websitesetting .webchange ul > li[vid='2']")){
        mod3.onclick = function(){
            ul = mod3.parentElement;
            ul.style.display = 'none';
            prev = ul.previousElementSibling;
            prev.children[0].style.height = '40%';
            prev.children[0].children[0].innerText = 'We will go over this\n content soon';
            prev.style.display = 'flex';
            setTimeout(function(){prev.children[0].style.height = '20%'; prev.style.display = 'none'; ul.parentElement.style.display = 'none'; ul.style.display = 'flex';}, 1000);
        }
    }
}
websetMod();

function searchhistory(){
    /* searchhistory pop out */
    /* the signal whether searchHistory should be shown is in the header .before-half-radius 's attribute named "show-flag"*/
    before_half_radius = document.querySelector('header .before-half-radius');

    closeHistory = document.querySelector('header .searchHistoryItems li[role="closure"]');
    closeHistory.onclick = function(){
        before_half_radius.setAttribute('show-flag', 0);
        searchH = document.querySelector('ul.searchHistoryItems');
        searchH.style.display = 'none';
        before_half_radius.style.borderBottomLeftRadius = '22px';
        rear_half_radius = document.querySelector('header .rear-half-radius');
        rear_half_radius.style.borderBottomRightRadius = '22px';
    }
    /* searchHistory representation */
    inputQuery = document.querySelector('header div.searchInput input.searchQuery');

    rear_half_radius = document.querySelector('header .rear-half-radius');
    searchH = document.querySelector('ul.searchHistoryItems');
    inputQuery.onclick = function(){
        if (before_half_radius.getAttribute('show-flag') == 1){
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
}

searchhistory();

/* backslash in the query box*/
backslash = document.querySelector('header .searchPart> .backslash');
backslash.onclick = function(){
    console.log("i ma here");
    backslash.previousElementSibling.firstElementChild.value = '';
}
/* backslash in the related search*/
relatedSearch = document.querySelectorAll('article .relatedSearch .relatedsearch');
for (let i = 0; i < relatedSearch.length; i++){
    svg = relatedSearch[i].children[2].firstElementChild.firstElementChild.firstElementChild;
    svg.onclick = function(){
        let index = parseInt(relatedSearch[i].getAttribute('data-backslash'));
        while(index < relatedSearch.length-1){
            relatedSearch[index+1].setAttribute('data-backslash', String(index));
            index++;
        }
        relatedSearch[i].style.display = "none";
    }
}
/* website setting in the article*/
websitesetting = document.querySelector('.main > article .searchResult .websitesetting');
websitesetting.onclick = function(){
    /* pop out the websitesetting */
}


/* navigation table display*/
    /* param = location.search;
    regex = /&pn=(?<page_number>[\d]+)[&$]/;
    pageNumber = regex.exec(param).groups.page_number; */


/* 
navigationitem = document.querySelector(`nav .Navigationitem[data-vid="${pageNumber}"]`);
navigationitem.firstElementChild.onclick = function(event){
    return stopDefault(event);
}

for (let navigationitem of document.querySelectorAll('nav .Navigationitem[data-vid]')){
    navigationitem.firstElementChild.firstElementChild.style.color = "#4285F4";
    if (navigationitem.getAttribute('data-vid') == pageNumber){
        navigationitem.firstElementChild.firstElementChild.style.color = "black";
    }
}
 */
/* maintain the mainContent banner*/
mainContents = document.querySelectorAll('article div.searchResult div.searchResultformat div.contentgeneral div.mainContent span')
for (let mainContent of mainContents){
    if (mainContent.innerText){
        text = mainContent.innerText;
        mainContent.innerText = '';
        mainContent.innerHTML = text;
    }
}

