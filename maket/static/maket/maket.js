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

function upd_detail(detail_id, dt1_place, dt2_place, dt3_place, dt4_place, dt5_place, dt1_name,
        dt2_name, dt3_name, dt4_name, dt5_name, dt_code, dt_name, dt_color){
    var line_number = 'dtl_id_' + detail_id;

    var html_code0 = ('<input type="hidden" class="form-control" name="detail_id" value="{{ detail.id }}"><td>' +
        '<a href="javascript:upd_detail_reverse(' + detail_id + ',' +
        "'" + dt1_place + "', '" + dt2_place + "', '" + dt3_place + "', '" + dt4_place + "', '" +
        dt5_place + "', '" + dt1_name + "', '" + dt2_name + "', '" + dt3_name + "', '" +
        dt4_name + "', '" + dt5_name + "', '" + dt_code + "', '" + dt_name + "', '" + dt_color + "'" +
         ');"><button type="button" class="btn-sm btn-outline-secondary">Отм.</button></a></td>' +
         '<td style="width:10px"><input name="dt_it_nm" placeholder="Арт." value="' +  dt_code + '"></td>' +
         '<td><input name="dt_nm" placeholder="Название" value="' + dt_name + '"></td>' +
         '<td><input name="dt_clr" placeholder="Цвет" value="' + dt_color + '"></td>');

    if (dt1_place == 'True'){var checked = 'checked'} else {var checked = ''}
    var html_code1 = (''+
         '<td><input class="form-check-input" type="checkbox"' + checked + ' value="' + dt1_place +
         '" name="flexCheck_det1_k"></td>'+
         '<td><input name="dt1_nm" placeholder="Деталь 1" value="' + dt1_name + '"></td>');

    if (dt2_place == 'True'){var checked = 'checked'} else {var checked = ''}
    var html_code2 = (''+
         '<td><input class="form-check-input" type="checkbox"' + checked + ' value="' + dt2_place +
         '" name="flexCheck_det2_"></td>' +
         '<td><input name="dt2_nm" placeholder="Деталь 2" value="' + dt2_name + '"></td>');

    if (dt3_place == 'True'){var checked = 'checked'} else {var checked = ''}
    var html_code3 = (''+
         '<td><input class="form-check-input" type="checkbox"' + checked + ' value="' + dt3_place +
         '" name="flexCheck_det3_"></td>' +
         '<td><input name="dt3_nm" placeholder="Деталь 3" value="' + dt3_name + '"></td>');

    if (dt4_place == 'True'){var checked = 'checked'} else {var checked = ''}
    var html_code4 = (''+
         '<td><input class="form-check-input" type="checkbox"' + checked + ' value="' + dt4_place +
         '" name="flexCheck_det4_"></td>' +
         '<td><input name="dt4_nm" placeholder="Деталь 4" value="' + dt4_name + '"></td>');

    if (dt5_place == 'True'){var checked = 'checked'} else {var checked = ''}
    var html_code5 = (''+
         '<td><input class="form-check-input" type="checkbox"' + checked + ' value="' + dt5_place +
         '" name="flexCheck_det5_"></td>' +
         '<td><input name="dt5_nm" placeholder="Деталь 5" value="' + dt5_name + '"></td>');

    var html_code6 = ('<td><button type="submit" class="btn-sm btn-outline-primary">' +
    'Записать</button></td>');
    var html_code = html_code0 + html_code1 + html_code2 + html_code3 + html_code4 + html_code5 +html_code6;

    document.getElementById(line_number).innerHTML = html_code;
}

