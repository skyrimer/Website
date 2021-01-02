/* CLock */ 
clock();
function clock() {
  const date = new Date();
  let hours = date.getHours();
  let minutes = date.getMinutes();
  let seconds = date.getSeconds();
  
  const hour = (hours * 30) + (minutes / 2);
  const minute = minutes * 6;
  const second = seconds * 6;
  document.querySelector('.hour').style.transform = `rotate(${hour}deg)`
  document.querySelector('.minute').style.transform = `rotate(${minute}deg)`
  document.querySelector('.second').style.transform = `rotate(${second}deg)`

  hours = (hours < 10) ? "0" + hours : hours
  minutes = (minutes < 10) ? "0" + minutes : minutes
  seconds = (seconds < 10) ? "0" + seconds : seconds
  document.getElementById("Time").innerHTML =`Time - ${hours}:${minutes}:${seconds}`;
}
var inc = 1000;
setInterval(clock, inc);

Calendar()
function Calendar() {
  const lang = navigator.language
  const date = new Date();

  let dayNumber = date.getDate()
  let month = date.getMonth()
  let dayName = date.toLocaleString(lang, {weekday: 'long'})
  let monthName = date.toLocaleString(lang, {month: 'long'})
  let year = date.getFullYear()

  document.getElementById('monthName').innerHTML = monthName
  document.getElementById('dayName').innerHTML = dayName
  document.getElementById('dayNumber').innerHTML = dayNumber
  document.getElementById('year').innerHTML = year
}
