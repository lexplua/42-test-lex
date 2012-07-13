$(document).ready(function(){

    $.ajaxSetup({
        beforeSend: function (request) {
            request.setRequestHeader('Accept', 'application/html+ajax');
            request.setRequestHeader('X_REQUESTED_WITH', 'XMLHttpRequest');
        }
    });
    $("#edit_form").ajaxForm({
        beforeSubmit: function(arr, $form, options) {
            $('input').prop('readonly','readonly');
            $('textarea').prop('readonly','readonly');
            $('#loading').css('visibility','visible');
            $('input').next().html('');
            $('textarea').next().html('');
            $('input').parent().parent().removeClass('error');
            $('textarea').parent().parent().removeClass('error');
        },
        success:function(data){
            $('input').prop('readonly','');
            $('textarea').prop('readonly','');
            $('#loading').css('visibility','hidden');
            var model = data[0];
            if ('fields' in model)
                $.each(model['fields'],
                    function(key,value){
                        if(key!='photo')
                            $('#id_'+key).prop('value',value);
                        else{
                            $('#prev_image').prop('src','/media/'+value);
                        }
                    }
                );
            if ('errors' in model)
                $.each(model['errors'],
                    function(key,value){
                        if(key[0]!='photo'){
                            $('#id_'+key).next().html(value[0]);
                            $('#id_'+key).parent().parent().addClass('error');
                        }

                    }
                );
        }

    });
    $('#id_date_of_birth').datepicker({ dateFormat: "dd.mm.yy" });
});