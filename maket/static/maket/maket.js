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

function clr_edit(clr_id){
    document.getElementById('clr_id').value = document.getElementById('clrid_' + clr_id).textContent;
    document.getElementById('clr_nm').value = document.getElementById('clrnm_' + clr_id).textContent;
    document.getElementById('dt1_ptn').value = document.getElementById('clrpnt_' + clr_id).textContent;
    document.getElementById('dt1_hex').value = document.getElementById('clrhex_' + clr_id).textContent;
    var chosen = document.getElementById('option_' + clr_id).value;
    document.getElementById('id_id').value = clr_id;
    document.getElementById('sch_id_' + chosen).selected = true;
}

function clear_color_modal(){
    document.getElementById('clr_id').value = null;
    document.getElementById('clr_nm').value = null;
    document.getElementById('dt1_ptn').value = null;
    document.getElementById('dt1_hex').value = null;
    document.getElementById('id_id').value = null;
}

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

function select_film(id){
    document.getElementById('modal_save').disabled = false;
    var pg_id_1 = 'pg_' + id + '_1';
    var pg_text_1 = document.getElementById(pg_id_1).value;
    var pg_id_2 = 'pg_' + id + '_2';
    var pg_text_2 = document.getElementById(pg_id_2).value;
    document.getElementById('modal_pg_id').value = id;
    document.getElementById('modal_pg_1').innerHTML = pg_text_1;
    document.getElementById('modal_pg_2').innerHTML = pg_text_2;
}

function save_to_film(obj){
    obj.disabled = true;
    var film_data = document.getElementById('select_film').value;
    var flm_data = film_data.split('|');
    var id = document.getElementById('modal_pg_id').value;
    var film = flm_data[0];
    if(film!=0){
    var film_date = flm_data[2];
    var film_id = flm_data[1]
    }else{
    var film_date = document.getElementById('current_date').value;
    var film_id = document.getElementById('last_film').value;
    //film = film_id;
    }
    var filmout = 'filmout_' + id;
    var dateout = 'dateout_' + id;
    document.getElementById(filmout).innerHTML = film_id;
    document.getElementById(dateout).innerHTML = film_date;
    var xhr = new XMLHttpRequest();
    var url = 'save_to_film/' + id + '/' + film;
    xhr.open("GET", url, true);
    xhr.send();

}

function update_film(id){
   var flm_id = 'film_' + id;
   var film_id = document.getElementById(flm_id).value;
   var date_ = 'date_' + id;
   var date = document.getElementById(date_).value;
   var format_ = 'format_' + id;
   var format = document.getElementById(format_).value;
   var sent_ = 'sent_' + id;
   var sent = document.getElementById(sent_).value;

   document.getElementById('id').value = id;
   document.getElementById('#').value = film_id;
   document.getElementById('date').value = date;
   document.getElementById('format').value = format;
   document.getElementById('sent').value = sent;
}

function update_to_film(){
   var id = document.getElementById('id').value;
   var film_id = document.getElementById('#').value;
   var date = document.getElementById('date').value;
   var arrDate = date.split("-");
   var date_s = arrDate[2] + "." +arrDate[1] + "." + arrDate[0];
   var format = document.getElementById('format').value;
   var sent = document.getElementById('sent').value;
   var output = 'output_' + id;
   var textout = 'Пленка: ' + film_id + ' от ' + date_s + ' формат ' + format;
   if(sent===''){
   textout += ' в работе ';
   }else{
   var arrDate2 = sent.split("-");
   textout += ' выведена ' + arrDate2[2] + "." +arrDate2[1] + "." + arrDate2[0];
   }
   var data_to_film = id + '_' + date + '_' + format + '_' + sent + '_' + film_id;
   document.getElementById(output).innerHTML = textout;
   var xhr = new XMLHttpRequest();
   var url = 'update_to_film/' + data_to_film;
   xhr.open("GET", url, true);
   xhr.send();
}

function upload_order(id){
    var cust_nm = document.getElementById('cust_nm_' + id).textContent;
    var ord_id = document.getElementById('ord_id_' + id).textContent;
    document.getElementById('upload_id').value = id;
    document.getElementById('uploadOrderLabel').textContent = ord_id + ' ' + cust_nm;
    document.getElementById('but_upl_' + id).disabled = false;
}

function upload_maket(id){
    var cust_nm = document.getElementById('cust_nm_' + id).value;
    var ord_id = document.getElementById('ord_id_' + id).value;
    var mk_id = document.getElementById('mk_id_' + id).textContent;
    document.getElementById('upload_id').value = id;
    document.getElementById('uploadMaketLabel').textContent = ord_id + mk_id;
    document.getElementById('uploadMaketLabel2').textContent = cust_nm;

    document.getElementById('but_upl_' + id).disabled = false;
}

function upload_film(id){
    var film1 = document.getElementById('film1_' + id).value;
    var film2 = document.getElementById('film2_' + id).value;
    document.getElementById('upload_id').value = id;
    document.getElementById('uploadFilmLabel').textContent = film1;
    document.getElementById('uploadFilmLabel2').textContent = film2;

    document.getElementById('but_upl_' + id).disabled = false;
}

function total_collapse(){
    const ids=document.querySelectorAll('[id*="collapse_mkt"]')
    for(var i in ids){
    if (ids[i].style.display ==='none'){
    ids[i].style.display = 'table-row-group';}
    else {ids[i].style.display = 'none';};
    }
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

function upload_pattern(buttonObj){
    document.getElementById('upload_id').value = buttonObj.parentElement
                                                                   .parentElement
                                                                   .dataset.id;
    document.getElementById('uploadPatternLabel').textContent = buttonObj.parentElement
                                                                                  .parentElement
                                                                                  .dataset.name;
}

function clear_add_file(clrObj){
    clrObj.parentElement
          .parentElement
          .childNodes[1]
          .childNodes[1]
          .childNodes[1].value = null;
    clrObj.parentElement
          .parentElement
          .childNodes[1]
          .childNodes[3]
          .childNodes[1].value = null;
    clrObj.parentElement
          .parentElement
          .childNodes[3]
          .childNodes[1].value = null;
}

