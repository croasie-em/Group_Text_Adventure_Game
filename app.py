from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = '12345'

# Define initial game variables
locations = {
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

# Game state variables
required_items = ['Backpack', 'Ancient Key', 'Candlestick', 'Silver Feather', 'Mystic Stone']
current_location = 'endless grove'
inventory = []

# Game functions
def show_intro():
    return

def show_current_location():
    loc = locations[current_location]
    description = f"<h3>You are in {loc['name']}.</h3><p>{loc['description']}</p>"
    if loc['items']:
        items = "<p>You see the following items:</p><ul>" + "".join(f"<li>{item}</li>" for item in loc['items']) + "</ul>"
        description += items
    return description

def move_player(direction):
    global current_location
    new_location = locations[current_location]['directions'].get(direction)
    if new_location:
        current_location = new_location

        # Check if the player reaches the forest edge after collecting all items
        if current_location == 'forest edge' and check_victory():
            return "Congratulations! You have successfully navigated to the forest edge and completed your adventure! 🎉"

        return show_current_location()
    else:
        return "You cannot go that way."


def take_item(item):
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
    if inventory:
        return "<p>Your inventory:</p><ul>" + "".join(f"<li>{item}</li>" for item in inventory) + "</ul>"
    else:
        return "Your inventory is empty."

def check_victory():
    return set(inventory) == set(required_items)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global current_location, inventory
    current_location = 'endless grove'
    inventory.clear()
    return jsonify({
        'intro': show_intro(),
        'location_desc': show_current_location(),
        'inventory_desc': show_inventory()
    })

@app.route('/process_action', methods=['POST'])
def process_action():
    global current_location
    action = request.json.get('action', '').lower()
    
    message = ""  # Default empty message
    if action.startswith("go"):
        direction = action.split()[-1]
        response = move_player(direction)
        
        # Set message only if there is a specific reason (like a failure)
        if response == "You cannot go that way.":
            message = response
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
        'message': message  # Empty if no special feedback
    })


@app.route('/quit_game', methods=['POST'])
def quit_game():
    global current_location, inventory
    current_location = 'endless grove'  # Reset to initial location or any default
    inventory.clear()  # Clear the inventory
    return jsonify({
        'message': "You have quit the game. Thank you for playing!",
        'location_desc': '',
        'inventory_desc': ''
    })

if __name__ == '__main__':
    app.run(debug=True)
