console.log(document.getElementById('groupA').rows[0].cells[1].offsetWidth);
console.log(document.getElementById('groupB').rows[0].cells[1].offsetWidth);
if(document.getElementById('groupA').rows[0].cells[1].offsetWidth>document.getElementById('groupB').rows[0].cells[1].offsetWidth){
  document.getElementById('groupB').rows[0].cells[1].width = document.getElementById('groupA').rows[0].cells[1].offsetWidth;
}
else{
  document.getElementById('groupA').rows[0].cells[1].width = document.getElementById('groupB').rows[0].cells[1].offsetWidth
}