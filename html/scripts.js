/*
steve.a.mccluskey@gmail.com
No rights reserved.
*/

function getPiData() {
  // gets temp values from Raspberry Pi Model 3B+.

  nocache = "&nocache=" + Math.random() * 1000000;
  var request = new XMLHttpRequest();
  var server = "sensorValuesNew.json";

  request.open("GET", server, true);

  request.onreadystatechange = function () {
    if (request.readyState == 4 && request.status == 200) {
      var piValues = JSON.parse(request.responseText);
      console.log(piValues);

      document.getElementById("timeStamp").innerHTML =
        piValues.timestamp[0]["dateTime"];

      document.getElementById("livingRoomTemp").innerHTML =
        piValues.sensors["livingRoom"]["temp"];
      document.getElementById("livingRoomId").innerHTML =
        piValues.sensors["livingRoom"]["id"];

      document.getElementById("upstairsTemp").innerHTML =
        piValues.sensors["upstairs"]["temp"];
      document.getElementById("upstairsId").innerHTML =
        piValues.sensors["upstairs"]["id"];

      document.getElementById("basementTemp").innerHTML =
        piValues.sensors["basement"]["temp"];
      document.getElementById("basementId").innerHTML =
        piValues.sensors["basement"]["id"];

      document.getElementById("outsideTemp").innerHTML =
        piValues.sensors["outside"]["temp"];
      document.getElementById("outsideId").innerHTML =
        piValues.sensors["outside"]["id"];

      document.getElementById("garageTemp").innerHTML =
        piValues.sensors["garage"]["temp"];
      document.getElementById("garageId").innerHTML =
        piValues.sensors["garage"]["id"];

      document.getElementById("sammyDoorTemp").innerHTML =
        piValues.sensors["sammyDoor"]["temp"];
      document.getElementById("sammyDoorId").innerHTML =
        piValues.sensors["sammyDoor"]["id"];

      document.getElementById("atticTemp").innerHTML =
        piValues.sensors["attic"]["temp"];
      document.getElementById("atticId").innerHTML =
        piValues.sensors["attic"]["id"];

      document.getElementById("freezerTemp").innerHTML =
        piValues.sensors["freezer"]["temp"];
      document.getElementById("freezerId").innerHTML =
        piValues.sensors["freezer"]["id"];

      document.getElementById("steveRoomTemp").innerHTML =
        piValues.sensors["stevesRoom"]["temp"];
      document.getElementById("steveRoomId").innerHTML =
        piValues.sensors["stevesRoom"]["id"];

      document.getElementById("officeTemp").innerHTML =
        piValues.sensors["office"]["temp"];
      document.getElementById("officeId").innerHTML =
        piValues.sensors["office"]["id"];

      document.getElementById("guestRoomTemp").innerHTML =
        piValues.sensors["guestRoom"]["temp"];
      document.getElementById("guestRoomId").innerHTML =
        piValues.sensors["guestRoom"]["id"];

      document.getElementById("incubatorTemp").innerHTML =
        piValues.sensors["incubator"]["temp"];
      document.getElementById("incubatorId").innerHTML =
        piValues.sensors["incubator"]["id"];

      document.getElementById("fruitingTemp").innerHTML =
        piValues.sensors["fruiting"]["temp"];
      document.getElementById("fruitingId").innerHTML =
        piValues.sensors["fruiting"]["id"];
    } //end if.
  }; //end request.
  request.send(null);
  setTimeout("getPiData()", 3000);
} //end getPiData().

