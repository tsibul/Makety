function upd_ln(cst_){
    var cst = 'cst_id_' + cst_;
    var cst2 = 'cst_id2_' + cst_;
    document.getElementById(cst2).style.display='block';
    document.getElementById(cst).style.display='none';}

function upd_ln_reverse(cst_){
    var cst = 'cst_id_' + cst_;
    var cst2 = 'cst_id2_' + cst_;
    document.getElementById(cst).style.display='block';
    document.getElementById(cst2).style.display='none';}

function add_ln(new_ln){
    document.getElementById(new_ln).style.display='block';}

function add_ln_reverse(new_ln){
    document.getElementById(new_ln).style.display='none';}

function colapse(id){
    var area = 'collapse_' + id;
    if (document.getElementById(area).style.display ==='none'){
    document.getElementById(area).style.display = 'initial';}
    else {document.getElementById(area).style.display = 'none';};
}

function colapse_(id){
    var area = 'collapse_' + id;
    if (document.getElementById(area).style.display ==='none'){
    document.getElementById(area).style.display = 'table-row-group';}
    else {document.getElementById(area).style.display = 'none';};
}

function upload_order(id){
    var cust_nm = document.getElementById('cust_nm_' + id).textContent;
    var ord_id = document.getElementById('ord_id_' + id).textContent;
    document.getElementById('upload_id').value = id;
    document.getElementById('uploadOrderLabel').textContent = ord_id + ' ' + cust_nm;
    document.getElementById('but_upl_' + id).disabled = false;
}

function  block_button(){
    document.getElementById('but_imp_modal').disabled = true;
}

function delete_object_modal(id){
    document.getElementById('object_to_delete').value = id
    document.getElementById('object_no').textContent = document.getElementById('ord_id_' + id).textContent
    document.getElementById('object_date').textContent = document.getElementById('order_date_' + id).textContent
    document.getElementById('object_customer').textContent = document.getElementById('cust_nm_' + id).textContent
}

function replace_print_rows(selectObj){
    var id_current = selectObj.dataset.id_current;
    var id = selectObj.dataset.id;
    var id_n_current = selectObj.value;
    var parentSelect = selectObj.parentNode.parentNode.parentNode
    var newObj = document.querySelector('[data-id_current="' + id_n_current + '"]')
    var parentNew = newObj.parentNode.parentNode.parentNode
    var id_n = newObj.dataset.id;
    var select_new = 'select_' + id_n;
    var rowNew = parentNew.nextElementSibling
    var rowOld = parentSelect.nextElementSibling
    parentSelect.parentNode.insertBefore(rowNew,parentSelect.nextSibling);
    parentNew.parentNode.insertBefore(rowOld,parentNew.nextSibling);
    document.getElementById(select_new).value = id_current;
    var temp = document.querySelector('[data-id_current="' + id_n_current + '"]');
    temp.dataset.id_current = id_current;
    selectObj.dataset.id_current = id_n_current;}

function order_repaired(id){
    var xhr = new XMLHttpRequest();
    var url = '/maket/maket_check_status/' + id;
    xhr.open("GET", url, true);
    xhr.send();

}

