const backendUrl = 'http://localhost:8000/api';

async function fetchData() {
  try {
    const response = await fetch(`${backendUrl}/data`);
    if (!response.ok) {
      throw new Error('Network response was not good');
    }
    const data = await response.json();
    displayData(data);
  } catch (error) {
    console.error('Error:', error);
  }
}

async function sendData(data) {
  try {
    const response = await fetch(`${backendUrl}/data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Network response was not good');
    }
    const result = await response.json();
    console.log('Result:', result);
  } catch (error) {
    console.error('Error:', error);
  }
}

function displayData(data) {
  const outputElement = document.getElementById('output');
  outputElement.innerHTML = JSON.stringify(data, null, 2);
}

fetchData(); 
sendData();