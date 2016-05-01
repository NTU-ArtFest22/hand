'use strict';

var photosRef = new Firebase('https://ntuaf-hand.firebaseio.com/photos');

photosRef.orderByChild("timestamp").limitToLast(1).on('child_added', function(childSnapshot, prevChildKey) {
  var data = childSnapshot.val();

  appendImg(data.real_path);
});

function appendImg(src){
  var container = document.getElementById('container');
  var divElem = document.createElement('div');
  var imgElem = document.createElement('img');
  divElem.className = 'photo-box'
  imgElem.className = 'photo';
  imgElem.src = src;

  var qrAPI = 'http://chart.apis.google.com/chart?cht=qr&chl=' + src + '&chs=120x120';

  divElem.appendChild(imgElem);
  container.appendChild(divElem);
  document.styleSheets[0].insertRule('.photo-box:after { content: url(' + qrAPI + ') }', 0);

  while(container.childElementCount > 10){
    container.removeChild(container.firstChild);
  }
}
