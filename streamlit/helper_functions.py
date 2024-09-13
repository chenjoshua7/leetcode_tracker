import re
from datetime import datetime, timedelta

def wrap_text(text, length=50):
    # Split text without breaking words unless necessary, handling ellipses and dashes
    words = re.split(r'(\s+)', text)  # Split by whitespace, keeping it as separators
    wrapped_lines = []
    current_line = []

    for word in words:
        # If adding the next word exceeds the length, wrap it
        if sum(len(w) for w in current_line) + len(word) > length:
            # Handle long words with dashes that exceed the length
            if '-' in word and len(word) > length:
                parts = word.split('-')
                for part in parts:
                    if current_line and sum(len(w) for w in current_line) + len(part) > length:
                        wrapped_lines.append(''.join(current_line))
                        current_line = [part + '-']
                    else:
                        current_line.append(part + '-')
                current_line[-1] = current_line[-1].rstrip('-')  # remove last dash
            else:
                wrapped_lines.append(''.join(current_line))
                current_line = [word]
        else:
            current_line.append(word)

    # Add any remaining content
    if current_line:
        wrapped_lines.append(''.join(current_line))

    # Join lines with <br> and avoid breaking ellipses
    return '<br>'.join(wrapped_lines).replace('...<br>', '...')

def get_current_streak(streak_data):
    # Get today's date and yesterday's date
    today = datetime.now().date()
    yesterday = (datetime.now() - timedelta(days=1)).date()
    
    # Extract the end_date of the most recent streak and convert it to a date object
    end_date = streak_data["end_date"][0].date()

    # Check if the most recent streak ended today or yesterday
    if end_date == today or end_date == yesterday:
        return streak_data["streak_length"][0]
    else:
        return 0
    
def get_daily_question(data):
    # Get today's date and yesterday's date
    today = datetime.now().date()
    
    top_row = data.iloc[0,:]
    
    if top_row["date"].date() == today:
        min, sec = divmod(int(top_row["time"]), 60)
        return f"""
            <div style='margin-bottom: 20px; width:100%; background-color: #2d2d2d; padding: 20px 30px; border-radius: 15px; 
                box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.1);'>
            <p style='font-size: 16px; font-weight: 600; color: #f9f9f9; margin-bottom: 5px;'>Today's Daily Challenge Problem</p>
            <p style='font-size: 15px; color: #dddddd; margin-bottom: 5px;'>{top_row["id"]}. {top_row["name"]}</p>
            <p style='font-size: 15px; color: #dddddd; margin-bottom: 5px;'>Completion Time: {min} minutes, {sec} seconds </p>
        </div>
        """
    else:
        return """
            <div style='margin-bottom: 20px; width:100%; background-color: #2d2d2d; padding: 20px 30px; border-radius: 15px; 
                box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.1);'>
            <p style='font-size: 16px; font-weight: 600; color: #f9f9f9; margin-bottom: 5px;'>Today's Daily Challenge Problem</p>
            <p>Daily Problem not completed... yet</p>
            </div>"""
