/**
 * Created by pasha on 03.03.16.
 */

var socket = new WebSocket('ws://localhost:8765');
//socket.onopen = function() {
//  alert("Соединение установлено.");
//};

//socket.onclose = function(event) {
//  if (event.wasClean) {
//    alert('Соединение закрыто чисто');
//  } else {
//    alert('Обрыв соединения'); // например, "убит" процесс сервера
//  }
//  alert('Код: ' + event.code + ' причина: ' + event.reason);
//};

socket.onmessage = function(event) {
  alert("Получены данные " + event.data);
};

socket.onerror = function(error) {
  alert("Ошибка " + error.message);
};

document.forms.onsubmit = function() {
  var outgoingMessage = this.message.value;

  socket.send(outgoingMessage);
  return false;
};

// обработчик входящих сообщений
socket.onmessage = function(event) {
  var incomingMessage = event.data;
  showMessage(incomingMessage);
};

// показать сообщение в div#subscribe
function showMessage(message) {
  var messageElem = document.createElement('div');
  messageElem.appendChild(document.createTextNode(message));
  document.getElementById('subscribe').appendChild(messageElem);
}