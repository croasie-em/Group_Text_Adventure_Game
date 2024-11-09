from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Game data
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

required_items = ['Backpack', 'Ancient Key', 'Candlestick', 'Silver Feather', 'Mystic Stone']
current_location = 'endless grove'
inventory = []

@app.route('/')
def index():
    ''' Renders the game HTML page '''
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start_game():
    ''' Initialize the game and display intro '''
    global current_location, inventory
    current_location = 'endless grove'
    inventory.clear()
    show_intro_text = (
        "You wake up on cold, damp ground, the earthy scent thick around you. "
        "Rising slowly, you find yourself trapped within towering hedges, their twisted branches woven tightly, creating walls too high to climb. "
        "Panic settles in as you search for any memory of how you got here—nothing. "
        "Your pockets are empty, and an eerie silence presses down, broken only by a faint, haunting melody echoing from somewhere deeper in the maze."
    )
    return jsonify({
        "intro": show_intro_text,
        "location": show_current_location(current_location)
    })

@app.route('/move', methods=['POST'])
def move():
    ''' Move the player in a specified direction '''
    global current_location
    direction = request.json.get('direction')
    new_location = locations[current_location]['directions'].get(direction)
    if new_location:
        current_location = new_location
        return jsonify(show_current_location(current_location))
    else:
        return jsonify({"error": "You cannot go that way"})

@app.route('/take', methods=['POST'])
def take():
    ''' Take an item and add it to inventory '''
    item = request.json.get('item')
    if item in locations[current_location].get('items', []):
        inventory.append(item)
        locations[current_location]['items'].remove(item)
        return jsonify({"message": f"You took the {item}."})
    else:
        return jsonify({"error": "That item isn't here."})

@app.route('/inventory', methods=['GET'])
def get_inventory():
    ''' Show current inventory '''
    if inventory:
        return jsonify({"inventory": inventory})
    else:
        return jsonify({"message": "Your inventory is empty."})

@app.route('/check', methods=['GET'])
def check():
    ''' Check if player has collected all required items '''
    missing_items = [item for item in required_items if item not in inventory]
    if not missing_items:
        return jsonify({"message": "You've gathered all the items needed to leave the forest. Are you ready to leave?"})
    else:
        return jsonify({"message": f"You still need: {', '.join(missing_items)}"})

def show_current_location(location):
    ''' Returns description of the current location'''
    loc = locations[location]
    items = loc.get('items', [])
    return {
        "name": loc['name'],
        "description": loc['description'],
        "items": items
    }

if __name__ == '__main__':
    app.run(debug=True)