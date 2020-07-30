$(function() {
    console.log("loaded");
    $('.floppy-green').parent().prop('title','Bookmark this product')
    $('.floppy-red').parent().prop('title','Already Bookmarked');

    $('.floppy-green').click(function(e){
        $(this).removeClass('floppy-green')
        $(this).addClass('floppy-red')
        $(this).parent().prop('title','Already Bookmarked');
        var barcodes = this.id;
        var data = {};
        var pos = barcodes.indexOf("-");
        var subst_barcode=barcodes.substr(0,pos);
        var prod_barcode=barcodes.substr(pos+1);
        data['subst'] = subst_barcode;
        data['prod'] = prod_barcode;
        data = JSON.stringify(data);
        SendAjax('POST','save_bookmark/',data)
            .done( function(response) {
                $(this).prop('title','Already saved as Bookmark');

            })
            .fail( function(response) {
                console.error("Erreur Ajax : " + response.data);
                $(this).css('color','red');
                alert("Erreur Ajax - "+ response.data);
            });
    });
});

var SendAjax = function(type=post ,url, data, datatype='json', contenttype='application/json' ){
    /*
    Send ajax request to server 
    */
    return $.ajax({
        type: type,
        url: url,
        data: data,
        dataType: datatype,
        contentType: contenttype,
    })
}; 