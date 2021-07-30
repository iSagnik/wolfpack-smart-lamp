console.log("Hello")
document.addEventListener("DOMContentLoaded", function (event) {

  function toggleRed(button) {
    if (button.value == "Red Off") {
      button.value = "Red On";
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open("GET", "/?light=red&state=on", false); // false for synchronous request
      xmlHttp.send(null);
      //return xmlHttp.responseText;
    } else {
      button.value = "Red Off";
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open("GET", "/?light=red&state=off", false); // false for synchronous request
      xmlHttp.send(null);
    }


  }
  function toggleWhite(button) {
    if (button.value == "White Off") {
      button.value = "White On";
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open("GET", "/?light=white&state=on", false); // false for synchronous request
      xmlHttp.send(null);
      //return xmlHttp.responseText;
    } else {
      button.value = "White Off";
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open("GET", "/?light=white&state=off", false); // false for synchronous request
      xmlHttp.send(null);
    }
  }

  function showTime() {
    var date = new Date();
    var h = date.getHours(); // 0 - 23
    var m = date.getMinutes(); // 0 - 59
    var s = date.getSeconds(); // 0 - 59

    var session = "AM";

    if (h == 0) {
      h = 12;
    }

    if (h > 12) {
      h = h - 12;
      session = "PM";
    }

    h = (h < 10) ? "0" + h : h;
    m = (m < 10) ? "0" + m : m;
    s = (s < 10) ? "0" + s : s;

    var time = h + ":" + m + ":" + s + " " + session;
    document.getElementById("MyClockDisplay").innerText = time;
    document.getElementById("MyClockDisplay").textContent = time;


    setTimeout(showTime, 1000);

  }

  showTime();
});