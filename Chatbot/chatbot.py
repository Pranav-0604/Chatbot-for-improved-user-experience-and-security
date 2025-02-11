import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox

# Global variable to track conversation state
conversation_state = "greeting"  # Start with greeting state

# Function to handle user input and generate a bot response based on the state
def send_message():
    global conversation_state
    user_input = user_entry.get().strip()
    
    if user_input == "":
        return

    # Display user message on the right
    display_message("You", user_input, "right")
    
    # Start the typing simulation for the bot
    chat_window.config(state=tk.NORMAL)
    typing_message_index = chat_window.index(tk.END)
    chat_window.insert(tk.END, "\nBot is typing...", "typing")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

    # Use a delay to simulate typing
    window.after(1000, lambda: handle_bot_response(user_input, typing_message_index))

    # Clear the entry widget
    user_entry.delete(0, tk.END)

# Function to handle the bot's response after a delay
def handle_bot_response(user_input, typing_message_index):
    global conversation_state
    
    # Remove the typing indicator
    chat_window.config(state=tk.NORMAL)
    chat_window.delete(typing_message_index, tk.END)  # Remove the "Bot is typing..." message
    chat_window.config(state=tk.DISABLED)
    
    # Process the conversation based on the current state
    bot_response = handle_conversation(user_input)

    # Display bot response on the left
    display_message("Bot", bot_response, "left")

# Function to display messages in a "bubble" style
def display_message(sender, message, align):
    chat_window.config(state=tk.NORMAL)
    
    if align == "right":
        chat_window.insert(tk.END, f"\n{sender}: {message}\n", "right")
    else:
        chat_window.insert(tk.END, f"\n{sender}: {message}\n", "left")
    
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

# Conversation handler based on the current state
def handle_conversation(user_input):
    global conversation_state
    
    # Check for specific keywords related to number plates
    if "different number plate" in user_input.lower():
        conversation_state = "asking_for_image"
        return "I see that you've arrived with a different number plate. Could you please provide an image of it?"

    if conversation_state == "greeting":
        # Start by greeting the user and asking if they have a complaint
        conversation_state = "asking_complaint"
        return "Hello! Do you have any complaints or issues you'd like to report?"

    elif conversation_state == "asking_complaint":
        # If user says yes, ask for the complaint details
        if "yes" in user_input.lower():
            conversation_state = "awaiting_complaint"
            return "Please tell me more about your complaint."
        else:
            conversation_state = "end"
            return "Okay! If you ever have any issues, feel free to let me know. Have a great day!"

    elif conversation_state == "awaiting_complaint":
        # Acknowledge the complaint
        complaint_details = user_input  # Capture the complaint
        
        # Check if the complaint contains valid keywords; if not, end the conversation
        if not any(keyword in complaint_details.lower() for keyword in ["number", "plate", "registered", "vehicle", "complaint"]):
            conversation_state = "end"
            disable_chat()  # Disable chat options
            return "Thank you for your input. Unfortunately, I couldn't identify the specific issue. We will redirect you to the customer support page. This conversation will now end."

        # If valid complaint, ask for image
        conversation_state = "asking_for_image"
        return f"Thank you for letting us know. We've received your complaint: '{complaint_details}'. Could you please provide an image of the number plate?"

    elif conversation_state == "asking_for_image":
        # If user provides an image link or confirmation, handle that
        if "image" in user_input.lower() or "sent" in user_input.lower():
            conversation_state = "awaiting_response"
            return "Thank you for providing the image! We will look into the details right away."
        else:
            return "Please share the image of the number plate when you can."

    elif conversation_state == "end":
        # Conversation is done, prompt user to start over if necessary
        return "Thank you for reaching out! If you have any more issues, feel free to message me again."

    return "Sorry, I didn't understand that. Could you please rephrase?"

# Function to upload an image
def upload_image():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", ".jpg;.jpeg;.png;.gif")])
    if file_path:
        display_message("You", "Uploaded an image: " + file_path, "right")
        bot_response = "Thank you for uploading the image. We will look into the issue."
        display_message("Bot", bot_response, "left")
        
        # After a delay, ask for options (discount or cancel)
        window.after(2000, ask_for_options)  # Delay for 2 seconds before asking options

# Function to ask the user for options after an image upload
def ask_for_options():
    # Clear existing buttons if any
    for widget in bottom_frame.winfo_children():
        widget.grid_forget()

    # Create a label for selection options
    label = tk.Label(bottom_frame, text="Choose an option:", font=("Helvetica", 12))
    label.grid(row=0, column=0, pady=5)

    # Create a frame for vertical buttons
    options_frame = tk.Frame(bottom_frame, bg='#F5F5F5')
    options_frame.grid(row=1, column=0, sticky='nsew')

    # Create buttons for options
    discount_button = tk.Button(options_frame, text="Get Discount", command=apply_discount, bg="#FFC107", fg="white", font=("Helvetica", 10), width=20)
    cancel_button = tk.Button(options_frame, text="Cancel & Find New Ride", command=cancel_ride, bg="#FFC107", fg="white", font=("Helvetica", 10), width=20)
    
    discount_button.pack(pady=5)
    cancel_button.pack(pady=5)

