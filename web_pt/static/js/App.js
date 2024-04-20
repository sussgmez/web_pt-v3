function show_div(id_div) {
    $(id_div).show();
}

function show_customer_menu(e, div) {
    if ($(div.parentElement.parentElement.querySelector('.customer-menu')).css('display') == 'none') {
        $('.options-menu').hide()
        $(div.parentElement.parentElement.querySelector('.customer-menu')).show();
        e.stopPropagation()
    }
}

async function get_form(url, id_div) {
    await fetch(`${url}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        document.getElementById(id_div).innerHTML = data
        $(`#${id_div}`).show()
    })
}

function save_schedule() {
    $('.assign-info').submit()
    add_alert_message("Agenda guardada.")
}

async function submit_scheduled_customer(form) {
    await fetch(form.action, {
        method: form.method,
        body: new FormData(form)
    })
    .finally(() => {
        if (window.location.pathname == '/schedule/') { 
            get_schedule()
        }
    })
}

async function save_customer(form) {
    await fetch(form.action, {
        method: form.method,
        body: new FormData(form)
    })
    .finally(() => {
        if (window.location.pathname == '/home/') { 
            get_customer_list()
        }
        if (window.location.pathname == '/schedule/') { 
            get_schedule()
            get_customers_to_assign()
        }
        if (window.location.pathname == '/preconfig/') { 
            get_preconfig_customers()
        }
        if (window.location.pathname == '/inventory/onu/') {
            get_onu_list()
            get_add_onu_form()
        }
        if (form.id == 'id_delete_customer_form') add_alert_message("Se ha eliminado el cliente.")
        else add_alert_message("Cambios guardados con éxito.")
    })
}

async function delete_onu(form) {
    await fetch(form.action, {
        method: form.method,
        body: new FormData(form)
    })
    .finally(() => {
        if (window.location.pathname == '/inventory/onu/') {
            get_onu_list()
            get_add_onu_form()
        }
        if (form.id == 'id_delete_customer_form') add_alert_message("Se ha eliminado el dispositivo correctamente.")
        else add_alert_message("Cambios guardados con éxito.")
    })
}

async function delete_router(form) {
    await fetch(form.action, {
        method: form.method,
        body: new FormData(form)
    })
    .finally(() => {
        if (window.location.pathname == '/inventory/router/') {
            get_router_list()
            get_add_router_form()
        }
        if (form.id == 'id_delete_customer_form') add_alert_message("Se ha eliminado el dispositivo correctamente.")
        else add_alert_message("Cambios guardados con éxito.")
    })
}

function check_serial_onu() {
    fetch(`../update_onu/${$('#id_serial').val()}`)
    .then(response => {
        if (response.ok) {
            add_error_message("Serial ONU ya registrado en la Base de Datos.")
        }
    })
}

function check_serial_router() {
    fetch(`../update_router/${$('#id_serial').val()}`)
    .then(response => {
        if (response.ok) {
            add_error_message("Serial Router ya registrado en la Base de Datos.")
        }
    })
}

async function save_onu(form) {
    await fetch(form.action, {
        method: form.method,
        body: new FormData(form)
    })
    .then(response => {
        if (response.status == 500) {
            add_error_message("Cliente no existe.")
        }
    })
    .finally(() => {
        if (window.location.pathname == '/inventory/onu/') {
            get_onu_list()
            get_add_onu_form()
        }
    })
}

async function save_router(form) {
    await fetch(form.action, {
        method: form.method,
        body: new FormData(form)
    })
    .then(response => {
        if (response.status == 500) {
            add_error_message("Cliente no existe.")
        }
    })
    .finally(() => {
        if (window.location.pathname == '/inventory/router/') {
            get_router_list()
            get_add_router_form()
        }
    })
}

async function assign_order(form) {
    await fetch(form.action, {
        method: form.method,
        body: new FormData(form)
    })
    .finally(() => {
        if (window.location.pathname == '/schedule/') { 
            get_schedule()
            get_customers_to_assign()
        }
    })
}

async function get_customer_list(num_page = 1) {
    filters = {
        'text_search': $('#id_filter_search_text').val(),
        'status_search': $('#id_filter_installation_status').val(),
        'min_date': $('#id_filter_from_date').val(),
        'max_date': $('#id_filter_to_date').val(),
        'technician_search': $('#id_filter_technician').val(),
        'order_by': $('#id_filter_order_by_input').val(),
    }
    await fetch(`../customer_list?page=${num_page}&text_search=${filters.text_search}&min_date=${filters.min_date}&max_date=${filters.max_date}&technician_search=${filters.technician_search}&status_search=${filters.status_search}&order_by=${filters.order_by}`)
    .then(response => {
        if (!response.ok) {
            get_customer_list()
            return Promise.reject(response);
        } else {
            return response.text()
        }
    })
    .then(data => {
        document.querySelector('#id_customer_list').innerHTML = data
    })
}

