/* get navigator item*/
innerheight = window.innerHeight;
innerwidth = window.innerWidth;


/* Let the picture items 'justify-contents:flex-start' */
picFrames = document.querySelector('.main > article div.picturePool div.picFrame');
picFrames.style.width = `${innerwidth}px`;

/* Let the navigation bar scroll*/
navigationBar = document.querySelector('nav .NavigationBar');
navigationBar.style.width = `${innerwidth}px`;

piCs = document.querySelectorAll('.main div.picFrame div.picItem div.picSrc img');
let prev = 0;
let index = 0;
let vector = Array();
while(index < piCs.length){
    
    piCs[index].style.width = `${piCs[index].naturalWidth * 180 / piCs[index].naturalHeight}px`;
    vector.push(piCs[index].naturalWidth * 180 / piCs[index].naturalHeight);
    piCs[index].parentElement.parentElement.parentElement.style.width = piCs[index].style.width;
    
    index += 1;
    let gap = 0;
    if (sum(vector) > innerwidth){
        regex = /(?<pixel>[\d\.]+)px/;
        let lastElement = parseInt(regex.exec(piCs[index-1].style.width).groups.pixel);
        inner = sum(vector) - lastElement;
        let gap = (innerwidth - inner) / (index - prev) / 2;
        if (gap < 10){
            let prevElement = parseInt(regex.exec(piCs[index-2].style.width).groups.pixel);
            gap = (innerwidth - inner + prevElement) / (index - prev - 1) / 2;
            console.log(piCs[index-2].style.width);
            index -= 1;
        }
        else if (gap > 25){
            /* too many vacancies that we should rearrange */
            /* Not implemented*/
        }
        for (let i = prev; i < index; i++){
            piCs[i].parentElement.parentElement.parentElement.style.marginLeft = `${gap}px`;
            piCs[i].parentElement.parentElement.parentElement.style.marginRight = `${gap}px`;
        }
        index -= 1;
        prev = index;
        vector = Array();
    }
    
    
}


function sum(Arr){
    return Arr.reduce(function(prev, curr, idx, arr){
        return prev + curr;
    });
}
