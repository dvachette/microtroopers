import sys
import os
sys.path.append(os.getcwd())

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from server.database import Database
class NewItemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Add New Items")

        self.db = Database('data.db')

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Create frames for each tab
        self.weapon_frame = ttk.Frame(self.notebook, width=400, height=400)
        self.cosmetic_frame = ttk.Frame(self.notebook, width=400, height=400)
        self.player_frame = ttk.Frame(self.notebook, width=400, height=400)

        self.weapon_frame.pack(fill='both', expand=True)
        self.cosmetic_frame.pack(fill='both', expand=True)
        self.player_frame.pack(fill='both', expand=True)

        # Add frames to notebook
        self.notebook.add(self.weapon_frame, text='Weapons')
        self.notebook.add(self.cosmetic_frame, text='Cosmetics')
        self.notebook.add(self.player_frame, text='Players')

        # Create weapon tab
        self.create_weapon_tab()

        # Create cosmetic tab
        self.create_cosmetic_tab()

        # Create player tab
        self.create_player_tab()

    def create_weapon_tab(self):
        # Create labels and entry widgets for weapon attributes
        tk.Label(self.weapon_frame, text="Weapon Name").grid(row=0, column=0)
        self.weapon_name_entry = tk.Entry(self.weapon_frame)
        self.weapon_name_entry.grid(row=0, column=1)

        tk.Label(self.weapon_frame, text="Price").grid(row=1, column=0)
        self.weapon_price_entry = tk.Entry(self.weapon_frame)
        self.weapon_price_entry.grid(row=1, column=1)

        tk.Label(self.weapon_frame, text="Damage").grid(row=2, column=0)
        self.weapon_damage_entry = tk.Entry(self.weapon_frame)
        self.weapon_damage_entry.grid(row=2, column=1)

        tk.Label(self.weapon_frame, text="Explosion Radius").grid(row=3, column=0)
        self.weapon_radius_entry = tk.Entry(self.weapon_frame)
        self.weapon_radius_entry.grid(row=3, column=1)

        tk.Label(self.weapon_frame, text="Reach").grid(row=4, column=0)
        self.weapon_reach_entry = tk.Entry(self.weapon_frame)
        self.weapon_reach_entry.grid(row=4, column=1)

        tk.Label(self.weapon_frame, text="Ammo").grid(row=5, column=0)
        self.weapon_ammo_entry = tk.Entry(self.weapon_frame)
        self.weapon_ammo_entry.grid(row=5, column=1)

        tk.Label(self.weapon_frame, text="Reload Speed").grid(row=6, column=0)
        self.weapon_reload_speed_entry = tk.Entry(self.weapon_frame)
        self.weapon_reload_speed_entry.grid(row=6, column=1)

        tk.Label(self.weapon_frame, text="Cool Down").grid(row=7, column=0)
        self.weapon_cool_down_entry = tk.Entry(self.weapon_frame)
        self.weapon_cool_down_entry.grid(row=7, column=1)

        tk.Label(self.weapon_frame, text="Velocity").grid(row=8, column=0)
        self.weapon_velocity_entry = tk.Entry(self.weapon_frame)
        self.weapon_velocity_entry.grid(row=8, column=1)

        tk.Label(self.weapon_frame, text="Motion Type").grid(row=9, column=0)
        self.weapon_motion_type_entry = tk.Entry(self.weapon_frame)
        self.weapon_motion_type_entry.grid(row=9, column=1)

        tk.Label(self.weapon_frame, text="Image").grid(row=10, column=0)
        self.weapon_image_entry = tk.Entry(self.weapon_frame)
        self.weapon_image_entry.grid(row=10, column=1)
        self.weapon_image_button = tk.Button(self.weapon_frame, text="Select Image", command=self.select_weapon_image)
        self.weapon_image_button.grid(row=10, column=2)

        # Create submit button
        self.weapon_submit_button = tk.Button(self.weapon_frame, text="Add Weapon", command=self.add_weapon)
        self.weapon_submit_button.grid(row=11, column=0, columnspan=3)

    def select_weapon_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")], initialdir=os.getcwd(), defaultextension=".png")
        if file_path:
            self.weapon_image_entry.delete(0, tk.END)
            self.weapon_image_entry.insert(0, file_path)

    def add_weapon(self):
        # Get values from entry widgets
        name = self.weapon_name_entry.get()
        price = self.weapon_price_entry.get()
        damage = self.weapon_damage_entry.get()
        radius = self.weapon_radius_entry.get()
        reach = self.weapon_reach_entry.get()
        ammo = self.weapon_ammo_entry.get()
        reload_speed = self.weapon_reload_speed_entry.get()
        cool_down = self.weapon_cool_down_entry.get()
        velocity = self.weapon_velocity_entry.get()
        motion_type = self.weapon_motion_type_entry.get()
        image_path = self.weapon_image_entry.get()

        # Validate inputs
        if not name or not price or not damage or not radius or not reach or not ammo or not reload_speed or not cool_down or not velocity or not motion_type or not image_path:
            messagebox.showerror("Input Error", "All fields are required")
            return

        try:
            price = int(price)
            damage = int(damage)
            radius = int(radius)
            reach = int(reach)
            ammo = int(ammo)
            reload_speed = int(reload_speed)
            cool_down = int(cool_down)
            velocity = int(velocity)
        except ValueError:
            messagebox.showerror("Input Error", "Price, Damage, Radius, Reach, Ammo, Reload Speed, Cool Down, and Velocity must be integers")
            return

        # Insert into database
        self.db.execute('''
            INSERT INTO weapons (name, price, damage, radius, reach, amo, reload_speed, cool_down, velocity, motion_type, path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, price, damage, radius, reach, ammo, reload_speed, cool_down, velocity, motion_type, image_path))

        messagebox.showinfo("Success", "Weapon added successfully")
        self.clear_weapon_entries()

    def clear_weapon_entries(self):
        self.weapon_name_entry.delete(0, tk.END)
        self.weapon_price_entry.delete(0, tk.END)
        self.weapon_damage_entry.delete(0, tk.END)
        self.weapon_radius_entry.delete(0, tk.END)
        self.weapon_reach_entry.delete(0, tk.END)
        self.weapon_ammo_entry.delete(0, tk.END)
        self.weapon_reload_speed_entry.delete(0, tk.END)
        self.weapon_cool_down_entry.delete(0, tk.END)
        self.weapon_velocity_entry.delete(0, tk.END)
        self.weapon_motion_type_entry.delete(0, tk.END)
        self.weapon_image_entry.delete(0, tk.END)

    def create_cosmetic_tab(self):
        # Create labels and entry widgets for cosmetics
        tk.Label(self.cosmetic_frame, text="Cosmetic Name").grid(row=0, column=0)
        self.cosmetic_name_entry = tk.Entry(self.cosmetic_frame)
        self.cosmetic_name_entry.grid(row=0, column=1)

        tk.Label(self.cosmetic_frame, text="Type").grid(row=1, column=0)
        self.cosmetic_type_entry = tk.Entry(self.cosmetic_frame)
        self.cosmetic_type_entry.grid(row=1, column=1)

        tk.Label(self.cosmetic_frame, text="Price").grid(row=2, column=0)
        self.cosmetic_price_entry = tk.Entry(self.cosmetic_frame)
        self.cosmetic_price_entry.grid(row=2, column=1)

        tk.Label(self.cosmetic_frame, text="Image").grid(row=3, column=0)
        self.cosmetic_image_entry = tk.Entry(self.cosmetic_frame)
        self.cosmetic_image_entry.grid(row=3, column=1)
        self.cosmetic_image_button = tk.Button(self.cosmetic_frame, text="Select Image", command=self.select_cosmetic_image)
        self.cosmetic_image_button.grid(row=3, column=2)

        # Create submit button for cosmetics
        self.cosmetic_submit_button = tk.Button(self.cosmetic_frame, text="Add Cosmetic", command=self.add_cosmetic)
        self.cosmetic_submit_button.grid(row=4, column=0, columnspan=3)

    def select_cosmetic_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.cosmetic_image_entry.delete(0, tk.END)
            self.cosmetic_image_entry.insert(0, file_path)

    def add_cosmetic(self):
        # Get values from entry widgets
        name = self.cosmetic_name_entry.get()
        type_ = self.cosmetic_type_entry.get()
        price = self.cosmetic_price_entry.get()
        image_path = self.cosmetic_image_entry.get()

        # Validate inputs
        if not name or not type_ or not price or not image_path:
            messagebox.showerror("Input Error", "All fields are required")
            return

        try:
            price = int(price)
        except ValueError:
            messagebox.showerror("Input Error", "Price must be an integer")
            return

        # Insert into database
        self.db.execute('''
            INSERT INTO cosmetics (name, type, price, image_path)
            VALUES (?, ?, ?, ?)
        ''', (name, type_, price, image_path))

        messagebox.showinfo("Success", "Cosmetic added successfully")
        self.clear_cosmetic_entries()

    def clear_cosmetic_entries(self):
        self.cosmetic_name_entry.delete(0, tk.END)
        self.cosmetic_type_entry.delete(0, tk.END)
        self.cosmetic_price_entry.delete(0, tk.END)
        self.cosmetic_image_entry.delete(0, tk.END)

    def create_player_tab(self):
        # Implementation for player tab
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = NewItemGUI(root)
    root.mainloop()