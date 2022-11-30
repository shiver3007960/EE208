(function(){
    article = document.querySelector('.main');
    nav = document.querySelector('nav');
    outline = document.querySelector('div.J6UZg');

    end = document.querySelector('#rzG2be');
    var date = new Date()
    time = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
    end.setAttribute('placeholder', time);

    backslash = document.querySelector('div.J6UZg > div.Gwgzqd');
    backslash.onclick = function(){
        outline.style.display = 'none';
        article.style.opacity = '1';
        nav.style.opacity = '1';
    }
    
    entrance = document.querySelector('#HEMlW');

    entrance.onclick = function(){
        if (entrance.getAttribute('show-flag') == '0'){
            outline.style.display = 'inline-block';
            article.style.opacity = '0.25';
            nav.style.opacity = '0.25';
            entrance.setAttribute('show-flag', '1');
            console.log(1);
        }else{
            console.log(2);
            outline.style.display = 'none';
            entrance.setAttribute('show-flag', '0');
            article.style.opacity = '1';
            nav.style.opacity = '1';
        }
    }

    button = document.querySelector('#T3kYXe > button');
    form = button.parentElement;
    form.onsubmit = function(){
        /* First check the validity of the numbers */
        query = /(?<=q=)(?<query>.*)(?=&fn=)/.exec(String(location.href));
        fn = /(?<=&fn=)(?<fn>\d+)(?=$|&)/.exec(String(location.href));
        
        if(!query || !fn) return false;
        form.children[0].value = query.groups.query;
        form.children[1].value = parseInt(fn.groups.fn);
        dateCheck = /(?<=^)(?<year>\d{4}).{1}(?<month>\d{1,2}).{1}(?<date>\d{1,2})(?=$)/;
        res1 = dateCheck.exec(form.children[2].value);
        res2 = dateCheck.exec(form.children[3].value);
        
        if (!res1 || !res2) {alert("Please enter a invliad date"); return false;}
        if (parseInt(res1.groups.year) < 1800 || parseInt(res2.groups.year) < 1800 || parseInt(res1.groups.year) > parseInt(res2.groups.year) ||
            parseInt(res2.groups.month) > 12 || parseInt(res2.groups.month) < 1 || parseInt(res1.groups.month) > 12 || parseInt(res1.groups.month) < 1 || 
            parseInt(res2.groups.date) > 31 || parseInt(res2.groups.date) < 1 || parseInt(res1.groups.date) > 31 || parseInt(res1.groups.date) < 1 ) {alert("Please enter a invliad date"); return false;}

        if (parseInt(res2.groups.year) > date.getFullYear())
        {alert("We cannot predict the future ..."); return false;}
        else if(parseInt(res2.groups.year) == date.getFullYear())
        {if (parseInt(res2.groups.month) > date.getMonth() + 1)
            {alert("We cannot predict the future ..."); return false;}
        else if (parseInt(res2.groups.month) == date.getMonth() + 1){
            if (parseInt(res2.groups.date) > date.getDate())
        {alert("We cannot predict the future ..."); return false;}}}

        if (parseInt(res1.groups.year) == parseInt(res2.groups.year)){
            if (parseInt(res1.groups.month) > parseInt(res2.groups.month)){alert('The month of start date should be earlier'); return false;}
            else if (parseInt(res1.groups.month) == parseInt(res2.groups.month)){
                if (parseInt(res1.groups.date) > parseInt(res2.groups.date)) {alert('The date of start date should be earlier'); return false;}
            }
        }
        form.children[2].value = `${res1.groups.year}-${res1.groups.month}-${res1.groups.date}`;
        form.children[3].value = `${res2.groups.year}-${res2.groups.month}-${res2.groups.date}`;
        return true;
    }
})();