async function get_schedule() {
    filters = {
        'technician': $('#id_filter_technician').val(),
        'date': $('#id_date').val(),
    }
    await fetch(`../scheduled_customers?date=${filters.date}&technician=${filters.technician}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        document.querySelector('#id_schedule').innerHTML = data
    })
}

async function get_customers_to_assign() {
    filters = {
        'text_search': $('#id_search_text_to_assign').val(),
    }
    await fetch(`../customers_to_assign?text_search=${filters.text_search}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        document.querySelector('#id_customers_to_assign').innerHTML = data
    })
}

async function get_preconfig_customers() {
    filters = {
        'date': $('#id_date').val(),
    }
    await fetch(`../preconfig_customers?date=${filters.date}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        document.querySelector('#id_preconfig_customers').innerHTML = data
    })
}

async function submit_preconfig_customer(form) {
    await fetch(form.action, {
        method: form.method,
        body: new FormData(form)
    })
}

function check_contract_number(value) {
    if (parseInt(value) >= 1000000 && parseInt(value) <= 1099999) {
        fetch(`../update_customer/${value}`)
        .then(response => {
            if (!response.ok) { 
                $("#id_btn_submit_add_customer").prop('disabled', false);
                $('#id_check_contract_number').removeClass('status-invalid');
                $('#id_check_contract_number').removeClass('status-waiting');
                $('#id_check_contract_number').addClass('status-valid');
                $('#id_check_contract_number').html("Nro. De Contrato válido.");
            } else {
                $("#id_btn_submit_add_customer").prop('disabled', true);
                $('#id_check_contract_number').addClass('status-invalid');
                $('#id_check_contract_number').removeClass('status-waiting');
                $('#id_check_contract_number').removeClass('status-valid');
                $('#id_check_contract_number').html("Nro. De Contrato ya existe.");
            }
        })
    } else {
        $("#id_btn_submit_add_customer").prop('disabled', true);
        $('#id_check_contract_number').removeClass('status-invalid');
        $('#id_check_contract_number').addClass('status-waiting');
        $('#id_check_contract_number').removeClass('status-valid');
        $('#id_check_contract_number').html("Ingrese un nro. de contrato válido.");
    }
}

async function export_xlsx() {
    var filename = ""
    filters = {
        'text_search': $('#id_search_text').val(),
        'status_search': $('#id_installation_status').val(),
        'min_date': $('#id_from_date').val(),
        'max_date': $('#id_to_date').val(),
        'technician_search': $('#id_technician').val(),
    }
    await fetch(`../export_xlsx?&text_search=${filters.text_search}&min_date=${filters.min_date}&max_date=${filters.max_date}&technician_search=${filters.technician_search}&status_search=${filters.status_search}&order_by=${filters.order_by}`)
    .then(response => {
        filename = response.headers.get('content-disposition').split('filename=')[1]
        return response.blob()
    })
    .then(response => {
        const aElement = document.createElement('a');
        aElement.setAttribute('download', filename)
        const href = URL.createObjectURL(response)
        aElement.href = href;
        aElement.setAttribute('target', '_blank');
        aElement.click()
        URL.revokeObjectURL(href);
    })
}

function get_preconfig_message() { 
    let preconfig_message = ""
    $('.preconfig-form').each(function (index, element) {
        let contract_number = element.querySelector('.preconfig-message-contract-number').value;
        let category = element.querySelector('.preconfig-message-category').value;
        let plan = element.querySelector('.preconfig-message-plan').value;
        let zone = element.querySelector('.preconfig-message-zone').value;
        let onu_serial = element.querySelector('.preconfig-message-onu').value;
        preconfig_message+=`C${contract_number}, Zona ${zone}, ${plan}, ${onu_serial}, ${category}\n`
    });
    navigator.clipboard.writeText(preconfig_message)
}

function get_customer_message(customer_form) {
    let category = customer_form.querySelector('#id_category').value;
    let contract_number = customer_form.querySelector('#id_contract_number').value;
    let customer_name = customer_form.querySelector('#id_customer_name').value;
    let address = customer_form.querySelector('#id_address').value;
    let plan = customer_form.querySelector('#id_plan').value;
    let zone = customer_form.querySelector('#id_zone').value;
    let olt = customer_form.querySelector('#id_olt').value;
    let card = customer_form.querySelector('#id_card').value;
    let pon = customer_form.querySelector('#id_pon').value;
    let box = customer_form.querySelector('#id_box').value;
    let port = customer_form.querySelector('#id_port').value;
    
    let box_power = customer_form.querySelector('#id_box_power').value;
    let house_power = customer_form.querySelector('#id_house_power').value;

    let onu_serial = customer_form.querySelector('#id_onu').value;

    let drop_serial = customer_form.querySelector('#id_drop_serial').value;
    let drop_used = customer_form.querySelector('#id_drop_used').value;

    let hook_used = customer_form.querySelector('#id_hook_used').value;
    let fast_conn_used = customer_form.querySelector('#id_fast_conn_used').value;

    let customer_message = `*Validar potencia | ${category}*\n*Nro. De Contrato:* C${contract_number}\n*Nombre:* ${customer_name}\n*Dirección:* ${address}\n*Plan:* ${plan}\n*Z${zone}.OLT${olt}.T${card}.PON${pon}.C${box}.PUERTO${port}*\n*PC:* ${box_power}dBm\n*PR:* ${house_power}dBm\n*Serial ONU:* ${onu_serial}\n*DROP:* ${drop_serial}/${drop_used}m\n*Tensores:* ${hook_used}\n*Conectores:* ${fast_conn_used}`
    navigator.clipboard.writeText(customer_message)
}

function get_schedule_message() {

    let customer_name = $('#id_customer_name').val();
    let date_assigned = $('#id_date_assigned').val().split('-');
    let time_assigned = $('#id_time_assigned').val().split(':');

    let message = `Reciba un cordial saludo, ${customer_name}.\nLe escribimos de parte de la contratista Piccioli Telco con intenciones de consultar si existe la posibilidad de asistir el día ${date_assigned[2]}/${date_assigned[1]} a las ${time_assigned[0]}:${time_assigned[1]} para realizar la instalación del servicio de Internet de Datalink C.A en su residencia, quedamos atento a su respuesta!`

    navigator.clipboard.writeText(message)
}

function add_alert_message(message_text) {
    let message = $('<p></p>').text(message_text).addClass("success");
    setTimeout(() => {message.fadeOut()}, 4000)
    $('#id_alert_messages').append(message)
}

function add_alert_message(message_text) {
    let message = $('<p></p>').text(message_text).addClass("success");
    setTimeout(() => {message.fadeOut()}, 4000)
    $('#id_alert_messages').append(message)
}

function add_error_message(message_text) {
    let message = $('<p></p>').text(message_text).addClass("error");
    setTimeout(() => {message.fadeOut()}, 4000)
    $('#id_alert_messages').append(message)
}

async function get_onu_list() {
    filters = {
        'text_search': $('#id_text_search').val(),
    }
    await fetch(`../onu_list?text_search=${filters.text_search}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        document.querySelector('#id_device_list').innerHTML = data
    })
}

