
function split_maket(print_range){
    var number_items = print_range.length;
    for(i=0; i<number_items; i++){
        var line = 'chck_' + print_range[i][2] + '_' + print_range[i][9]
        if(document.getElementById(line).checked){
            if (print_range[i][8] === 'note' | print_range[i][8] === 'cover'){
                try {
                    document.getElementById(print_range[i][2] + '_' + print_range[i][9]).style.display='block';
                    }
                catch {};
                }
            else{
                try{
                    document.getElementById(print_range[i][2] + '_' + print_range[i][9]).style.display='inherit';}
                catch {}
            };
            var hd_line = print_range[i][2] + '_' + print_range[i][9] + '_';
            var hd_line1 = document.querySelectorAll("[id=" + CSS.escape(hd_line) + "]");
            for(var j = 0; j < hd_line1.length; j++) {hd_line1[j].style.display='table-row';}
        }
        else{
            try{
                document.getElementById(print_range[i][2] + '_' + print_range[i][9] ).style.display ='none';}
            catch{};
            var hd_line = print_range[i][2] + '_' + print_range [i][9] + '_';
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

function pen_position(id, len){
    var pen_pos = document.getElementById('pen_pos_' + id).value;
    for(var i=1; i<len+1; i++){
    if(pen_pos === i.toString()){
    document.getElementById(i+'_'+id).style.display = 'inline';
    document.getElementById(i+'_big_'+id).style.display = 'inline';}
    else{
    document.getElementById(i+'_'+id).style.display = 'none';
    document.getElementById(i+'_big_'+id).style.display = 'none';}
    }
}

function  block_button(){
    document.getElementById('but_imp_modal').disabled = true;
}

function setPantone(printGroup){
    var colorInput = printGroup.value;
    var printPlace = printGroup.dataset.place;
    var printNo = printGroup.dataset.id;
    var printProduct = printGroup.dataset.product;

    var pensArray = Array.from(document.querySelectorAll('[data-in="receiver"][data-number="' + printNo + '"]' +
        '[data-place="' + printPlace +'"][data-product="' + printProduct + '"]'));
    for (var i = 0; i < pensArray.length; i++){pensArray[i].value = colorInput}
}

function showTable(objInput){
    if(objInput.checked){
        document.getElementById('items_table').style.display = 'initial';}
    else{document.getElementById('items_table').style.display = 'none';}
}

function printSmallItems(printObj){
    if(printObj.checked){
        printObj.parentElement.parentElement.classList.add('d-print-none')
    }
    else {
        printObj.parentElement.parentElement.classList.remove('d-print-none')

    }
}

function selectAllItems(thisInput, selectId){
    var printItems = document.querySelectorAll('[data-in="checked"][data-product="' + selectId + '"]');
    if(thisInput.checked){
        printItems.forEach(makeChecked)
    }
    else {printItems.forEach(makeUnChecked)}
    printItems.forEach(selectItem);
}

function selectItem(thisInput){
    if(thisInput.checked) {
        document.querySelector('[data-id="' + thisInput.id + '"]').style.display = 'block'
    }
    else{
        document.querySelector('[data-id="' + thisInput.id + '"]').style.display = 'none'
    }
}

function makeChecked(item){
    item.checked = true;
}

function makeUnChecked(item){
    item.checked = false;
}

function setPantoneBack(counter, product5, product9, color){
    document.querySelector('[data-in="sender"][data-id="' + counter + '"]' +
        '[data-place="' + color +'"][data-product="' + product5 + '_' + product9 + '"]').value =
        document.querySelector('[data-in="receiver"][data-number="' + counter + '"]' +
        '[data-place="' + color +'"][data-product="' + product5 + '_' + product9 + '"]').value;

}