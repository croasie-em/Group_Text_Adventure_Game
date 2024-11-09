// Function to start the game when the button is clicked
function startGame() {
    // Hide the start button after the game starts
    document.getElementById('start-button').style.display = 'none';
    
    // Show the game controls and game log
    document.getElementById('game-controls').style.display = 'block';
    
    // Call Flask to start the game and get the intro text
    fetch('/start')
        .then(response => response.json())
        .then(data => {
            // Display intro text in the game log
            document.getElementById('game-log').innerText = data.intro;

            // Store the first location data so it can be shown after user clicks a direction
            window.currentLocationData = data.location;
        })
        .catch(error => {
            console.error('Error starting the game:', error);
        });
}

// Function to move the player (e.g., "Go North", "Go South", etc.)
function move(direction) {
    // Hide the intro text when the user clicks a direction (the game starts here)
    document.getElementById('game-log').innerHTML = ""; // Clear intro text

    // Fetch the new location based on the current location and the direction chosen
    fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction: direction })
    })
    .then(response => response.json())
    .then(data => {
        // Update the location and game log with the new data
        updateLocation(data);

        // Update the current location with the new data for future moves
        window.currentLocationData = data;
    })
    .catch(error => {
        console.error('Error moving:', error);
    });
}

// Function to take an item from the current location and add it to inventory
function takeItem() {
    // Ask the user for the item they want to take
    const item = prompt("Which item would you like to take?");

    // Send the item to Flask for processing
    fetch('/take', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item: item })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Update the game log with the success message
            document.getElementById('game-log').innerHTML += "<br>" + data.message;
        } else if (data.error) {
            // Display the error message
            document.getElementById('game-log').innerHTML += "<br>" + data.error;
        }
    })
    .catch(error => {
        console.error('Error taking item:', error);
    });
}

// Function to update the game log and location details
function updateLocation(data) {
    // Display location name and description
    document.getElementById('game-log').innerHTML += "<strong>" + data.name + "</strong><br>";
    document.getElementById('game-log').innerHTML += data.description + "<br>";
    
    // Display items available in the location
    if (data.items && data.items.length > 0) {
        document.getElementById('inventory').innerText = "Items here: " + data.items.join(', ');
    } else {
        document.getElementById('inventory').innerText = "No items here.";
    }
}