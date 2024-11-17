from flask import Flask, render_template, request, jsonify
import copy

app = Flask(__name__)
app.secret_key = '12345'

# Define initial game variables
initial_locations = {
    'endless grove': {
        'name': 'The Endless Grove',
        'description': 'The forest here stretches on with towering trees, their twisted branches interlocking above, blocking most of the light.',
        'directions': {'north': 'old oak', 'east': 'stone circle'},
        'items': ['Backpack']
    },
    'old oak': {
        'name': 'The Old Oak',
        'description': 'A massive oak tree dominates this part of the forest, its gnarled roots forming strange shapes in the ground.',
        'directions': {'south': 'endless grove', 'east': 'misty pond'},
        'items': ['Ancient Key']
    },
    'stone circle': {
        'name': 'The Stone Circle',
        'description': 'A ring of ancient stones, weathered by time, sits quietly in the forest. Moss covers each stone, and faint markings suggest they once held some ceremonial importance.',
        'directions': {'west': 'endless grove', 'north': 'misty pond'},
        'items': ['Candlestick']
    },
    'misty pond': {
        'name': 'The Misty Pond',
        'description': 'A small pond appears through the trees, its surface obscured by a layer of mist.',
        'directions': {'west': 'old oak', 'south': 'stone circle', 'east': 'fallen log'},
        'items': ['Silver Feather']
    },
    'fallen log': {
        'name': 'The Fallen Log',
        'description': 'A giant log lies across the forest floor, as though felled by some ancient force.',
        'directions': {'west': 'misty pond', 'north': 'forest edge'},
        'items': ['Mystic Stone']
    },
    'forest edge': {
        'name': 'The Forest Edge',
        'description': 'At last, the trees begin to thin, revealing the edge of the forest. The sky opens up, and a warm light shines from beyond the trees.',
        'directions': {'south': 'fallen log'},
        'items': []
    }
}

# Copy the initial state to locations for gameplay
locations = copy.deepcopy(initial_locations)

# Game state variables
required_items = ['Backpack', 'Ancient Key', 'Candlestick', 'Silver Feather', 'Mystic Stone']
current_location = 'endless grove'
inventory = []

# Game functions

def show_intro():
    """
    Function to show the introduction to the game.
    Currently, it does nothing, but it can be used to provide an introductory message in the future.
    """
    return

def show_current_location():
    """
    Function to return the description of the current location.
    Includes the location name, description, and any items present.
    """
    loc = locations[current_location]
    description = f"<h3>You are in {loc['name']}.</h3><p>{loc['description']}</p>"
    if loc['items']:
        items = "<p>You see the following items:</p><ul>" + "".join(f"<li>{item}</li>" for item in loc['items']) + "</ul>"
        description += items
    return description

def move_player(direction):
    """
    Function to move the player in the specified direction.
    Updates the current location if the direction is valid.
    Returns information about the new location and any messages.
    """
    global current_location
    new_location = locations[current_location]['directions'].get(direction)
    if new_location:
        current_location = new_location

        # Check if the player reaches the forest edge after collecting all items
        if current_location == 'forest edge' and check_victory():
            return {
                "location": show_current_location(),
                "message": "Congratulations! You have successfully navigated to the forest edge and completed your adventure! 🎉",
                "victory": True
            }

        return {
            "location": show_current_location(),
            "message": "",
            "victory": False
        }
    else:
        return {
            "location": show_current_location(),
            "message": "You cannot go that way.",
            "victory": False
        }

def take_item(item):
    """
    Function to take an item from the current location and add it to the player's inventory.
    Normalizes user input to handle case insensitivity.
    Updates the inventory and checks for victory conditions after taking an item.
    """
    loc = locations[current_location]
    
    # Normalize user input and items for comparison (case insensitive)
    item = item.lower()
    items_in_location = {i.lower(): i for i in loc['items']}  # Create a dictionary to map lowercase to original

    if item in items_in_location:
        original_item = items_in_location[item]
        inventory.append(original_item)
        loc['items'].remove(original_item)
        
        # Check for victory condition after taking an item
        if check_victory():
            return f"You have taken the {original_item}. You have collected all the items! Now, head to the forest edge to complete your journey."
        else:
            return f"You have taken the {original_item}."
    else:
        return "No such item here."

def show_inventory():
    """
    Function to display the player's current inventory.
    """
    if inventory:
        return "<p>Your inventory:</p><ul>" + "".join(f"<li>{item}</li>" for item in inventory) + "</ul>"
    else:
        return "Your inventory is empty."

def check_victory():
    """
    Function to check if the player has collected all required items.
    Returns True if all items are collected, otherwise False.
    """
    return set(inventory) == set(required_items)

# Routes
@app.route('/')
def index():
    """
    Route for the main page of the game.
    Renders the HTML template for the game interface.
    """
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    """
    Route to start or restart the game.
    Resets the current location, inventory, and locations to their initial states.
    Returns the initial game state as JSON.
    """
    global current_location, inventory, locations
    current_location = 'endless grove'
    inventory.clear()
    locations = copy.deepcopy(initial_locations)  # Reset locations to the initial state
    return jsonify({
        'intro': show_intro(),
        'location_desc': show_current_location(),
        'inventory_desc': show_inventory()
    })

@app.route('/process_action', methods=['POST'])
def process_action():
    """
    Route to handle player actions such as moving, taking items, or showing inventory.
    Returns the updated game state and any relevant messages as JSON.
    """
    global current_location
    action = request.json.get('action', '').lower()
    
    message = ""  # Default empty message
    victory = False

    if action.startswith("go"):
        direction = action.split()[-1]
        response = move_player(direction)
        message = response["message"]
        victory = response["victory"]
    elif action.startswith("take"):
        item = action.split(" ", 1)[1]
        message = take_item(item)
    elif action == "inventory":
        message = show_inventory()
    else:
        message = "Invalid action."

    return jsonify({
        'location_desc': show_current_location(),  # Always show the current location
        'inventory_desc': show_inventory(),
        'message': message,  # Empty if no special feedback
        'victory': victory
    })

@app.route('/quit_game', methods=['POST'])
def quit_game():
    """
    Route to quit the game.
    Resets the game state and returns a quit message.
    """
    global current_location, inventory, locations
    current_location = 'endless grove'  # Reset to initial location or any default
    inventory.clear()  # Clear the inventory
    locations = copy.deepcopy(initial_locations)  # Reset locations to the initial state
    return jsonify({
        'message': "You have quit the game. Thank you for playing!",
        'location_desc': '',
        'inventory_desc': ''
    })

if __name__ == '__main__':
    app.run(debug=True)
