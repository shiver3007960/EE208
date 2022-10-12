/* backslash in the query box*/
backslash = document.querySelector('header .searchPart> .backslash');
backslash.onclick = function(){
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

