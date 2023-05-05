$(document).ready(function() {
    
    "use strict";
    
    $('.contact-list .table tbody td').on('click', function(e) {
        $('#contact-info').modal('show');
    });
            
    $('.contact-list .table tbody th').on('click', function(e) {
        if(e.target == this){ 
            $(this).find('input').click();
        }
    });
            
    $('.contact-list .table thead th input').on('change', evt =>  {
        if($(evt.target).is(':checked')) {
            $('.contact-list table tbody th input:not(:checked)').click();
        } else {
            $('.contact-list table tbody th input:checked').click();
        }
    });   
});