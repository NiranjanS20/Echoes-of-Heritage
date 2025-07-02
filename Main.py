import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime
import os
from typing import Dict, List, Any

class HeritageApp:
    def __init__(self, root):  # Fixed method name here
        self.root = root
        self.root.title("Echoes of Heritage")
        self.root.geometry("800x600")
        
        # Data storage paths
        self.data_dir = "heritage_data"
        self.projects_file = os.path.join(self.data_dir, "projects.json")
        self.contacts_file = os.path.join(self.data_dir, "contacts.json")
        
        # Initialize data storage
        self.initialize_storage()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Store references to dynamic elements
        self.events_frame = None
        self.events_list = None
        self.project_list = None
        
        # Create tabs
        self.create_home_tab()
        self.create_projects_tab()
        self.create_documentation_tab()
        self.create_contact_tab()

    def initialize_storage(self):
        """Initialize file-based storage system"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Initialize projects file
        if not os.path.exists(self.projects_file):
            self.save_data([], self.projects_file)
        
        # Initialize contacts file
        if not os.path.exists(self.contacts_file):
            self.save_data([], self.contacts_file)

    def save_data(self, data: List[Dict[str, Any]], file_path: str):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def create_home_tab(self):
        """Create the home tab with mission statement and overview"""
        home_frame = ttk.Frame(self.notebook)
        self.notebook.add(home_frame, text="Home")
        
        # Create a canvas with scrollbar for the home tab
        canvas = tk.Canvas(home_frame)
        scrollbar = ttk.Scrollbar(home_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = ttk.Label(
            scrollable_frame,
            text="Echoes of Heritage",
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=20)
        
        # Mission Statement
        mission_text = """
        Echoes of Heritage is deeply committed to cultural preservation 
        and heritage documentation. We strive to empower communities 
        worldwide to safeguard their traditions and stories. Through 
        innovative digital solutions, we aim to make cultural learning 
        engaging and accessible to a global audience.
        """
        mission_label = ttk.Label(
            scrollable_frame,
            text=mission_text,
            wraplength=600,
            justify="center"
        )
        mission_label.pack(pady=20)
        
        # Services Frame
        services_frame = ttk.LabelFrame(scrollable_frame, text="Our Services")
        services_frame.pack(padx=10, pady=10, fill="x")
        
        services = [
            ("Language Documentation", "Documenting endangered languages for future generations"),
            ("Traditional Knowledge", "Preserving ancient practices and wisdom"),
            ("Cultural Storytelling", "Bringing cultural narratives to life")
        ]
        
        for title, desc in services:
            service_frame = ttk.Frame(services_frame)
            service_frame.pack(padx=5, pady=5, fill="x")
            
            ttk.Label(
                service_frame,
                text=title,
                font=("Helvetica", 12, "bold")
            ).pack()
            
            ttk.Label(
                service_frame,
                text=desc,
                wraplength=500
            ).pack()

        # Events Section
        self.events_frame = ttk.LabelFrame(scrollable_frame, text="Upcoming Events & Projects")
        self.events_frame.pack(padx=10, pady=10, fill="x")
        
        # Create Treeview for events
        self.events_list = ttk.Treeview(
            self.events_frame,
            columns=("Name", "Category", "Date"),
            show="headings",
            height=5
        )
        
        self.events_list.heading("Name", text="Project Name")
        self.events_list.heading("Category", text="Category")
        self.events_list.heading("Date", text="Date Added")
        
        self.events_list.pack(padx=5, pady=5, fill="x")
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load initial events
        self.refresh_events()

    def refresh_events(self):
        """Refresh the events list on the home page"""
        if self.events_list:
            # Clear current items
            for item in self.events_list.get_children():
                self.events_list.delete(item)
            
            # Load and display projects
            projects = self.load_data(self.projects_file)
            # Sort projects by date (newest first)
            projects.sort(key=lambda x: x["date_added"], reverse=True)
            
            for project in projects:
                self.events_list.insert(
                    "",
                    "end",
                    values=(
                        project["name"],
                        project["category"],
                        project["date_added"].split("T")[0]
                    )
                )

    def create_projects_tab(self):
        """Create the projects tab for managing heritage projects"""
        projects_frame = ttk.Frame(self.notebook)
        self.notebook.add(projects_frame, text="Projects")
        
        # Project Entry Form
        entry_frame = ttk.LabelFrame(projects_frame, text="Add New Project")
        entry_frame.pack(padx=10, pady=5, fill="x")
        
        # Project Name
        ttk.Label(entry_frame, text="Project Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(entry_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Project Category
        ttk.Label(entry_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        category_combo = ttk.Combobox(
            entry_frame,
            values=["Language", "Traditional Knowledge", "Cultural Story"]
        )
        category_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Project Description
        ttk.Label(entry_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        desc_text = scrolledtext.ScrolledText(entry_frame, height=4)
        desc_text.grid(row=2, column=1, padx=5, pady=5)
        
        def add_project():
            """Add new project to storage and update displays"""
            if not name_entry.get() or not category_combo.get():
                messagebox.showwarning("Warning", "Please fill in all required fields.")
                return
                
            project = {
                "name": name_entry.get(),
                "category": category_combo.get(),
                "description": desc_text.get("1.0", tk.END).strip(),
                "date_added": datetime.now().isoformat()
            }
            
            projects = self.load_data(self.projects_file)
            projects.append(project)
            self.save_data(projects, self.projects_file)
            
            # Clear form
            name_entry.delete(0, tk.END)
            category_combo.set("")
            desc_text.delete("1.0", tk.END)
            
            # Refresh both project list and events on home page
            self.display_projects()
            self.refresh_events()
            messagebox.showinfo("Success", "Project added successfully!")
        
        ttk.Button(
            entry_frame,
            text="Add Project",
            command=add_project
        ).grid(row=3, column=1, pady=10)
        
        # Project List
        list_frame = ttk.LabelFrame(projects_frame, text="Current Projects")
        list_frame.pack(padx=10, pady=5, fill="both", expand=True)
        
        self.project_list = ttk.Treeview(
            list_frame,
            columns=("Name", "Category", "Date"),
            show="headings"
        )
        
        self.project_list.heading("Name", text="Project Name")
        self.project_list.heading("Category", text="Category")
        self.project_list.heading("Date", text="Date Added")
        
        self.project_list.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Display initial projects
        self.display_projects()

    def display_projects(self):
        """Display projects in the treeview"""
        # Clear current items
        for item in self.project_list.get_children():
            self.project_list.delete(item)
        
        # Load and display projects
        projects = self.load_data(self.projects_file)
        for project in projects:
            self.project_list.insert(
                "",
                "end",
                values=(
                    project["name"],
                    project["category"],
                    project["date_added"].split("T")[0]
                )
            )

    def create_documentation_tab(self):
        """Create the documentation tab for language and cultural documentation"""
        doc_frame = ttk.Frame(self.notebook)
        self.notebook.add(doc_frame, text="Documentation")
        
        # Documentation Tools Frame
        tools_frame = ttk.LabelFrame(doc_frame, text="Documentation Tools")
        tools_frame.pack(padx=10, pady=5, fill="x")
        
        tools = [
            "Language Recording",
            "Cultural Practice Documentation",
            "Story Collection",
            "Artifact Photography"
        ]
        
        for tool in tools:
            tool_frame = ttk.Frame(tools_frame)
            tool_frame.pack(padx=5, pady=5, fill="x")
            
            ttk.Label(
                tool_frame,
                text=tool,
                font=("Helvetica", 10, "bold")
            ).pack(side="left", padx=5)
            
            ttk.Button(
                tool_frame,
                text="Launch",
                command=lambda t=tool: self.launch_tool(t)
            ).pack(side="right", padx=5)

    def launch_tool(self, tool_name: str):
        """Launch documentation tool (placeholder)"""
        messagebox.showinfo(
            "Launch",
            f"Launching {tool_name}...\n\nThis is a placeholder for the actual tool implementation."
        )

    def create_contact_tab(self):
        """Create the contact tab for user inquiries"""
        contact_frame = ttk.Frame(self.notebook)
        self.notebook.add(contact_frame, text="Contact")
        
        # Contact Form
        form_frame = ttk.LabelFrame(contact_frame, text="Contact Us")
        form_frame.pack(padx=10, pady=5, fill="x")
        
        # Name Entry
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Email Entry
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        email_entry = ttk.Entry(form_frame)
        email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Message Entry
        ttk.Label(form_frame, text="Message:").grid(row=2, column=0, padx=5, pady=5)
        message_text = scrolledtext.ScrolledText(form_frame, height=6)
        message_text.grid(row=2, column=1, padx=5, pady=5)
        
        def submit_contact():
            """Submit contact form"""
            contact = {
                "name": name_entry.get(),
                "email": email_entry.get(),
                "message": message_text.get("1.0", tk.END).strip(),
                "date_submitted": datetime.now().isoformat()
            }
            
            contacts = self.load_data(self.contacts_file)
            contacts.append(contact)
            self.save_data(contacts, self.contacts_file)
            
            # Clear form
            name_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            message_text.delete("1.0", tk.END)
            
            messagebox.showinfo("Success", "Message sent successfully!")
        
        ttk.Button(
            form_frame,
            text="Submit",
            command=submit_contact
        ).grid(row=3, column=1, pady=10)
        
        # Contact Information
        info_frame = ttk.LabelFrame(contact_frame, text="Contact Information")
        info_frame.pack(padx=10, pady=5, fill="x")
        
        contact_info = [
            ("Phone:", "123-456-789"),
            ("Email:", "info@mysite.com"),
            ("Address:", "500 Terry Francine Street, 6th Floor"),
            ("", "San Francisco, CA 94158")
        ]
        
        for row, (label, value) in enumerate(contact_info):
            ttk.Label(info_frame, text=label).grid(row=row, column=0, padx=5, pady=2)
            ttk.Label(info_frame, text=value).grid(row=row, column=1, padx=5, pady=2)

if __name__ == "__main__":  # Fixed main block
    root = tk.Tk()
    app = HeritageApp(root)
    root.mainloop()