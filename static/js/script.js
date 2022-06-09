console.log(document.getElementById('groupA').rows[0].cells[1].offsetWidth);
console.log(document.getElementById('groupB').rows[0].cells[1].offsetWidth);
if(document.getElementById('groupA').rows[0].cells[1].offsetWidth>document.getElementById('groupB').rows[0].cells[1].offsetWidth){
  document.getElementById('groupB').rows[0].cells[1].width = document.getElementById('groupA').rows[0].cells[1].offsetWidth;
}
else{
  document.getElementById('groupA').rows[0].cells[1].width = document.getElementById('groupB').rows[0].cells[1].offsetWidth
}

function login () {
  var data = new FormData(document.getElementById("login"));
  fetch("/lin", { method:"POST", body:data })
  .then((res) => { return res.text(); })
  .then((txt) => {
    if (txt=="OK") { location.href = "../upload"; }
    else { alert(txt); }
  })
  .catch((err) => {
    alert("Server error - " + err.message);
    console.error(err);
  });
  return false;
}