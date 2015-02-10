$('div.trigger').click(function() {
    $(this).find('div.popup').toggle()
});
/*
function set_tab(str){
    $("div.tab").hide();
    $("div."+$.trim(str)).show();
    $("ul.nav-tabs > li.active").removeClass("active")
    $("ul.nav-tabs > li."+$.trim(str)).addClass("active")
}

set_tab("STAGE");
*/
