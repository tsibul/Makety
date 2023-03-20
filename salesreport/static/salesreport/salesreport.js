function block_but(param) {
    document.getElementById(param).disabled = true;
}

function clientActive(obj) {
    if (obj.name == "off") {
        document.querySelectorAll(".text-danger").forEach((x) => {
            x.style.display = "none";
        });
        obj.name = "on";
    } else {
        document.querySelectorAll(".text-danger").forEach((x) => {
            x.style.display = "table-row"
        })
        obj.name = "off";
    }
}

function fillModalCustomers(custObj) {
    document.getElementById('id').value = custObj.dataset.id;
    document.getElementById('gr_id').value = custObj.dataset.group_id;
    document.getElementById('rg').value = custObj.dataset.region;
    document.getElementById('inn').value = custObj.dataset.inn;
    document.getElementById('nm').textContent = custObj.dataset.name;
    document.getElementById('gr').value = custObj.dataset.group;
    document.getElementById('fr').value = custObj.dataset.fr;
    document.getElementById('tp').value = custObj.dataset.type;
    document.getElementById('ad').textContent = custObj.dataset.address;
    if (custObj.dataset.in == 'True') {
        document.getElementById('in').value = 'on';
    }


}

function clearModalCustomers() {
    document.getElementById('id').value = null;
    document.getElementById('gr_id').value = null;
    document.getElementById('rg').value = null;
    document.getElementById('in').value = null;
    document.getElementById('nm').textContent = null;
    document.getElementById('gr').value = '1';
    document.getElementById('fr').value = null;
    document.getElementById('tp').value = '1';
    document.getElementById('ad').textContent = null;
    document.getElementById('inn').value = null;
}

function fillModalCustomerGroups(custObj) {
    document.getElementById('id').value = custObj.dataset.id;
    document.getElementById('nm').value = custObj.dataset.name;
    document.getElementById('tp').value = custObj.dataset.type;

}

function clearModalCustomerGroups() {
    document.getElementById('id').value = null;
    document.getElementById('nm').value = null;
    document.getElementById('tp').value = '1';
}

function redNumberColor(tdObj) {
    tdObj.classList.add('text-danger')
}

function backNumberColor(tdObj) {
    tdObj.classList.remove('text-danger')
}

function showClientsC(trObj) {
    var objId = trObj.parentElement.id
    document.querySelectorAll("." + objId.toString()).forEach((x) => {
        x.style.display = "table-row"
    })
    trObj.parentElement.style.display = 'none'
}

function hideClientsC(param) {
    document.querySelectorAll("." + param).forEach((x) => {
        x.style.display = "none"
    })
    document.getElementById(param).style.display = 'table-row'
}

function listCustomers(listObj) {
    var customers = listObj.dataset.list.replace('[', '')
                                        .replace(']', '')
                                        .replaceAll("'", '')
                                        .replaceAll('"', '')
                                        .split(',');
    var textOut = '';
    customers.forEach(addBr);
    document.getElementById('customerListModalLabel').textContent = listObj.dataset.name;
    document.getElementById('modal-body').innerHTML = textOut;

    function addBr(value){
      textOut += value + ",<br>";
    }
}

function activeWeeksNo(inpObj){
    document.getElementById('group_weeks').value = inpObj.value;

}

function redParentNumberColor(tdObj) {
    tdObj.classList.add('text-danger')
    tdObj.classList.add('table-secondary')
}

function backParentNumberColor(tdObj) {
    tdObj.classList.remove('text-danger')
    tdObj.classList.remove('table-secondary')
}


function showClientsG(trObj) {
    var objId = trObj.id
    document.querySelectorAll("." + objId.toString()).forEach((x) => {
        x.style.display = "table-row"
    })
    trObj.style.display = 'none'
}

function hideClientsG(param) {
    document.querySelectorAll("." + param).forEach((x) => {
        x.style.display = "none"
    })
    document.getElementById(param).style.display = 'table-row'
}