async function get_router_list() {
    filters = {
        'text_search': $('#id_text_search').val(),
    }
    await fetch(`../router_list?text_search=${filters.text_search}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        document.querySelector('#id_device_list').innerHTML = data
    })
}

async function get_add_onu_form() {
    await fetch(`../add_onu`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        document.querySelector('#id_div_form_onu').innerHTML = data
    })
}

async function get_add_router_form() {
    await fetch(`../add_router`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        document.querySelector('#id_div_form_router').innerHTML = data
    })
}

async function get_update_onu_form(pk) {
    await fetch(`../update_onu/${pk}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        document.querySelector('#id_div_form_onu').innerHTML = data
    })
}

async function get_update_router_form(pk) {
    await fetch(`../update_router/${pk}`)
    .then(response => {
        return response.text()
    })
    .then(data => {
        document.querySelector('#id_div_form_router').innerHTML = data
    })
}

function redirect_inventory(type) {
    document.location = `../${type}/`
}

window.onload = () => {
    document.addEventListener('click', function () {
        $('.options-menu').hide()
    })
    if (window.location.pathname == '/home/') {
        $('#id_btn_add_customer_options').click(function (e) { 
            if ($('#id_add_customer_options').css('display') == 'none') {
                $('.options-menu').hide()
                show_div('#id_add_customer_options')
                e.stopPropagation()
            }
        });
        $('#id_installation_status').change(function (e) { 
            e.preventDefault();
            if (this.value == 'or-assigned' || this.value == 'or-completed') {
                $("#id_from_date").prop('disabled', false);
                $("#id_to_date").prop('disabled', false);
                $("#id_technician").prop('disabled', false);
                
            } else {
                $("#id_from_date").val("");
                $("#id_to_date").val("");
                
                $("#id_from_date").prop('disabled', true);
                $("#id_to_date").prop('disabled', true);
                $("#id_technician").prop('disabled', true);
            }
        });
        get_customer_list()
    }
    else if (window.location.pathname == '/schedule/')  {
        get_schedule() 
        get_customers_to_assign()
    }
    else if (window.location.pathname == '/preconfig/') {
        get_preconfig_customers()
    }
    else if (window.location.pathname == '/inventory/onu/') {
        get_onu_list()
        get_add_onu_form()
    }
    else if (window.location.pathname == '/inventory/router/') {
        get_router_list()
        get_add_router_form()
    }
    

    $('#id_alert_messages').children().each(function () { 
        setTimeout(() => {$(this).fadeOut()}, 4000)
    })
}