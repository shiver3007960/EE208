
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