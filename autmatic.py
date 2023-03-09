import gmpy2
import tkinter as tk
from tkinter import ttk

# Initialize high score variables
high_score_num = 0
high_score_steps = 0
high_scores = []

# root window
root = tk.Tk()
root.geometry('300x500')
root.title('Progressbar Demo')

# Create GUI elements
start_label = tk.Label(root, text="Start:")
start_label.pack()

start_entry = tk.Entry(root, width=10)
start_entry.pack()

end_label = tk.Label(root, text="End:")
end_label.pack()

end_entry = tk.Entry(root, width=10)
end_entry.pack()

max_num_label = tk.Label(root, text="Maximum number (optional):")
max_num_label.pack()

max_num_entry = tk.Entry(root, width=10)
max_num_entry.pack()

calculate_button = tk.Button(root, text="Calculate")
calculate_button.pack()

pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)
pb.pack()

output_label = tk.Label(root, text="Output:")
output_label.pack()

output_text = tk.Text(root, height=20, width=40)
output_text.pack()

high_score_label = tk.Label(
    root, text="Current leading number: 0\nMost steps until the 1 loop: 0")
high_score_label.pack()

high_scores_label = tk.Label(root, text="Top 100 high scores:")
high_scores_label.pack()

high_scores_text = tk.Text(root, height=10)
high_scores_text.pack()


# function to calculate 3n+1 sequence
def calculate():
    global high_score_num, high_score_steps, high_scores

    # clear output box
    output_text.delete('1.0', tk.END)

    try:
        start = int(start_entry.get())
        end = int(end_entry.get())
        max_num = int(
            max_num_entry.get()) if max_num_entry.get() else 100000000000000000000000000000000000000000000000000000000000000000000000000
    except ValueError:
        # handle invalid input
        output_text.insert(
            tk.END,
            "Invalid input. Please enter integers for Start, End, and Maximum number."
        )
        return
    for n in range(start, end + 1):
        # update progress bar value
        progress = (n - start) / (end - start) * 100
        pb['value'] = progress
        root.update()
        if n > max_num:
            break
        currentn = n
        steps = 0
        output_text.insert(tk.END, f"Sequence for {n}:\n")
        while n != 1:
            if gmpy2.c_mod(currentn, 2) == 0:
                high_score_num = currentn
                high_score_steps = steps
                high_scores.append((high_score_num, high_score_steps))

                # sort high scores in descending order by steps
                high_scores.sort(key=lambda x: x[1], reverse=True)

                # only keep the top 100 high scores
                if len(high_scores) > 1000000:
                    high_scores = high_scores[:1000000]
                break
            if n < currentn:
                high_score_num = currentn
                high_score_steps = steps
                high_scores.append((high_score_num, high_score_steps))

                # sort high scores in descending order by steps
                high_scores.sort(key=lambda x: x[1], reverse=True)

                # only keep the top 100 high scores
                if len(high_scores) > 1000000:
                    high_scores = high_scores[:1000000]
                break
            if gmpy2.c_mod(n, 2) == 0:
                n = gmpy2.c_div(n, 2)
            else:
                n = gmpy2.c_div((3 * n + 1), 2)
                steps += 1
            steps += 1
            output_text.insert(tk.END, f"{n}\n")

            # scroll output box to the bottom
            # if output_text.index('end-1c') != None:
            #     output_text.see('end-1c')

            # clear output box if it gets too big
            if len(output_text.get('1.0', 'end')) > 100000:
                output_text.delete('1.0', 'end')

        # record high score if applicable
            if n == 1:
                high_score_num = currentn
                high_score_steps = steps
                high_scores.append((high_score_num, high_score_steps))

                # sort high scores in descending order by steps
                high_scores.sort(key=lambda x: x[1], reverse=True)

                # only keep the top 100 high scores
            if len(high_scores) > 1000000:
                high_scores = high_scores[:1000000]

                # update high score display
        update_high_score_display()


# function to update high score display
def update_high_score_display():
    high_score_label.config(
        text=f"Last Number: {high_score_num}\n"
        f"Last numbers' steps until we known it is finite: {high_score_steps}")
    high_scores_text.delete('1.0', tk.END)
    for i, score in enumerate(high_scores):
        high_scores_text.insert(tk.END,
                                f"{i + 1}. {score[0]} ({score[1]} steps)\n")


# load high scores from file (if any)
try:
    with open('high_scores.txt', 'r') as f:
        for line in f:
            num, steps = line.strip().split(',')
            high_scores.append((int(num), int(steps)))
        high_scores.sort(key=lambda x: x[1], reverse=True)
        update_high_score_display()
except FileNotFoundError:
    pass


# save high scores to file (on exit)
def save_high_scores():
    with open('high_scores.txt', 'w') as f:
        for score in high_scores:
            f.write(f"{score[0]},{score[1]}\n")
    root.destroy()


# bind the calculate function to the button
calculate_button.config(command=calculate)

# bind the save_high_scores function to the window close button
root.protocol("WM_DELETE_WINDOW", save_high_scores)

root.mainloop()
