import pandas as pd 
import tkinter as tk 
from tkinter import messagebox, simpledialog
import csv   #  comma seprated file 
import ttkbootstrap as ttkb  #  alias 
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from tkinter import ttk  #  tkinter > ttk > ttkbootstrap

user_logged_in = False
current_user_email = ""
user_section = None
main_window_ref = None


def refresh_user_section():
    global user_logged_in, user_section

    # Clear previous buttons
    for widget in user_section.winfo_children():
        widget.destroy()

    if user_logged_in:
        ttkb.Label(user_section, text="👤 Logged in", bootstyle="success", font=("Segoe UI", 12)).pack(side="left", padx=10)
        ttkb.Button(user_section, text="Logout", bootstyle="danger-outline", command=log_out).pack(side="left", padx=5)

    else:
        ttkb.Button(user_section, text="Log In", bootstyle="success-outline", width=15, command=logIn).pack(side="left", padx=5)
        ttkb.Button(user_section, text="Sign Up", bootstyle="primary-outline", width=15, command=signUp).pack(side="left", padx=5)


def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the window geometry to center it
    window.geometry(f'{width}x{height}+{x}+{y}')


def mainWindow():
    global user_logged_in, user_section, main_window_ref, tree, book_data
    root = ttkb.Window(themename="cosmo")  #  create a window
    main_window_ref = root
    root.state("zoomed")
    root.title("PyBrary - Library Book Finder")

    container = ttkb.Frame(root, padding=20)
    container.pack(fill="both", expand=True)

    # Top Frame
    top_frame = ttkb.Frame(container)
    top_frame.pack(fill='x', pady=10)

    header = ttkb.Label(top_frame, text="📚 Welcome to PyBrary", font=("Segoe UI", 32, "bold"), bootstyle="dark")
    header.pack(side="left")

    user_section = ttkb.Frame(top_frame)
    user_section.pack(side="right")

    refresh_user_section()

    # Load CSV
    book_data = pd.read_csv("books.csv")
    # data cleaning
    book_data.drop_duplicates(inplace=True)
    # book_data = book_data.drop_duplicates(subset='Title', keep='first')

    # Apply font and row height to Treeview
    style = Style()
    style.configure("Treeview", font=("Segoe UI", 10, "bold"), rowheight=30)
    style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"))

     # Update Treeview
    def update_tree(filtered_data):
        tree.delete(*tree.get_children())
        for _, row in filtered_data.iterrows():
            tree.insert("", "end", values=tuple(row[col] for col in ("Title", "Author", "Year", "Genre", "Price", "Rating")))
    
    
    # Search Logic
    def perform_search():
        query = search_entry.get().strip().lower()
        if query == "" or query == "search for a book by title, author...":
            update_tree(book_data)
        else:
            result = book_data[book_data.apply(
                lambda row: query in row.astype(str).str.lower().to_string(), axis=1)]
            update_tree(result)

        
    # Search Bar
    search_frame = ttkb.Frame(container, padding=(10, 15))
    search_frame.pack(fill='x')
    search_entry = ttkb.Entry(search_frame, width=60, font=("Segoe UI", 14))
    search_entry.insert(0, "Search for a book by title, author...")
    search_entry.pack(side="left", padx=(0, 10))
    search_button = ttkb.Button(search_frame, text="🔍 Search", bootstyle="dark", width=12, command=perform_search) 
    search_button.pack(side="left")

    # Book Table
    display_frame = ttkb.Frame(container)
    display_frame.pack(fill='both', expand=True, pady=20)

    tree = ttkb.Treeview(display_frame, columns=("Title", "Author", "Year", "Genre", "Price", "Rating"),
                         show="headings", bootstyle="primary", height=15)
    for col in ("Title", "Author", "Year", "Genre", "Price", "Rating"):
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='center')
    tree.pack(fill="both", expand=True)

   

    # Book Actions + Help/About
    action_frame = ttkb.Labelframe(container, text="Book Actions", padding=20, bootstyle="primary")
    action_frame.pack(fill='x', pady=30)

    ttkb.Button(action_frame, text="💰 Buy", bootstyle="success", width=25, command=buy).pack(side="left", padx=5, pady=5)
    ttkb.Button(action_frame, text="📚 Borrow", bootstyle="primary", width=25, command=borrow).pack(side="left", padx=5, pady=5)
    ttkb.Button(action_frame, text="⭐ Rate", bootstyle="secondary", width=25, command=rate).pack(side="left", padx=5, pady=5)

    ttkb.Button(action_frame, text="❓ Help", bootstyle="primary-outline", width=15, command=help).pack(side="right", padx=5, pady=5)
    ttkb.Button(action_frame, text="ℹ️ About", bootstyle="primary-outline", width=15, command=about).pack(side="right", padx=5, pady=5)
    root.mainloop()


