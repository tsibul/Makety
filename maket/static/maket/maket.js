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

function upd_dtl(detail_id, clr_in){
    var red = 'red_' + detail_id;
    var it_nm = 'it_nm_' + detail_id;
    var nm = 'nm_' + detail_id;
    var clr = 'ColorSelect_' + detail_id;
    var chck1 = 'chck1_' + detail_id;
    var dt1_nm = 'dt1_nm_' + detail_id;
    var chck2 = 'chck2_' + detail_id;
    var dt2_nm = 'dt2_nm_' + detail_id;
    var chck3 = 'chck3_' + detail_id;
    var dt3_nm = 'dt3_nm_' + detail_id;
    var chck4 = 'chck4_' + detail_id;
    var dt4_nm = 'dt4_nm_' + detail_id;
    var chck5 = 'chck5_' + detail_id;
    var dt5_nm = 'dt5_nm_' + detail_id;
    var otm = 'otm_' + detail_id;
    var ok = 'ok_' + detail_id;

    var clr_schemes = []
    for (var i=1; i<100; i++) {
    var clr_id = 'clr_sr_' + i;
    try {var clr_schm = document.getElementById(clr_id).value;
    clr_schemes.push(clr_schm);}
    catch(err){break}};

    var clr_numb = clr_schemes.length;
    var clr_html = ''

    for (var i = 0; i < clr_numb; i++){
    if (clr_schemes[i] === clr_in){var selected = 'selected'}else{var selected = ''};
    clr_html +=('<option value="' + clr_schemes[i] + '" ' + selected + ' name="ColorSelect">' +
    clr_schemes[i] + '</option>');
    }

    document.getElementById(red).disabled = true;
    document.getElementById(it_nm).disabled = false;
    document.getElementById(nm).disabled = false;
    document.getElementById(clr).disabled = false;
    document.getElementById(clr).innerHTML = clr_html;

    document.getElementById(chck1).disabled = false;
    document.getElementById(dt1_nm).disabled = false;

    document.getElementById(chck2).disabled = false;
    document.getElementById(dt2_nm).disabled = false;

    document.getElementById(chck3).disabled = false;
    document.getElementById(dt3_nm).disabled = false;

    document.getElementById(chck4).disabled = false;
    document.getElementById(dt4_nm).disabled = false;

    document.getElementById(chck5).disabled = false;
    document.getElementById(dt5_nm).disabled = false;

    document.getElementById(otm).disabled = false;
    document.getElementById(ok).disabled = false;
}

function upd_dtl_reverse(detail_id, color){
    var red = 'red_' + detail_id;
    var it_nm = 'it_nm_' + detail_id;
    var nm = 'nm_' + detail_id;
    var clr = 'ColorSelect_' + detail_id;
    var chck1 = 'chck1_' + detail_id;
    var dt1_nm = 'dt1_nm_' + detail_id;
    var chck2 = 'chck2_' + detail_id;
    var dt2_nm = 'dt2_nm_' + detail_id;
    var chck3 = 'chck3_' + detail_id;
    var dt3_nm = 'dt3_nm_' + detail_id;
    var chck4 = 'chck4_' + detail_id;
    var dt4_nm = 'dt4_nm_' + detail_id;
    var chck5 = 'chck5_' + detail_id;
    var dt5_nm = 'dt5_nm_' + detail_id;
    var otm = 'otm_' + detail_id;
    var ok = 'ok_' + detail_id;

    clr_html = '<option value="' + color + '" name="color" disabled selected>' + color + '</option>';


    document.getElementById(red).disabled = false;
    document.getElementById(it_nm).disabled = true;
    document.getElementById(nm).disabled = true;

    document.getElementById(chck1).disabled = true;
    document.getElementById(dt1_nm).disabled = true;

    document.getElementById(chck2).disabled = true;
    document.getElementById(dt2_nm).disabled = true;

    document.getElementById(chck3).disabled = true;
    document.getElementById(dt3_nm).disabled = true;

    document.getElementById(chck4).disabled = true;
    document.getElementById(dt4_nm).disabled = true;

    document.getElementById(chck5).disabled = true;
    document.getElementById(dt5_nm).disabled = true;

    document.getElementById(otm).disabled = true;
    document.getElementById(ok).disabled = true;

    document.getElementById(clr).innerHTML = clr_html;
    document.getElementById(clr).disabled = true;

}

