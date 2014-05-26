/**
 * Created by leonardo on 5/14/14.
 */
// Función general para aumentar contador de orden para el campo de tipo suministrado
function sumar(target, type, total){
    var value = target.val();
    if (!isNaN(value) && value < total) {
        if (total > 1){
            ++value;
            $('.orden-'+type).each(function(){
                if ($(this).val() == value){
                    $(this).val(value-1);
                }
            })
        }
    }
    target.val(value);
}

// Función general para reducir contador de orden para el campo de tipo suministrado
function restar(target, type, total){
    var value = target.val();
    if (!isNaN(value) && value > 1) {
        if (total > 1){
            --value;
            $('.orden-'+type).each(function(){
                if ($(this).val() == value){
                    $(this).val(value+1);
                }
            })
        }
    }
    target.val(value);
}

function agregarFormset(select_options) {
   /*var options = [
        {% for tipo_pago in tipos_pago %}
            {
                label: {{tipo_pago}},
                value: {{tipo_pago.id}}

            },
        {% endfor %}
   ]*/
    var total = parseInt($('#id_form-TOTAL_FORMS').val(), 10);
   var $div = $('<div/>');
   $('<label/>', {
       class: "control-label",
       text: "Tipo Pago"
   }).appendTo($div)
   var select = $('<select/>', {

        id: 'id_form-'+total+'-tipo_pago',
        name: 'form-'+total+'-tipo_pago',
        class: 'form-control',
        onchange: 'verificar()',
       style: 'asdas'
   });

    $.each(select_options,function(index, option){
        $('<option/>',{
            value: option.value,
            text: option.label
        }).appendTo(select);
    });

    select.appendTo($div);
   $('<label/>', {
       class: "control-label",
       text: "Referencia"
   }).appendTo($div)
    $('<input/>', {
        id: 'id_form-'+total+'-referencia',
        name: 'form-'+total+'-referencia',
        type: 'text',
        class: 'form-control'
    }).appendTo($div);
   $('<label/>', {
       class: "control-label",
       text: "Monto"
   }).appendTo($div)
    $('<input/>', {
        id: 'id_form-'+total+'-monto',
        name: 'form-'+total+'-monto',
        type: 'text',
        class: 'form-control'
    }).appendTo($div);
    $('#formsets').append($div);
    $('#id_form-TOTAL_FORMS').val(total+1);
}


$(document).on('click', '.add-imagen', function(event){
    event.preventDefault();
    var target = $(this).parent().siblings('input:text');
    sumar(target, 'imagen', total_imagenes);
});
$(document).on('click', '.minus-imagen', function(event){
    event.preventDefault();
    var target = $(this).parent().siblings('input:text');
    restar(target, 'imagen', total_imagenes)
});
