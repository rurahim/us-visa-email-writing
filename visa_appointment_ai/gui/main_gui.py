# streamlit_app/gui.py

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
import threading

class VisaAppointmentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("US Visa Appointment Assistant")
        self.root.geometry("800x600")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input fields
        ttk.Label(main_frame, text="Full Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(main_frame, width=40)
        self.email_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Visa Type:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.visa_type = ttk.Combobox(main_frame, values=["F1", "H1B", "J1", "B1", "B2", "Medical", "Other"])
        self.visa_type.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.visa_type.set("F1")
        
        ttk.Label(main_frame, text="Message:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.message_text = scrolledtext.ScrolledText(main_frame, width=50, height=10)
        self.message_text.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Submit button
        self.submit_button = ttk.Button(main_frame, text="Process Request", command=self.start_processing)
        self.submit_button.grid(row=4, column=1, sticky=tk.W, pady=10)
        
        # Results section
        ttk.Label(main_frame, text="Results:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.results_text = scrolledtext.ScrolledText(main_frame, width=50, height=10)
        self.results_text.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    def validate_inputs(self):
        """Validate all input fields"""
        if not self.name_entry.get().strip():
            messagebox.showerror("Error", "Please enter your full name")
            return False
            
        if not self.email_entry.get().strip():
            messagebox.showerror("Error", "Please enter your email")
            return False
            
        if not self.visa_type.get():
            messagebox.showerror("Error", "Please select a visa type")
            return False
            
        if not self.message_text.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "Please enter your message")
            return False
            
        return True
        
    def update_ui(self, status, result=None, error=None):
        """Update UI elements on the main thread"""
        self.status_var.set(status)
        self.submit_button.state(['!disabled'])
        
        if error:
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert("1.0", error)
            messagebox.showerror("Error", error)
        elif result:
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert("1.0", result)
            
    def process_request(self):
        """Process the visa appointment request in a separate thread"""
        try:
            # Get input values
            data = {
                "full_name": self.name_entry.get().strip(),
                "email": self.email_entry.get().strip(),
                "visa_type": self.visa_type.get(),
                "message": self.message_text.get("1.0", tk.END).strip()
            }
            
            # Make API request
            response = requests.post("http://localhost:8000/api/process/", json=data)
            
            if response.status_code == 200:
                result = response.json()
                # Format results
                formatted_result = f"""Initial Score: {result['initial_score']:.2f}
Final Score: {result['final_score']:.2f}

Original Email:
{result['original_email']}

Improved Email:
{result['best_email']}

Explanation:
{result['xai_explanation']}"""
                
                self.root.after(0, lambda: self.update_ui("Request processed successfully", result=formatted_result))
            else:
                error_msg = f"Error: {response.status_code}\n{response.text}"
                self.root.after(0, lambda: self.update_ui("Error processing request", error=error_msg))
                
        except requests.exceptions.ConnectionError:
            error_msg = "Could not connect to the server. Please make sure the server is running at http://localhost:8000"
            self.root.after(0, lambda: self.update_ui("Connection error", error=error_msg))
            
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            self.root.after(0, lambda: self.update_ui("Error", error=error_msg))
            
    def start_processing(self):
        """Start the processing in a separate thread"""
        if not self.validate_inputs():
            return
            
        self.status_var.set("Processing request...")
        self.submit_button.state(['disabled'])
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_request)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = VisaAppointmentGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