function clr_edit(detail_id, clr_in){
    var red = 'red_' + detail_id;
    var clrid = 'clrid_' + detail_id;
    var clrnm = 'clrnm_' + detail_id;
    var clrpnt = 'clrpnt_' + detail_id;
    var clrhex = 'clrhex_' + detail_id;
    var clr = 'ColorSelect2_' + detail_id;
    var ok = 'okclr_' + detail_id;
    var otmclr = 'otmclr_' + detail_id;
    var okclr = 'okclr_' + detail_id;


    var clr_schemes = []
    for (var i=1; i<100; i++) {
    var clr_id = 'clr_sr_' + i;
    try {var clr_schm = document.getElementById(clr_id).value;
    clr_schemes.push(clr_schm);}
    catch(err){break}};

    var clr_numb = clr_schemes.length;
    var clr_html = ''

    for (var i = 0; i < clr_numb; i++){
    if (clr_schemes[i] === clr_in){var selected = 'selected'}else{var selected = ''};
    clr_html +=('<option value="' + clr_schemes[i] + '" ' + selected + ' name="ColorSelect">' +
    clr_schemes[i] + '</option>');
    }

    document.getElementById(red).disabled = true;
    document.getElementById(clrid).disabled = false;
    document.getElementById(clrnm).disabled = false;
    document.getElementById(clrpnt).disabled = false;
    document.getElementById(clrhex).disabled = false;
    document.getElementById(clr).disabled = false;
    document.getElementById(clr).innerHTML = clr_html;

    document.getElementById(otmclr).disabled = false;
    document.getElementById(okclr).disabled = false;
}

function clr_edit_reverse(detail_id, color){
    var red = 'red_' + detail_id;
    var clrid = 'clrid_' + detail_id;
    var clrnm = 'clrnm_' + detail_id;
    var clrpnt = 'clrpnt_' + detail_id;
    var clrhex = 'clrhex_' + detail_id;
    var clr = 'ColorSelect2_' + detail_id;
    var ok = 'okclr_' + detail_id;
    var otmclr = 'otmclr_' + detail_id;
    var okclr = 'okclr_' + detail_id;

    clr_html = '<option value="' + color + '" name="color" disabled selected>' + color + '</option>';

    document.getElementById(red).disabled = false;
    document.getElementById(clrid).disabled = true;
    document.getElementById(clrnm).disabled = true;
    document.getElementById(clrpnt).disabled = true;
    document.getElementById(clrhex).disabled = true;
    document.getElementById(clr).disabled = true;
    document.getElementById(clr).innerHTML = clr_html;

    document.getElementById(otmclr).disabled = true;
    document.getElementById(okclr).disabled = true;

}

function upd_cst(id){
    var nm = 'nm_' + id;
    var gr = 'gr_' + id;
    var tp = 'tp_' + id;
    var rg = 'rg_' + id;
    var in_ = 'in_' + id;
    var ad = 'addr_' + id;
    var nm_val = document.getElementById(nm).textContent;
    var gr_val = document.getElementById(gr).textContent;
    var tp_val = document.getElementById(tp).textContent;
    var rg_val = document.getElementById(rg).textContent;
    var in_val = document.getElementById(in_).textContent;
    var ad_val = document.getElementById(ad).textContent;
    var nm_html = ('<div class="row"><div class="col" style="max-width:40px;"><div class="m-1">' +
    '<a href="javascript:upd_cst_reverse(' + id + ');"><button class="btn btn-sm btn-outline-secondary" type="button">' +
    '<i class="bi bi-arrow-counterclockwise"></i></button></a></div>' +
    '<div class="m-1"><button class="btn btn-sm btn-outline-primary" type="submit" form="form_' + id + '">' +
    '<i class="bi bi-check2"></i></button></div></div><div class="col">' +
    '<textarea  class="form-control" name="nm" form="form_' + id + '">' +
    nm_val + '</textarea></div></div>');
    document.getElementById(nm).innerHTML = nm_html;
    var gr_html = ('<textarea  class="form-control" name="gr" id="' + gr +'" form="form_' + id + '">' +
    gr_val + '</textarea>');
    document.getElementById(gr).innerHTML = gr_html;
    var tp_html = ('<textarea  class="form-control" name="tp" form="form_' + id + '">' +
    tp_val + '</textarea>');
    document.getElementById(tp).innerHTML = tp_html;
    var rg_html = ('<textarea  class="form-control" name="rg" form="form_' + id + '">' +
    rg_val + '</textarea>');
    document.getElementById(rg).innerHTML = rg_html;
    var in_html = ('<textarea  class="form-control" name="in_" form="form_' + id + '">' +
    in_val + '</textarea>');
    document.getElementById(in_).innerHTML = in_html;
    var ad_html = ('<textarea  class="form-control" name="ad" form="form_' + id + '">' +
    ad_val + '</textarea>');
    document.getElementById(ad).innerHTML = ad_html;
    document.getElementById('row_'+id).setAttribute('onclick','');
}

