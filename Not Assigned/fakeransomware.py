import tkinter as tk

def show_ransom_popup_fullscreen(ransom_amount, countdown_seconds=10):
    root = tk.Tk()
    root.title("Your Files Are Locked!")

    # Make the window fullscreen
    root.attributes('-fullscreen', True)
    root.configure(background='black')

    # Keep window on top and force focus
    root.attributes('-topmost', True)
    root.focus_force()

    label = tk.Label(root, font=("Arial", 30), fg="red", bg="black", justify="center")
    label.pack(expand=True)

    def format_time(seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def flash_background(count=0):
        colors = ['red', 'black']
        root.configure(background=colors[count % 2])
        label.configure(bg=colors[count % 2])
        if count < 20:
            root.after(100, flash_background, count + 1)
        else:
            root.configure(background='black')
            label.configure(bg='black', text="💥 BOOM! 💥\nYour files went BOOM.")

    def update_timer(remaining):
        if remaining >= 0:
            timer_msg = (
                "=== WARNING ===\n\n"
                "Your files have been encrypted!\n"
                f"To recover your files, you must pay ${ransom_amount} TrumpCoin ransom.\n\n"
                f"Time remaining: {format_time(remaining)}\n\n"
            )
            label.config(text=timer_msg)
            root.after(1000, update_timer, remaining - 1)
        else:
            flash_background()

    # Disable close button by overriding the window close protocol with a no-op
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    # Disable Alt+F4 and other window manager close shortcuts by ignoring keyboard interrupts
    def block_event(event):
        return "break"

    root.bind_all("<Alt-F4>", block_event)
    root.bind_all("<Control-w>", block_event)
    root.bind_all("<Command-w>", block_event)

    update_timer(countdown_seconds)
    root.mainloop()

if __name__ == "__main__":
    ransom_amount = input("Enter ransom amount (USD): ")
    if not ransom_amount.isdigit():
        print("Invalid amount. Using default $1000.")
        ransom_amount = "1000"
    show_ransom_popup_fullscreen(ransom_amount)
