let innerheight = window.innerHeight;
let innerwidth = window.innerWidth;

navigationBar = document.querySelector('nav .NavigationBar');
navigationBar.style.width = String(innerwidth);

/* Navigation pop out */

for (let navigationMain of document.querySelectorAll('nav div.Navigationitem')){
    navigationMain.onmouseover = function(){
        navigationMain.style.backgroundColor = 'gainsboro';
        navigationMain.firstElementChild.firstElementChild.nextElementSibling.style.opacity = '1';
    }
    navigationMain.onmouseout = function(){
        navigationMain.style.backgroundColor = 'transparent';
        navigationMain.firstElementChild.firstElementChild.nextElementSibling.style.opacity = '0.01'
    }
}

/* Maintain the newsContent bar*/
newsContents = document.querySelectorAll('div.searchResultgeneral div.searchResultformat div.contentgeneral div.mainContent span') 
for (let newsContent of newsContents){
    if (newsContent.innerText){
        text = newsContent.innerText;
        newsContent.innerText = ''
        newsContent.innerHTML = text;
    }
}