/*
steve.a.mccluskey@gmail.com
No rights reserved.
*/

function getPiData() {
  // gets temp values from Raspberry Pi Model 3B+.

  nocache = "&nocache=" + Math.random() * 1000000;
  var request = new XMLHttpRequest();
  var server =
    "http://vulture2600.dyndns.org:5016/mount/data/sensorValuesNew.json";

  request.open("GET", server, true);

  request.onreadystatechange = function () {
    if (request.readyState == 4 && request.status == 200) {
      var piValues = JSON.parse(request.responseText);
      console.log(piValues);

      document.getElementById("timeStamp").innerHTML =
        piValues.timestamp[0]["dateTime"];

      document.getElementById("outsideTemp").innerHTML =
        piValues.sensors["outside"]["temp"];
      document.getElementById("outsideId").innerHTML =
        piValues.sensors["outside"]["id"];
    } //end if.
  }; //end request.
  request.send(null);
  setTimeout("getPiData()", 3000);
} //end getPiData().

function getPiWeather() {
  //gets weather data from Raspberry Pi.
  nocache = "&nocache=" + Math.random() * 100000;
  var request = new XMLHttpRequest();
  var server = "http://vulture2600.dyndns.org:5016/mount/data/weatherData.json";

  request.open("GET", server, true);

  request.onreadystatechange = function () {
    if (request.readyState == 4 && request.status == 200) {
      var piWeather = JSON.parse(request.responseText);
      console.log(piWeather);

      var utcDate = new Date(
        (piWeather.current["dt"] + piWeather.timezone_offset) * 1000
      );

      document.getElementById("weatherTimeStamp").innerHTML =
        utcDate.toUTCString();

      document.getElementById("highToday").innerHTML = Math.round(
        piWeather.daily[0]["temp"]["max"]
      );
      document.getElementById("lowToday").innerHTML = Math.round(
        piWeather.daily[0]["temp"]["min"]
      );
      document.getElementById("highTomorrow").innerHTML = Math.round(
        piWeather.daily[1]["temp"]["max"]
      );
      document.getElementById("lowTomorrow").innerHTML = Math.round(
        piWeather.daily[1]["temp"]["min"]
      );
      document.getElementById("humidity").innerHTML =
        piWeather.current["humidity"];
      document.getElementById("feelsLike").innerHTML = Math.round(
        piWeather.current["feels_like"]
      );

      var weatherIconCurrentURL = `http://openweathermap.org/img/wn/${piWeather.current["weather"][0]["icon"]}@2x.png`;

      var weatherIconTodayURL = `http://openweathermap.org/img/wn/${piWeather.daily[0]["weather"][0]["icon"]}@2x.png`;

      var weatherIconTomorrowURL = `http://openweathermap.org/img/wn/${piWeather.daily[1]["weather"][0]["icon"]}@2x.png`;

      document.documentElement.style.setProperty(
        "--weatherCurrentIcon",
        "url(" + weatherIconCurrentURL + ")"
      );
      document.documentElement.style.setProperty(
        "--weatherTodayIcon",
        "url(" + weatherIconTodayURL + ")"
      );
      document.documentElement.style.setProperty(
        "--weatherTomorrowIcon",
        "url(" + weatherIconTomorrowURL + ")"
      );

      document.getElementById("weatherCurrentDescription").innerHTML =
        piWeather.current["weather"][0]["main"];
      document.getElementById("descriptionToday").innerHTML =
        piWeather.daily[0]["weather"][0]["main"];
      document.getElementById("descriptionTomorrow").innerHTML =
        piWeather.daily[1]["weather"][0]["main"];

      document.getElementById("windSpeed").innerHTML = Math.round(
        piWeather.current["wind_speed"]
      );

      var windDirection = Math.round(piWeather.current["wind_deg"]) + 180;

      document.getElementById("arrowPos").style.transform =
        "rotate(" + windDirection + "deg)";

      document.getElementById("windGusts").innerHTML = Math.round(
        piWeather.daily[0]["wind_gust"]
      );
    }
  };
  request.send(null);
  setTimeout("getPiWeather()", 60000);
} //end getPiWeather().
