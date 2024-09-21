// Get fingerprint with getClientRect
function getRectsFingerprint() {
  var elements = document.getElementsByClassName('fingerprint-element');
  var fingerprint = [];

  for (var i = 0; i < elements.length; i++) {
    //var rect = elements[i].getClientRects()[0]; // utilisation naive qui se fait bloquer par Trace
    var rect = getClientRectsWithoutBlocking(elements[i]); // Utiliser une fonction alternative pour récupérer les rectangles de délimitation

    if (rect) {
      fingerprint.push({
        'x': rect.x,
        'y': rect.y,
        'width': rect.width,
        'height': rect.height,
        'top': rect.top,
        'right': rect.right,
        'bottom': rect.bottom,
        'left': rect.left
      });
    }
  }

  var json = JSON.stringify(fingerprint, null, 2);
  var hash = CryptoJS.SHA256(json).toString();

  return hash + json;
}

  // Fonction alternative pour récupérer les rectangles de délimitation
  function getClientRectsWithoutBlocking(element) {
    return element.getClientRects(); // Utiliser getClientRects
  }
  
  // Vérifier si le rectangle est valide (non vide)
  function isValidRect(rect) {
    return rect.width !== 0 || rect.height !== 0;
  }
  