def logIn():
    global user_logged_in, current_user_email
    log_root = ttkb.Toplevel()
    log_root.title("Log In")
    log_root.geometry("400x450")
    log_root.resizable(False, False)
    center_window(log_root, 400, 450)
    
    ttkb.Label(log_root, text="🔐 Log In", font=("Arial", 34, "bold"), bootstyle="primary").pack(pady=(30, 10))
    form = ttkb.Frame(log_root, padding=20)
    form.pack(pady=10)

    ttkb.Label(form, text="Email", font=("Segoe UI", 12)).pack(anchor="w", pady=(10, 5))
    email_entry = ttkb.Entry(form, width=30, font=("Segoe UI", 12))
    email_entry.pack()

    ttkb.Label(form, text="Password", font=("Segoe UI", 12)).pack(anchor="w", pady=(15, 5))
    password_entry = ttkb.Entry(form, width=30, font=("Segoe UI", 12), show="•")
    password_entry.pack()

    def log_check():
        global user_logged_in, current_user_email

        password = password_entry.get().strip() 
        email = email_entry.get().strip().lower()
    
        if not email or not password:   
            messagebox.showerror("Error", "Please fill in both email and password")
            return

        try:  
            with open("users.csv", "r", newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['email'].lower() == email and row['password'] == password:
                        user_logged_in = True
                        current_user_email = email
                        messagebox.showinfo("Success", "Login successful!")
                        log_root.destroy()
                        refresh_user_section()
                        return
                messagebox.showerror("Error", "Invalid email or password")

        except FileNotFoundError:
            messagebox.showerror("Error", "User database not found")
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")

    ttkb.Button(form, text="Log In", bootstyle="success", width=20, command=log_check).pack(pady=25)
    ttkb.Label(form, text="Forgot Password?", font=("Segoe UI", 10, "underline"), foreground="blue").pack(pady=(0, 10))
    ttkb.Label(form, text="Don't have an account? Sign Up", font=("Segoe UI", 10), foreground="gray").pack()


def signUp():
    sign_root = ttkb.Toplevel()
    sign_root.title("Sign Up")
    sign_root.geometry("400x450")
    sign_root.resizable(False, False)
    center_window(sign_root, 400, 450)

    ttkb.Label(sign_root, text="🔐 Sign Up", font=("Arial", 34, "bold"), bootstyle="primary").pack(pady=(30, 10))
    form = ttkb.Frame(sign_root, padding=20)
    form.pack(pady=10)

    ttkb.Label(form, text="Email", font=("Segoe UI", 12)).pack(anchor="w", pady=(10, 5))
    email_s_entry = ttkb.Entry(form, width=30, font=("Segoe UI", 12))
    email_s_entry.pack()

    ttkb.Label(form, text="Password", font=("Segoe UI", 12)).pack(anchor="w", pady=(15, 5))
    password_s_entry = ttkb.Entry(form, width=30, font=("Segoe UI", 12), show="•")
    password_s_entry.pack()

    def sign_check():
        password = password_s_entry.get().strip()
        email = email_s_entry.get().strip().lower()
        
        # Ensure both fields are filled
        if not email or not password:
            messagebox.showerror("Error", "Please fill in both email and password")
            return
        
        # Check if email already exists
        try:
            with open("users.csv", "r", newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["email"].lower() == email:
                        messagebox.showerror("Error", "Email already exists!")
                        return

        except FileNotFoundError:
            # Handle case if the users.csv file does not exist
            pass
        
        # Save new user data to "users.csv"
        try:
            with open("users.csv", "a", newline='', encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["email", "password"])
                if file.tell() == 0:  # If the file is empty, write the header first
                    writer.writeheader()
                writer.writerow({"email": email, "password": password})
                
            messagebox.showinfo("Success", "Account created successfully!")
            sign_root.destroy()  # Close sign-up window

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create account: {str(e)}")

    # Sign Up button
    ttkb.Button(form, text="Sign Up", bootstyle="success", width=20, command=sign_check).pack(pady=25)


def log_out():
    global user_logged_in, current_user_email
    user_logged_in = False
    current_user_email = ""
    messagebox.showinfo("Log Out", "You have been logged out.")
    refresh_user_section()
    
    
def about():
    about_root = ttkb.Toplevel()
    about_root.geometry("650x600")  # width, length  
    about_root.title("About Us")
    about_root.resizable(False, False)
    center_window(about_root, 650, 600)
    about_root.configure(padx=20, pady=20)

    # Title
    ttkb.Label(
        about_root,
        text="About Us",
        font=("Segoe UI", 36, "bold"),
        bootstyle="primary"
    ).pack(pady=(20, 10))

    # Subtitle
    ttkb.Label(
        about_root,
        text="Meet the GlitchWave Team behind PyBrary",
        font=("Segoe UI", 12),
        bootstyle="secondary"
    ).pack(pady=(0, 20))

    # Styled Frame for the about content
    content_frame = ttkb.Labelframe(
        about_root,
        text="WHO ARE WE",
        bootstyle="primary",
        padding=10
    )
    content_frame.pack(fill="both", expand=True)

    # Text displayed as Label inside frame
    about_text = (
    "🚩 GlitchWave Team\n"
    "• Alaa Gabr\n"
    "• Alaa Basem\n"
    "• Abdelrahman Sherif\n"
    "• Omr Abdelaziz\n"
    "• Omr Eladly\n\n"

    "🔧 Challenges We Faced:\n"
    "- Designing a dynamic and modern GUI layout with real usability.\n"
    "- Handling login/logout functionality reliably.\n"
    "- Managing and validating user data using CSV files.\n"
    "- Implementing a live book search that updates the interface in real time.\n\n"

    "🐍Tools & Technologies:\n"
    "- Python\n"
    "- Tkinter & ttkbootstrap (for GUI)\n"
    "- CSV for data storage\n"
    "- Custom styles and responsive layouts"
)



    ttkb.Label(
        content_frame,
        text=about_text,
        wraplength=580,
        font=("Segoe UI", 12),
        justify="left",
        anchor="w",              
        padding=0              
    ).pack(fill="both", expand=True, anchor="w", padx=0)
    

def help():
    help_root = ttkb.Toplevel()
    help_root.geometry("700x680")
    help_root.title("Help - PyBrary User Guide")
    help_root.resizable(False, False)
    center_window(help_root, 700, 680)
    help_root.configure(padx=20, pady=20)

    # Header Label
    header = ttkb.Label(
        help_root,
        text="📚 Welcome to PyBrary - Library Book Finder",
        font=("Helvetica", 18, "bold"),
        bootstyle="primary"
    )
    header.pack(pady=(10, 10))

    # Content Frame
    content_frame = ttkb.Labelframe(
        help_root,
        text="How To Use PyBrary",
        bootstyle="primary",
        padding=15
    )
    content_frame.pack(fill="both", expand=True, pady=(10, 10))

    help_text = (
        "🟦 Login / Signup\n"
        " - To use the app, first create an account by clicking 'Sign Up'.\n"
        " - If you already have an account, click 'Login' and enter your credentials.\n\n"
        "🟩 Search for Books\n"
        " - Use the search bar at the top of the interface.\n"
        " - You can search for books by title, author, or genre.\n"
        " - Click 'Search' to display the results in the table below.\n\n"
        "🟨 Interacting with Books\n"
        " - Buy Book: Select a book from the list and click the 'Buy' button.\n"
        " - Borrow Book: Click 'Borrow' to borrow the selected book (only one at a time).\n"
        " - Rate Book: Once logged in, you can rate books you've read.\n\n"
        "🟪 User Menu\n"
        " - After logging in, your log in sign will appear at the top.\n"
        " - From the log out button, you can log out.\n\n"
        "💡 Tips\n"
        " - Use the help menu anytime to get assistance on using the app.\n\n"
        "🎯 Common Issues\n"
        " - If you encounter any errors or bugs, try restarting the app.\n"
        " - For further assistance, feel free to contact support.\n\n"
        "📞 Contact Support\n"
        " - If you have any questions or need assistance, reach out to support via email.\n"
        " - email : engalaagabr@hotmail.com"
    )

    instructions = ttkb.Label(
        content_frame,
        text=help_text,
        justify="left",
        wraplength=600,
        font=("Segoe UI", 10)
    )
    instructions.pack(anchor="w")


def buy():
    if not user_logged_in:
        messagebox.showwarning("Login Required", "You must be logged in to buy a book.")
        return

    selected_item = tree.focus()
    if not selected_item:
        messagebox.showinfo("No Selection", "Please select a book to buy.")
        return

    book = tree.item(selected_item, 'values')[0]  
    messagebox.showinfo("Purchase Successful", f"You have bought '{book}'.\nThank you!")


def rate():
    if not user_logged_in:
        messagebox.showwarning("Login Required", "You must be logged in to rate a book.")
        return

    selected_item = tree.focus()
    
    if not selected_item:
        messagebox.showinfo("No Selection", "Please select a book to rate.")
        return

    # Get the book title (or other info if needed)
    book_title = tree.item(selected_item, 'values')[0]

    # Ask for rating input
    rating = simpledialog.askfloat("Rate Book", f"Enter your rating for '{book_title}' (0.0 to 5.0):", minvalue=0.0, maxvalue=5.0)
    
    if rating is None:
        return  # User cancelled the input

    # Update the rating in books_data (if available) and tree
    for book in book_data[0]:
        if book['title'] == book_title:
            book['rating'] = rating

    # Update the Treeview row
    tree.item(selected_item, values=(book['title'], book['author'], book['genre'], rating))

    messagebox.showinfo("Success", f"You rated '{book_title}' {rating} stars!")


def borrow():
    if not user_logged_in:
        messagebox.showwarning("Login Required", "You must be logged in to borrow a book.")
        return

    selected_item = tree.focus()
    if not selected_item:
        messagebox.showinfo("No Selection", "Please select a book to borrow.")
        return

    book_info = tree.item(selected_item, 'values')
    book_title = book_info[0]  

    messagebox.showinfo("Book Borrowed", f"You have borrowed '{book_title}'. Enjoy reading!")

mainWindow()

# Thanks 