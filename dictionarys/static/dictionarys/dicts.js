function fillModal(pgObj){
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

function clearModal(){
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