function getPiDoors() {
  //gets door values from Raspberry Pi Model B.
  nocache = "&nocache=" + Math.random() * 100000;
  var request = new XMLHttpRequest();
  var server = "getDoors.php";

  request.open("GET", server, true);
  request.onreadystatechange = function () {
    if (request.readyState == 4 && request.status == 200) {
      var piDoorValues = JSON.parse(request.responseText);
      console.log(piDoorValues);

      if (piDoorValues.doorSensors[0]["mainDoor"] == 1) {
        document.getElementById("mainDoor").src = "garageOpen.gif";
      } //end if.
      else {
        document.getElementById("mainDoor").src = "garageClosed.gif";
      } //end else.

      if (piDoorValues.doorSensors[0]["sideDoor"] == 1) {
        document.getElementById("sideDoor").src = "doorOpen.gif";
      } //end if.
      else if (piDoorValues.doorSensors[0]["sideDoor"] == 0) {
        if (piDoorValues.doorSensors[0]["sideDoorLock"] == 1) {
          document.getElementById("sideDoor").src = "doorUnlocked.gif";
        } //end if.
        else if (piDoorValues.doorSensors[0]["sideDoorLock"] == 0) {
          document.getElementById("sideDoor").src = "doorLocked.gif";
        } //end else if.
      } //end else if.
    } // end if.
  }; //end request.
  request.send(null);
  setTimeout("getPiDoors()", 1000);
} //end getPiDoors().

function getSammyDoorStatus() {
  //gets data from Raspberry Pi Model 3A+
  nocache = "&nocache=" + Math.random() * 10000;
  var request = new XMLHttpRequest();
  var server = "/getStatus";
  request.open("GET", server, true);

  request.onreadystatechange = function () {
    if (request.readyState == 4 && request.status == 200) {
      var sammyDoorStatus = JSON.parse(request.responseText);
      console.log(sammyDoorStatus);

      if (
        // door open, lock-in irrelevant:
        sammyDoorStatus.status[0]["doorStatus"] == 1 ||
        sammyDoorStatus.status[0]["doorState"] == 1
      ) {
        document.getElementById("sammyDoorImg").src = "/img/sammyDoorOpen.gif";
      } // end if.
      //
      //
      else if (
        // closed and locked :
        sammyDoorStatus.status[0]["doorStatus"] == 0 &&
        sammyDoorStatus.status[0]["lockStatus"] == 1
      ) {
        document.getElementById("sammyDoorImg").src = "img/sammyDoorLocked.gif";
      } // end if.
      //
      //
      else if (
        // closed and unlocked, lock-in enabled :
        sammyDoorStatus.status[0]["doorStatus"] == 0 &&
        sammyDoorStatus.status[0]["lockStatus"] == 0 &&
        sammyDoorStatus.status[0]["lockIn"] == 1
      ) {
        document.getElementById("sammyDoorImg").src =
          "img/sammyDoorUnLocked.gif";
      } //end if.
      //
      //
      else if (
        // closed and unlocked :
        sammyDoorStatus.status[0]["doorStatus"] == 0 &&
        sammyDoorStatus.status[0]["lockStatus"] == 0
      ) {
        document.getElementById("sammyDoorImg").src =
          "/img/sammyDoorClosed.gif";
      } //end if.
    } //end if.
  }; //end request.
  request.send(null);
  setTimeout("getSammyDoorStatus()", 1500);
} //end getArduinoIO().

function lockInEnable() {
  nocache = "&nocache=" + Math.random() * 100000;
  var request = new XMLHttpRequest();
  var server = "/lockIn?enable=enable";
  request.open("GET", server, true);
  request.onreadystatechange = function () {
    if (request.readyState == 4 && request.status == 200) {
      console.log(request.responseText);
    }
  };
  request.send();
} //end lockoutEnable.

function lockInDisable() {
  nocache = "&nocache=" + Math.random() * 100000;
  var request = new XMLHttpRequest();
  var server = "/lockIn?enable=disable";
  request.open("GET", server, true);
  request.onreadystatechange = function () {
    if (request.readyState == 4 && request.status == 200) {
      console.log(request.responseText);
    }
  };
  request.send();
} //end lockoutDisable.

function getPiWeather() {
  //gets weather data from Raspberry Pi.
  nocache = "&nocache=" + Math.random() * 100000;
  var request = new XMLHttpRequest();
  var server = "weatherData.json";

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
