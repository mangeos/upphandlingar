import tkinter as tk
from tkinter import messagebox
from pprint import pprint
import winsound

from system_manager import SystemManager

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Sökhanterare")
        self.geometry("400x300")

        self.system_manager = SystemManager(self)

        # Entry för att mata in sökningar
        self.entry = tk.Entry(self)
        self.entry.pack(pady=10)

        # Knapp för att lägga till sökning
        self.add_button = tk.Button(self, text="Lägg till sökning", command=self.add_search)
        self.add_button.pack()

        # Lista för att visa befintliga sökningar
        self.listbox = tk.Listbox(self)
        self.listbox.pack(expand=True, fill=tk.BOTH)

        # Knapp för att ta bort sökning
        self.remove_button = tk.Button(self, text="Ta bort vald sökning", command=self.remove_search)
        self.remove_button.pack()

        # Knapp för att köra alla sökningar
        self.run_button = tk.Button(self, text="Kör alla sökningar", command=self.run_all_searches)
        self.run_button.pack()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Uppdatera listan över sökningar
        self.update_search_list()
        
        # # Skapa ett Observer-objekt och binda en funktion till den egna händelsen
        # self.bind("<<CustomEvent>>", self.handle_event)

    def open_link(self, url):
        # Öppna länken när användaren klickar på den
        import webbrowser
        webbrowser.open_new(url)
    
    def handle_event(self, url):
        # Uppdatera etiketten med händelsedata
        # pprint(event)
        
        # messagebox.showinfo("Nya Upphandlingar", event)
        winsound.Beep(440, 300)  # Frekvensen 1000 Hz och varaktigheten 300 ms
        new_window = tk.Toplevel(self)
        new_window.title("Nytt fönster")

        # Skapa en länk i det nya fönstret
        link_label = tk.Label(new_window, text="Klicka här för att öppna länken", fg="blue", cursor="hand2")
        link_label.pack(padx=10, pady=10)
        link_label.bind("<Button-1>", lambda event: self.open_link(url))

        # Skapa en knapp för att stänga det nya fönstret
        close_button = tk.Button(new_window, text="Stäng", command=new_window.destroy)
        close_button.pack(padx=10, pady=10)

    def add_search(self):
        query = self.entry.get()
        if query:
            added = self.system_manager.add_query(query)
            if added:
                self.update_search_list()
            else:
                messagebox.showwarning("Redan tillagd", "Sökningen finns redan.")
        else:
            messagebox.showwarning("Tom sökning", "Vänligen ange en sökning.")

    def remove_search(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            query = self.listbox.get(index)
            self.system_manager.delete_query(query)
            self.update_search_list()
        else:
            messagebox.showwarning("Ingen sökning vald", "Vänligen välj en sökning att ta bort.")

    def run_all_searches(self):
        self.system_manager.run_all_queries_to_script()
        # messagebox.showinfo("Sökningar klara", "Alla sökningar är klara.")

    def update_search_list(self):
        self.listbox.delete(0, tk.END)
        for query in self.system_manager.get_all_query():
            self.listbox.insert(tk.END, query)

    def on_closing(self):
        # Denna metod anropas när användaren försöker stänga fönstret
        # Här kan du lägga till koden för att hantera stängningshändelsen
        print("Fönstret stängs...")
        # Till exempel, om du vill förhindra att fönstret stängs direkt:
        self.system_manager.stop_schedule()
        self.destroy()
    
if __name__ == "__main__":
    app = GUI()
    app.mainloop()
