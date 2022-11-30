/* get navigator item*/
innerheight = window.innerHeight;
innerwidth = window.innerWidth;

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


inputQuery = document.querySelector('header div.searchInput input.searchQuery');

rear_half_radius = document.querySelector('header .rear-half-radius');
searchH = document.querySelector('ul.searchHistoryItems');
var logoLeft = document.querySelector('header .logo').style.left;
console.log(logoLeft);
inputQuery.onclick = function(event){
    if (before_half_radius.getAttribute('show-flag') == 1){
        
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

/* Let the picture items 'justify-contents:flex-start' */
picFrames = document.querySelector('.main > article div.picturePool div.picFrame');
picFrames.style.width = `${innerwidth}px`;

/* Let the navigation bar scroll*/
navigationBar = document.querySelector('nav .NavigationBar');
navigationBar.style.width = `${innerwidth}px`;

/* Arrange the picture items */
(function pictureArrange(){

    piCs = document.querySelectorAll('.main div.picFrame div.picItem div.picSrc img');
    let prev = 0;
    let index = 0;
    let vector = Array();
    while(index < piCs.length){
        
        var width = piCs[index].naturalWidth * 180 / piCs[index].naturalHeight;
        piCs[index].style.width = `${width}px`;
        vector.push(width);
        piCs[index].parentElement.parentElement.parentElement.style.width = piCs[index].style.width;
        
        index += 1;
        let gap = 0;
        if (sum(vector) > innerwidth){
            regex = /(?<pixel>[\d\.]+)px/;
            let lastElement = parseInt(regex.exec(piCs[index-1].style.width).groups.pixel);
            inner = sum(vector) - lastElement;
            gap = (innerwidth - inner) / (index - prev) / 2;

            
            if (gap < 10 || gap > 25){
                let minIndex = prev, min = parseInt(regex.exec(piCs[prev].style.width).groups.pixel);
                
                for(let i = prev; i < index - 1; i++){
                    let value = parseInt(regex.exec(piCs[i].style.width).groups.pixel);
                    if (value < min){
                        min = value;
                        minIndex = i;
                    }
                }
                if(minIndex != index - 2){
                    let latter = piCs[index-2].parentElement.parentElement.parentElement; // The element node to be preserved
                    let front = piCs[minIndex].parentElement.parentElement.parentElement; // The element node to be removed
                    front.parentElement.children[index-2] = front;
                    front.parentElement.children[minIndex] = latter;
                }
                if (gap < 10){
                    let prevElement = parseInt(regex.exec(piCs[index-2].style.width).groups.pixel);
                    gap = (innerwidth - inner + prevElement) / (index - prev - 1) / 2;
                    index -= 1;
                }
                else{
                    /* too many vacancies that we should rearrange */
                    /* Not implemented */

                    f = parseInt(regex.exec(piCs[index-2].style.width).groups.pixel);
                    l = parseInt(regex.exec(piCs[index-1].style.width).groups.pixel);
                    console.log(`f is ${f}, l is ${l}`);
                    if (f < l){
                        let front = piCs[index-2].parentElement.parentElement.parentElement; // The element node to be preserved
                        let latter = piCs[index-1].parentElement.parentElement.parentElement; // The element node to be removed
                        
                        console.log(`gap before is ${gap}`);
                        front.parentElement.children[index-2] = latter;
                        front.parentElement.children[index-1] = front;
                        gap = (innerwidth - inner + f - l) / (index - prev) / 2;
                        console.log(`gap after is ${gap}`);
                    }
                    
                }
            }
            for (let i = prev; i < index - 1; i++){
                piCs[i].parentElement.parentElement.parentElement.style.marginLeft = `${gap}px`;
                piCs[i].parentElement.parentElement.parentElement.style.marginRight = `${gap}px`;
            }
            index -= 1;
            prev = index;
            vector = Array();
        }
        
        
    }
})();


function sum(Arr){
    return Arr.reduce(function(prev, curr, idx, arr){
        return prev + curr;
    });
}
