function fillModalPg(pgObj){
    document.getElementById('pg_id').value = pgObj.id;
    document.getElementById('pg_cd').value = pgObj.dataset.code;
    document.getElementById('pg_nm').value = pgObj.dataset.name;
    document.getElementById('pg_ly').value = pgObj.dataset.layout;
    document.getElementById('pg_op').value = pgObj.dataset.options;
    document.getElementById('pg_width').value = pgObj.dataset.width;
    document.getElementById('pg_height').value = pgObj.dataset.height;
    document.getElementById('pg_width_initial').value = pgObj.dataset.swidth;
    document.getElementById('pg_height_initial').value = pgObj.dataset.sheight;
}

function clearModalPg(){
    document.getElementById('pg_id').value = null;
    document.getElementById('pg_cd').value = null;
    document.getElementById('pg_nm').value = null;
    document.getElementById('pg_ly').value = null;
    document.getElementById('pg_op').value = null;
    document.getElementById('pg_width').value = null;
    document.getElementById('pg_height').value = null;
    document.getElementById('pg_width_initial').value = null;
    document.getElementById('pg_height_initial').value = null;
}

function fillModalGoods(goodObj){
    document.getElementById('dt_it_id').value = goodObj.dataset.id;
    document.getElementById('dt_it_art').value = goodObj.dataset.art;
    document.getElementById('dt_it_nm').value = goodObj.dataset.name;
    document.getElementById('dt_it_clr').value = goodObj.dataset.color;
    document.getElementById('dt_it_pg').value = goodObj.dataset.pg;
    document.getElementById('dt1_nm').value = goodObj.dataset.det1nm;
    document.getElementById('flexCheck_det1').checked = goodObj.dataset.det1chck == 'True' ? true : false;
    document.getElementById('dt2_nm').value = goodObj.dataset.det2nm;
    document.getElementById('flexCheck_det2').checked = goodObj.dataset.det2chck == 'True' ? true : false;
    document.getElementById('dt3_nm').value = goodObj.dataset.det3nm;
    document.getElementById('flexCheck_det3').checked = goodObj.dataset.det3chck == 'True' ? true : false;
    document.getElementById('dt4_nm').value = goodObj.dataset.det4nm;
    document.getElementById('flexCheck_det4').checked = goodObj.dataset.det4chck == 'True' ? true : false;
    document.getElementById('dt5_nm').value = goodObj.dataset.det5nm;
    document.getElementById('flexCheck_det5').checked = goodObj.dataset.det5chck == 'True' ? true : false;
    document.getElementById('dt6_nm').value = goodObj.dataset.det6nm;
    document.getElementById('flexCheck_det6').checked = goodObj.dataset.det6chck == 'True' ? true : false;

}

function clearModalGoods(){
    document.getElementById('dt_it_id').value = null;
    document.getElementById('dt_it_art').value = null;
    document.getElementById('dt_it_nm').value = null;
    document.getElementById('dt_it_clr').value = null;
    document.getElementById('dt_it_pg').value = null;
    document.getElementById('dt1_nm').value = null;
    document.getElementById('flexCheck_det1').checked = false;
    document.getElementById('dt2_nm').value = null;
    document.getElementById('flexCheck_det2').checked = false;
    document.getElementById('dt3_nm').value = null;
    document.getElementById('flexCheck_det3').checked = false;
    document.getElementById('dt4_nm').value = null;
    document.getElementById('flexCheck_det4').checked = false;
    document.getElementById('dt5_nm').value = null;
    document.getElementById('flexCheck_det5').checked = false;
    document.getElementById('dt6_nm').value = null;
    document.getElementById('flexCheck_det6').checked = false;

}