// Permet de communiquer avec le server et la DataBase
function sendFingerprintToServer(fingerprint) {
  var name = document.getElementById('name-server').value;

  fetch('/store-fingerprint', {
    method: 'POST',

    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ fingerprint: fingerprint, name: name })
  })
  .then(response => {
    console.log('Fingerprint sent to server');
  })
  .catch(error => {
    console.error('Error sending fingerprint to server:', error);
  });
}

function getNameFromServer(fingerprint) {
  fetch('/get-name', {
    method: 'POST',

    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ fingerprint: fingerprint})
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      document.getElementById('name-value').innerText = data.name;
      console.log('Name retrieved from server:', data.name);
    })
    .catch(error => {
      console.error('Error retrieving name from server:', error);
      alert('Error retrieving name from server. Please try again later.');
    });
}