function upd_cst_reverse(id){
    var nm = 'nm_' + id;
    var gr = 'gr_' + id;
    var tp = 'tp_' + id;
    var rg = 'rg_' + id;
    var in_ = 'in_' + id;
    var ad = 'addr_' + id;
    var nm_val = document.getElementById(nm).textContent;
    var gr_val = document.getElementById(gr).textContent;
    var tp_val = document.getElementById(tp).textContent;
    var rg_val = document.getElementById(rg).textContent;
    var in_val = document.getElementById(in_).textContent;
    var ad_val = document.getElementById(ad).textContent;

    document.getElementById(nm).innerHTML = nm_val;
    document.getElementById(gr).innerHTML = gr_val;
    document.getElementById(tp).innerHTML = tp_val;
    document.getElementById(rg).innerHTML = rg_val;
    document.getElementById(in_).innerHTML = in_val;
    document.getElementById(ad).innerHTML = ad_val;
    document.getElementById('row_'+id).setAttribute('onclick','javascript:upd_cst(' + id + ');');

}

function split_maket(print_range){
    var number_items = print_range.length;
    for(i=0; i<number_items; i++){
    var line = 'chck_' + print_range[i][2] + '_' + print_range[i][9]
    if(document.getElementById(line).checked){if (print_range[i][8] === 'note'){
    document.getElementById(print_range[i][2] + '_' + print_range[i][9]).style.display='block';}
    else{document.getElementById(print_range[i][2] + '_' + print_range[i][9]).style.display='inherit';};
    var hd_line = print_range[i][2] + '_' + print_range[i][9] + '_';
    var hd_line1 = document.querySelectorAll("[id=" + CSS.escape(hd_line) + "]");
    for(var j = 0; j < hd_line1.length; j++) {hd_line1[j].style.display='table-row';}
    }
    else{
    document.getElementById(print_range[i][2] + '_' + print_range[i][9] ).style.display ='none';
    var hd_line = print_range[i][2] + '_' + print_range [i][9] + '_8';
    var hd_line1 = document.querySelectorAll("[id=" + CSS.escape(hd_line) + "]");
    for(var j = 0; j < hd_line1.length; j++) {hd_line1[j].style.display='none';}
    }
}}

