// Function to initialize the game and display the starting information
function startGame() {
    // Hide the Start Game button
    document.querySelector('.start-button').style.display = 'none';

    // Show the game content
    document.getElementById('game-content').style.display = 'block';

    // Start the game by calling the Flask endpoint
    fetch('/start_game', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Display introduction and starting location only once
        document.getElementById("message").innerHTML = data.intro;
        document.getElementById("game-output").innerHTML = data.location_desc;
        document.getElementById("inventory").innerHTML = data.inventory_desc;
    });
}


// Function to handle directional movement (north, south, east, west)
function goDirection(direction) {
    fetch('/process_action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: `go ${direction}` })
    })
    .then(response => response.json())
    .then(data => {
        // Clear existing content before updating
        document.getElementById("game-output").innerHTML = ""; 
        document.getElementById("game-output").innerHTML = data.location_desc;
        document.getElementById("message").innerHTML = data.message;
        document.getElementById("inventory").innerHTML = data.inventory_desc;
    });
}

// Function to quit the game
function quitGame() {
    document.getElementById("message").innerHTML = "You have quit the game.";
    document.getElementById("game-output").innerHTML = "";
}

// Function to display inventory
function showInventory() {
    fetch('/process_action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'inventory' })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("inventory").innerHTML = data.inventory_desc;
        document.getElementById("message").innerHTML = data.message || "Inventory updated";
    });
}


function submitAction() {
    const action = document.getElementById("action").value.toLowerCase();
    fetch('/process_action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: action })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("game-output").innerHTML = data.location_desc;
        document.getElementById("message").innerHTML = data.message;
        document.getElementById("inventory").innerHTML = data.inventory_desc;
    });
}

function takeItem() {
    // Get the value from the input field
    const item = document.getElementById("item").value.trim();
    if (item === "") {
        document.getElementById("message").innerHTML = "Please specify an item to take.";
        return;
    }
    // Send the action to the backend
    fetch('/process_action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: `take ${item}` })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("game-output").innerHTML = data.location_desc;
        document.getElementById("message").innerHTML = data.message;
        document.getElementById("inventory").innerHTML = data.inventory_desc;
    });
}