# Function to clear option buttons after selection
def clear_option_buttons():
    for widget in bottom_frame.winfo_children():
        widget.grid_forget()  # Remove the buttons from the grid

# Function to handle discount selection
def apply_discount():
    display_message("Bot", "You will receive a 50% discount on your current ride! Hope we resolved the issue.", "left")
    clear_option_buttons()
    window.after(2000, ask_for_rating)  # Ask for rating after a short delay

# Function to handle cancellation selection
def cancel_ride():
    display_message("Bot", "You will be rerouted to the booking page with no cancellation charges. Hope we resolved the issue.", "left")
    clear_option_buttons()
    window.after(2000, ask_for_rating)  # Ask for rating after a short delay

# Function to ask for rating
def ask_for_rating():
    rating_label = tk.Label(bottom_frame, text="How would you rate your experience?", font=("Helvetica", 12))
    rating_label.grid(row=0, column=0, pady=5)

    # Create a frame for rating buttons
    rating_frame = tk.Frame(bottom_frame, bg="#F5F5F5")
    rating_frame.grid(row=1, column=0, pady=5)

    # Create buttons for rating (1 to 5)
    for i in range(1, 6):
        rating_button = tk.Button(rating_frame, text=str(i), command=lambda rating=i: submit_rating(rating), bg="#FFC107", fg="white", font=("Helvetica", 10), width=3)
        rating_button.grid(row=0, column=i-1, padx=5)  # Place buttons in the same row

    # Adjust grid weights for better alignment
    for i in range(5):
        rating_frame.grid_columnconfigure(i, weight=1)

# Function to submit the selected rating
def submit_rating(rating):
    display_message("Bot", f"Thank you for rating us {rating} out of 5!", "left")
    clear_rating_buttons()

# Function to clear rating buttons after submission
def clear_rating_buttons():
    for widget in bottom_frame.winfo_children():
        widget.grid_forget()  # Remove the buttons from the grid

# Function to disable chat options
def disable_chat():
    user_entry.config(state=tk.DISABLED)  # Disable the entry field
    send_button.config(state=tk.DISABLED)  # Disable the send button
    plus_button.config(state=tk.DISABLED)  # Disable the plus button

# Function to send an SOS alert
def send_sos():
    messagebox.showinfo("SOS Alert", "The alert has been sent to your emergency contacts and the authorities, and your location has been shared.")

# Create the main window
window = tk.Tk()
window.title("Chatbot")
window.geometry("400x600")
window.configure(bg="#F5F5F5")  # Light background

# Set the header frame with a less bright yellow color
header_frame = tk.Frame(window, bg='#FFEB3B', height=50, bd=0, relief='flat')  # Adjusted yellow color
header_frame.pack(fill=tk.X)

# Header label
header_label = tk.Label(header_frame, text="Rapido Complaint Bot", font=("Helvetica", 14, "bold"), bg='#FFEB3B', fg="black")
header_label.pack(pady=10, side=tk.LEFT)

# SOS button
sos_button = tk.Button(header_frame, text="SOS", command=send_sos, bg="red", fg="white", font=("Helvetica", 10))
sos_button.pack(pady=10, padx=10, side=tk.RIGHT)

# Create a scrolled text area for chat history
chat_window = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, bg="#FFFFFF", fg="black", font=("Helvetica", 10), bd=0)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Tag configuration for alignment and bubble style
chat_window.tag_configure("right", justify='right', background="#FFC107", spacing1=5, spacing3=5, lmargin1=20, lmargin2=20, foreground="black", font=("Helvetica", 10))
chat_window.tag_configure("left", justify='left', background="#FFFFFF", spacing1=5, spacing3=5, lmargin1=20, lmargin2=20, foreground="black", font=("Helvetica", 10))
chat_window.tag_configure("typing", justify='left', background="#FFFFFF", foreground="#777777", font=("Helvetica", 10, "italic"))

# Bottom frame for user input and buttons
bottom_frame = tk.Frame(window, bg="#F5F5F5")
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# User entry box
user_entry = tk.Entry(bottom_frame, font=("Helvetica", 12), width=30)
user_entry.grid(row=0, column=1, padx=10, pady=10)

# Create a send button with smaller size
send_button = tk.Button(bottom_frame, text="Send", command=send_message, bg="#FFC107", fg="white", font=("Helvetica", 10))
send_button.grid(row=0, column=2, padx=5, pady=10)

# Create a plus button
plus_button = tk.Button(bottom_frame, text="+", command=upload_image, bg="#FFC107", fg="white", font=("Helvetica", 10), width=2)
plus_button.grid(row=0, column=0, padx=5, pady=10)

# Bind the Enter key to send the message
user_entry.bind("<Return>", lambda event: send_message())

# Start the main loop with the initial greeting
if conversation_state == "greeting":
    display_message("Bot", "Hello! Do you have any complaints or issues you'd like to report?", "left")
    conversation_state = "asking_complaint"  # Change state after greeting

# Start the main loop
window.mainloop()