function chs_note(prt_0_, note){
    const prt_3A6 = [];
    for(i=0; i<prt_0_.length; i++){
    if(prt_0_[i][3] + '_' + prt_0_[i][6] ===note){prt_3A6.push(prt_0_[i])}
    }
    var number_items = prt_3A6.length;
    try{if(document.getElementById(('chck_'+ note + '_all')).checked){
    for(i=0; i<number_items; i++){var itm_id = 'itm_' + note + '_' + prt_3A6[i][0];
    document.getElementById(itm_id).style.display='block';
    var ln = 'chck_' + note + '_' + prt_3A6[i][0]
    document.getElementById(ln).checked = true;}
    }else{
        try {document.getElementById(('chck_'+ note + '_0'));
    if(document.getElementById(('chck_'+ note + '_0')).checked){
    document.getElementById(('itm_' + note + '_0')).style.display='block';}
    else{document.getElementById(('itm_' + note + '_0')).style.display='none';};}
    catch(err){};
    for(i=0; i<number_items; i++){
    var line = 'chck_' + note + '_' + prt_3A6[i][0]
    var itm_id = 'itm_' + note + '_' + prt_3A6[i][0]
    if(document.getElementById(line).checked){
    document.getElementById(itm_id).style.display='block';}
    else{document.getElementById(itm_id).style.display='none';}
}
    }}catch(err){
    try {document.getElementById(('chck_'+ note + '_0'));
    if(document.getElementById(('chck_'+ note + '_0')).checked){
    document.getElementById(('itm_' + note + '_0')).style.display='block';}
    else{document.getElementById(('itm_' + note + '_0')).style.display='none';};}
    catch(err){};
    for(i=0; i<number_items; i++){
    var line = 'chck_' + note + '_' + prt_3A6[i][0]
    var itm_id = 'itm_' + note + '_' + prt_3A6[i][0]
    if(document.getElementById(line).checked){
    document.getElementById(itm_id).style.display='block';}
    else{document.getElementById(itm_id).style.display='none';}
}}}


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

function pen_position(id, pen_pos){
    var pen_pos = document.getElementById('pen_pos_' + id).value;
    for(var i=1; i<5; i++){
    if(pen_pos === i){
    document.getElementById(i+'_'+id).style.display = 'inline';
    document.getElementById(i+'_big_'+id).style.display = 'inline';}
    else{
    document.getElementById(i+'_'+id).style.display = 'none';
    document.getElementById(i+'_big_'+id).style.display = 'none';}
    }
}