function upd_detail_reverse(detail_id, dt1_place, dt2_place, dt3_place, dt4_place, dt5_place, dt1_name,
        dt2_name, dt3_name, dt4_name, dt5_name, dt_code, dt_name, dt_color){
    var line_number = 'dtl_id_' + detail_id;
    var html_code0 = ('<input type="hidden" class="form-control" name="detail_id" value="' + detail_id + '"><td>' +
        '<a href="javascript:upd_detail(' +
         + detail_id + ", '" + dt1_place + "', '" + dt2_place + "', '" + dt3_place +
        "', '" + dt4_place + "', '" + dt5_place + "', '" + dt1_name + "', '" + dt2_name + "', '" + dt3_name +
        "', '" + dt4_name + "', '" + dt5_name + "', '" + dt_code + "', '" + dt_name + "', '" + dt_color + "'" +
        ');">' +
        '<button type="button" class="btn-sm btn-outline-primary">Ред.</button></a></td>' +
        '<td>' + dt_code + '</td>' +
        '<td>' + dt_name + '</td>' +
        '<td>' + dt_color + '</td>');
    if (dt1_place == 'True'){var checked = 'checked'} else {var checked = ''}
    var html_code1 = ('' +
        '<td><input class="form-check-input" type="checkbox"  disabled ' + checked + ' value="'+
        dt1_place + '"' + ' name="flexCheck_det1_"><td>' + dt1_name + '</td>');
    if (dt2_place == 'True'){var checked = 'checked'} else {var checked = ''}
    var html_code2 = ('' +
        '<td><input class="form-check-input" type="checkbox"  disabled value="'+ dt2_place + '"' +
        checked + ' name="flexCheck_det2_"><td>' + dt2_name + '</td>');
    if (dt3_place == 'True'){var checked = 'checked'} else {var checked = ''}
    var html_code3 = ('' +
        '<td><input class="form-check-input" type="checkbox"  disabled value="'+ dt3_place + '"' +
        checked + ' name="flexCheck_det3_"><td>' + dt3_name + '</td>');
    if (dt4_place == 'True'){var checked = 'checked'} else {var checked = ''}
    var html_code4 = ('' +
        '<td><input class="form-check-input" type="checkbox"  disabled value="'+ dt4_place + '"' +
        checked + ' name="flexCheck_det4_"><td>' + dt4_name + '</td>');
    if (dt5_place == 'True'){var checked = 'checked'} else {var checked = ''}
    var html_code5 = ('' +
        '<td><input class="form-check-input" type="checkbox"  disabled value="'+ dt5_place + '"' +
        checked + ' name="flexCheck_det5_"><td>' + dt5_name + '</td>');
    var html_code6 = '';
    var html_code = html_code0 +html_code1 + html_code2 + html_code3 + html_code4 + html_code5 +html_code6;

    document.getElementById(line_number).innerHTML = html_code;

}

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
    if (clr_schemes[i] == clr_in){var selected = 'selected'}else{var selected = ''};
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
    if (clr_schemes[i] == clr_in){var selected = 'selected'}else{var selected = ''};
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
    var line = 'chck_' + print_range[i][2]
    if(document.getElementById(line).checked){if (print_range[i][2] == 'prt_3A6' ||
     print_range[i][2] == 'prt_3A5' || print_range[i][2] == 'prt_3D5' || print_range[i][2] == 'prt_37'){
    document.getElementById(print_range[i][2]).style.display='block';}
    else{document.getElementById(print_range[i][2]).style.display='inherit';};
    var hd_line = print_range[i][2] + '_';
    var hd_line1 = document.querySelectorAll("[id=" + CSS.escape(hd_line) + "]");
    for(var j = 0; j < hd_line1.length; j++) {hd_line1[j].style.display='table-row';}
    }
    else{
    document.getElementById(print_range[i][2]).style.display ='none';
    var hd_line = print_range[i][2] + '_';
    var hd_line1 = document.querySelectorAll("[id=" + CSS.escape(hd_line) + "]");
    for(var j = 0; j < hd_line1.length; j++) {hd_line1[j].style.display='none';}
    }
}}

function chs_note(prt_3A6, note){
    var number_items = prt_3A6.length;
    try{if(document.getElementById(('chck_'+ note + '_all')).checked){
    for(i=0; i<number_items; i++){var itm_id = 'itm_' + note + '_' + prt_3A6[i][0];
    document.getElementById(itm_id).style.display='block';}
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
    if (document.getElementById(area).style.display =='none'){
    document.getElementById(area).style.display = 'initial';}
    else {document.getElementById(area).style.display = 'none';};
}

function colapse_(id){
    var area = 'collapse_' + id;
    if (document.getElementById(area).style.display =='none'){
    document.getElementById(area).style.display = 'table-row-group';}
    else {document.getElementById(area).style.display = 'none';};
}