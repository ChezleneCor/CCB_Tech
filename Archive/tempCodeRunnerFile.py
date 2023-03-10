class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id
        
        # title
        title = Label(self, text="User Management", font=(title_font, 50), fg=title_color)
        title.grid(row=0, column=0, columnspan=4)

        # treeview to display users
        tree = ttk.Treeview(self, columns=('Username', 'User Level'))
        tree.heading('Username', text='Username')
        tree.heading('User Level', text='User Level')
        tree.grid(row=1, column=0, columnspan=4)

        # populate the treeview with data from the database
        connection = sqlite3.connect("inventory.db")
        cursor = connection.execute('SELECT username, user_level FROM login')
        for row in cursor:
            tree.insert('', 0, text='', values=(row[0], row[1]))
        connection.close()

        # user level label and combobox
        user_level_label = Label(self, text="Select User Level:").grid(row=2, column=0)
        user_levels = ['1', '2', '3']
        user_level_combo = ttk.Combobox(self, values=user_levels)
        user_level_combo.grid(row=2, column=1)

        # change user level button
        change_button = Button(self, text="Change User Level", command=lambda: update_user_level())
        change_button.grid(row=2, column=2)

        # delete user label and entry box
        delete_label = Label(self, text="Enter Username to Delete:").grid(row=3, column=0)
        delete_entry = Entry(self)
        delete_entry.grid(row=3, column=1)

        # delete user button
        delete_button = Button(self, text="Delete User", command=lambda: delete_user())
        delete_button.grid(row=3, column=2)

        # user level guide
        guide_label = Label(self, text="User Level Guide:").grid(row=4, column=0, sticky=W)
        employee_label = Label(self, text="1 - Employee", font=("Arial", 12)).grid(row=5, column=0, sticky=W)
        manager_label = Label(self, text="2 - Manager", font=("Arial", 12)).grid(row=6, column=0, sticky=W)
        ceo_label = Label(self, text="3 - CEO", font=("Arial", 12)).grid(row=7, column=0, sticky=W)

        def update_user_level():
            # get selected username from treeview
            selected_item = tree.focus()
            if selected_item:
                selected_username = tree.item(selected_item)['values'][0]
            else:
                tkinter.messagebox.showerror("Error", "Please select a user from the list.")

            # get selected user level from combobox
            selected_user_level = user_level_combo.get()

            # update user level in database
            connection = sqlite3.connect("inventory.db")
            connection.execute('UPDATE login SET user_level=? WHERE username=?', (selected_user_level, selected_username))
            connection.commit()
            connection.close()

            # update treeview with new user level
            tree.item(selected_item, values=(selected_username, selected_user_level))

        def delete_user():
            # get username to delete from entry box
            username = delete_entry.get()

            # confirm deletion with user
            confirm_delete = tkinter.messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete user {username}?")

            if confirm_delete:
                # delete user from database
                connection = sqlite3.connect("inventory.db")
                connection.execute('DELETE FROM login WHERE username=?', (username,))
                connection.commit()
                connection.close()

                # remove user from treeview
                for child in tree.get_children():
                    if tree.item(item)['values'][0] == username:
                        tree.delete(item)

                tkinter.messagebox.showinfo("Success", f"User {username} has been deleted.")