function upd_good(id, clr_schemes, print_group){
   document.getElementById('row_' + id).onclick = "";
   var clr_scheme ='[';
   for(i=0; i<clr_schemes.length; i++){
   clr_scheme += "'" + clr_schemes[i] +"',";
   }
   clr_scheme = clr_scheme.substring(0, clr_scheme.length - 1);
   clr_scheme += ']';
   var print_grp ='[';
   for(i=0; i<print_group.length; i++){
   print_grp += "'" + print_group[i] +"',";
   }
   print_grp = print_grp.substring(0, print_grp.length - 1);
   print_grp += ']';
   var art_ln = 'art_' + id;
   var nm_ln = 'nm_' + id;
   var cs_ln = 'cs_' + id;
   var pg_ln = 'pg_' + id;
   var dt1_ln = 'dt1_' + id;
   var dt1c_ln = 'dt1c_' + id;
   var dt2_ln = 'dt2_' + id;
   var dt2c_ln = 'dt2c_' + id;
   var dt3_ln = 'dt3_' + id;
   var dt3c_ln = 'dt3c_' + id;
   var dt4_ln = 'dt4_' + id;
   var dt4c_ln = 'dt4c_' + id;
   var dt5_ln = 'dt5_' + id;
   var dt5c_ln = 'dt5c_' + id;
   var art = document.getElementById(art_ln).textContent;
   var nm = document.getElementById(nm_ln).textContent;
   var cs = document.getElementById(cs_ln).textContent;
   var pg = document.getElementById(pg_ln).textContent;
   var dt1 = document.getElementById(dt1_ln).textContent;
   var dt2 = document.getElementById(dt2_ln).textContent;
   var dt3 = document.getElementById(dt3_ln).textContent;
   var dt4 = document.getElementById(dt4_ln).textContent;
   var dt5 = document.getElementById(dt5_ln).textContent;
   document.getElementById(dt1c_ln).disabled=false;
   document.getElementById(dt2c_ln).disabled=false;
   document.getElementById(dt3c_ln).disabled=false;
   document.getElementById(dt4c_ln).disabled=false;
   document.getElementById(dt5c_ln).disabled=false;

   var clr_numb = clr_schemes.length;
   var clr_html = ('<div class="input-group"><select class="form-select" style="font-size:80%" id="ColorSelect_' + id
                   + '" name="ColorSelect" form="form_' + id + '">');

   for (var i = 0; i < clr_numb; i++){
   if (clr_schemes[i] === cs){var selected = 'selected'}else{var selected = ''};
   clr_html +=('<option value="' + clr_schemes[i] + '" ' + selected + ' name="ColorSelect_">' +
   clr_schemes[i] + '</option>');
   }
   clr_html += '</select></div>';
   document.getElementById(cs_ln).innerHTML = clr_html;

   var prt_numb = print_group.length;
   var prt_html = ('<div class="input-group"><select class="form-select" style="font-size:80%" id="PrtSelect_' + id
                   + '" name="PrtSelect" form="form_' + id + '">');

   for (var i = 0; i < prt_numb; i++){
   if (print_group[i] === pg){var selected = 'selected'}else{var selected = ''};
   prt_html +=('<option value="' + print_group[i] + '" ' + selected + ' name="PrtSelect_">' +
   print_group[i] + '</option>');
   }
   prt_html += '</select></div>';
   document.getElementById(pg_ln).innerHTML = prt_html;

   document.getElementById(art_ln).innerHTML = '<div class="row"><div class="col" style="max-width:40px;"><div class="m-1">' +
    '<a href="javascript:upd_good_reverse(' + id + ", '" + cs + "', '" + pg + "', " + clr_scheme + ", "  + print_grp +
    "" + ');"><button class="btn btn-sm btn-outline-secondary" type="button">' +
    '<i class="bi bi-arrow-counterclockwise"></i></button></a></div>' +
    '<div class="m-1"><button class="btn btn-sm btn-outline-primary" type="submit" form="form_' + id + '">' +
    '<i class="bi bi-check2"></i></button></div></div><div class="col">' +
    '<textarea type="text" name="art" style="max-width:60px; font-size:80%;"' +
                                    ' class="form-control" form="form_' + id + '">' + art + '</textarea></div></div>';
   document.getElementById(nm_ln).innerHTML = '<textarea type="text" name="nm"' +
                        '" class="form-control" style="font-size:100%;" form="form_' + id + '">' + nm + '</textarea>';
   document.getElementById(dt1_ln).innerHTML = '<textarea type="text" name="dt1"' +
                        '" class="form-control" style="font-size:80%;" form="form_' + id + '">' + dt1 + '</textarea>';
   document.getElementById(dt2_ln).innerHTML = '<textarea type="text" name="dt2"' +
                        '" class="form-control" style="font-size:80%;" form="form_' + id + '">' + dt2 + '</textarea>';
   document.getElementById(dt3_ln).innerHTML = '<textarea type="text" name="dt3"' +
                        '" class="form-control" style="font-size:80%;" form="form_' + id + '">' + dt3 + '</textarea>';
   document.getElementById(dt4_ln).innerHTML = '<textarea type="text" name="dt4"' +
                        '" class="form-control" style="font-size:80%;" form="form_' + id + '">' + dt4 + '</textarea>';
   document.getElementById(dt5_ln).innerHTML = '<textarea type="text" name="dt5"' +
                        '" class="form-control" style="font-size:80%;" form="form_' + id + '">' + dt5 + '</textarea>';
}

