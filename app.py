from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

def generate_lottery_numbers():
    # Generate lottery numbers like in the original game
    ticket_lottery = []
    ticket_lottery += random.sample(range(1, 6), k=1)
    ticket_lottery += random.sample(range(6, 11), k=1)
    ticket_lottery += random.sample(range(11, 16), k=1)
    ticket_lottery += random.sample(range(16, 21), k=1)
    ticket_lottery += random.sample(range(21, 26), k=1)
    ticket_lottery += random.sample(range(26, 31), k=1)
    ticket_lottery += random.sample(range(31, 36), k=1)
    ticket_lottery += random.sample(range(36, 41), k=1)
    return ticket_lottery

@app.route('/')
def index():
    ranges = [
        "1-5", "6-10", "11-15", "16-20", 
        "21-25", "26-30", "31-35", "36-40"
    ]
    return render_template('index.html', ranges=ranges)

@app.route('/play', methods=['POST'])
def play():
    try:
        # Get user selected numbers
        user_numbers = request.json.get('numbers', [])
        if len(user_numbers) != 8:
            return jsonify({'error': 'Please select one number from each column'})

        # Generate lottery numbers
        lottery_numbers = generate_lottery_numbers()

        # Calculate matches
        matches = []
        points = 0
        for user_num, lottery_num in zip(user_numbers, lottery_numbers):
            is_match = user_num == lottery_num
            matches.append({
                'user': user_num,
                'lottery': lottery_num,
                'match': is_match
            })
            if is_match:
                points += 1

        # Add message based on points
        message = ""
        if points == 8:
            message = "Congratulations! Perfect Match! 🎉"
        elif points >= 6:
            message = "Great job! 🌟"
        elif points >= 4:
            message = "Good try! 👍"
        else:
            message = "Better luck next time! 🍀"

        return jsonify({
            'lottery_numbers': lottery_numbers,
            'matches': matches,
            'points': points,
            'message': message
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 