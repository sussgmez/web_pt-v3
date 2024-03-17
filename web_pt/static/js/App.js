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
        'text_search': $('#id_search_text').val(),
        'status_search': $('#id_installation_status').val(),
        'min_date': $('#id_from_date').val(),
        'max_date': $('#id_to_date').val(),
        'technician_search': $('#id_technician').val(),
        'order_by': $('#id_order_by_input').val(),
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
        'technician': $('#id_technician').val(),
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

function check_contract_number(value) {
    if (parseInt(value) >= 1000000 && parseInt(value) <= 1099999) {
        fetch(`./update_customer/${value}`)
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
                $("#id_technician").val("--");
                
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
}