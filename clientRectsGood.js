// Get fingerprint with getBoundingClientRect
function getBoundingRectsFingerprint() {
    var elements = document.getElementsByClassName('fingerprint-element');
    var GetfingerprintRects = [];
  
    for (var i = 0; i < elements.length; i++) {
      var rect = getClientRectsWithoutBlocking(elements[i]); // Utiliser une fonction alternative pour récupérer les rectangles de délimitation
      if (isValidRect(rect)) { // Vérifier si le rectangle est valide
        GetfingerprintRects.push({
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
  
    var json = JSON.stringify(GetfingerprintRects, null, 2);
    var hash = CryptoJS.SHA256(json).toString();
  
    return hash;
  }

  // Fonction alternative pour récupérer les rectangles de délimitation
function getClientRectsWithoutBlocking(element) {
    return element.getBoundingClientRect(); // Utiliser getBoundingClientRect au lieu de getClientRects
  }
  
  // Vérifier si le rectangle est valide (non vide)
  function isValidRect(rect) {
    return rect.width !== 0 || rect.height !== 0;
  }
  