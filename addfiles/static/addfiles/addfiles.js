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