function upd_good_reverse(id, cs, pg, clr_schemes, print_group){
   var clr_scheme ='[';
   for(i=0; i<clr_schemes.length; i++){
   clr_scheme += "'" + clr_schemes[i] +"',";
   }
   clr_scheme = clr_scheme.substring(0, clr_scheme.length - 1);
   clr_scheme += ']';
   var print_grp ='[';
   for(i=0; i<print_group.length; i++){
   print_grp += "'" + print_group[i] +"',";
   }
   print_grp = print_grp.substring(0, print_grp.length - 1);
   print_grp += ']';
   document.getElementById('row_'+id).setAttribute('onclick','javascript:upd_good(' + id + ', ' + clr_scheme +
                            ', ' + print_grp + ');');
   var art_ln = 'art_' + id;
   var nm_ln = 'nm_' + id;
   var cs_ln = 'cs_' + id;
   var pg_ln = 'pg_' + id;
   var dt1_ln = 'dt1_' + id;
   var dt1c_ln = 'dt1c_' + id;
   var dt2_ln = 'dt2_' + id;
   var dt2c_ln = 'dt2c_' + id;
   var dt3_ln = 'dt3_' + id;
   var dt3c_ln = 'dt3c_' + id;
   var dt4_ln = 'dt4_' + id;
   var dt4c_ln = 'dt4c_' + id;
   var dt5_ln = 'dt5_' + id;
   var dt5c_ln = 'dt5c_' + id;
   var art = document.getElementById(art_ln).textContent;
   var nm = document.getElementById(nm_ln).textContent;
   var dt1 = document.getElementById(dt1_ln).textContent;
   var dt2 = document.getElementById(dt2_ln).textContent;
   var dt3 = document.getElementById(dt3_ln).textContent;
   var dt4 = document.getElementById(dt4_ln).textContent;
   var dt5 = document.getElementById(dt5_ln).textContent;
   var dt1c = document.getElementById(dt1c_ln).checked;
   var dt2c = document.getElementById(dt2c_ln).checked;
   var dt3c = document.getElementById(dt3c_ln).checked;
   var dt4c = document.getElementById(dt4c_ln).checked;
   var dt5c = document.getElementById(dt5c_ln).checked;
   document.getElementById(dt1c_ln).disabled = true;
   document.getElementById(dt2c_ln).disabled = true;
   document.getElementById(dt3c_ln).disabled = true;
   document.getElementById(dt4c_ln).disabled = true;
   document.getElementById(dt5c_ln).disabled = true;
   document.getElementById(dt1c_ln).checked = dt1c;
   document.getElementById(dt2c_ln).checked = dt2c;
   document.getElementById(dt3c_ln).checked = dt3c;
   document.getElementById(dt4c_ln).checked = dt4c;
   document.getElementById(dt5c_ln).checked = dt5c;
   document.getElementById(pg_ln).innerHTML = pg;
   document.getElementById(cs_ln).innerHTML = cs;
   document.getElementById(art_ln).innerHTML = art;
   document.getElementById(nm_ln).innerHTML = nm;
   document.getElementById(dt1_ln).innerHTML = dt1;
   document.getElementById(dt2_ln).innerHTML = dt2;
   document.getElementById(dt3_ln).innerHTML = dt3;
   document.getElementById(dt4_ln).innerHTML = dt4;
   document.getElementById(dt5_ln).innerHTML = dt5;
}

function select_film(id){
   var pg_id_1 = 'pg_' + id + '_1';
   var pg_text_1 = document.getElementById(pg_id_1).value;
   var pg_id_2 = 'pg_' + id + '_2';
   var pg_text_2 = document.getElementById(pg_id_2).value;
   document.getElementById('modal_pg_id').value = id;
   document.getElementById('modal_pg_1').innerHTML = pg_text_1;
   document.getElementById('modal_pg_2').innerHTML = pg_text_2;
}

function save_to_film(){
    var film_data = document.getElementById('select_film').value;
    var flm_data = film_data.split('|');
    var id = document.getElementById('modal_pg_id').value;
    var film = flm_data[0];
    if(film!==0){
    var film_date = flm_data[2];
    var film_id = flm_data[1]
    }else{
    var film_date = document.getElementById('current_date').value;
    var film_id = document.getElementById('last_film').value
    }
    var filmout = 'filmout_' + id;
    document.getElementById(filmout).innerHTML = 'пленка: ' + film_id + ' от ' + film_date;
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
   var data_to_film = id + '_' + date + '_' + format + '_' + sent;
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
    const ids=document.querySelectorAll('[id*="collapse"]')
    for(var i in ids){
    if (ids[i].style.display ==='none'){
    ids[i].style.display = 'table-row-group';}
    else {ids[i].style.display = 'none';};
    }
}

function order_collapse(){
    const ids=document.querySelectorAll('[id*="collapse_ord"]')
    for(var i in ids){
    if (ids[i].style.display ==='none'){
    ids[i].style.display = 'table-row-group';}
    else {ids[i].style.display = 'none';};
    }
}

