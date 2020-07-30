$(function() {
    console.log("loaded !!");
    $(".helptext").css("opacity","0.5");
    $(".btn_connexion").on('click',function(){
        $("#id_connexion_creation").val("connexion")
    });
    $(".btn_register").on('click',function(){
        $("#id_connexion_creation").val("register")
    });
});