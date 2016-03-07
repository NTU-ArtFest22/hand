'use strict';

var photosRef = new Firebase('https://ntuaf-hand.firebaseio.com/photos');

photosRef.on('child_added', function(childSnapshot, prevChildKey) {
  console.log(childSnapshot.key());
  var filename = 'images/photos/' + childSnapshot.key() + '.JPG';
  appendImg(filename);
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

  while(container.childElementCount > 4){
    container.removeChild(container.firstChild);
  }
}
