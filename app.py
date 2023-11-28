import tkinter as tk
from tkinter import messagebox
from blockchainapp import Blockchain


class BlockchainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Blockchain App - MILESTONE 2")

        self.blockchain = Blockchain()

        # Milestone 2
        milestone2_label = tk.Label(master, text="Milestone 2")
        milestone2_label.pack(pady=10)

        # get unlock password from user
        input_label = tk.Label(master, text="Enter unlock password")
        input_label.pack()
        self.entry_unlock_password = tk.Entry(master, width=40)
        self.entry_unlock_password.pack(pady=5, padx=40)

        self.button_generate_wallet = tk.Button(master, text="Generate Mnemonic & Wallet", command=self.generate_wallet)
        self.button_generate_wallet.pack(pady=5)

        # Mnemonic phrase generated will display in the box below
        input_label = tk.Label(master, text="Generated 24-word phrase will be shown below")
        input_label.pack()
        self.entry_unlock_password = tk.Entry(master, width=40)
        self.entry_unlock_password.insert(0, self.blockchain.mnemonic)
        self.entry_unlock_password.pack(pady=5)

        # Generate a persona DID
        self.button_generate_persona_did = tk.Button(master, text="Generate Persona DID", command=self.generate_persona_did)
        self.button_generate_persona_did.pack(pady=5)
        self.entry_persona_did = tk.Entry(master, width=40)
        self.entry_persona_did.insert(0, self.blockchain.persona_did)
        self.entry_persona_did.pack(pady=5)


        # Get user fullname, address etc
        input_label = tk.Label(master, text="Enter full name below")
        input_label.pack()
        self.entry_fullname = tk.Entry(master, width=40)
        self.entry_fullname.pack(pady=5)

        # Get user fullname, address etc
        input_label = tk.Label(master, text="Enter resident address below")
        input_label.pack()
        self.entry_resident_address = tk.Entry(master, width=40)
        self.entry_resident_address.pack(pady=5)


        # Step 2
        input_label = tk.Label(master, text="STEP 2")
        input_label.pack(pady=10)
        self.button_generate_new_address = tk.Button(master, text="Generate New Address/Account", command=self.generate_new_address)
        input_label = tk.Label(master, text="Generated address will display below")
        input_label.pack(pady=5)
        self.button_generate_new_address.pack(pady=5)
        self.entry_new_address = tk.Entry(master, width=40)
        # self.entry_new_address.insert(0, self.blockchain.address)
        self.entry_new_address.pack(pady=10)

        # Delete account/address
        input_label = tk.Label(master, text="Enter address or account to delete below")
        input_label.pack(pady=5)
        self.entry_address_delete = tk.Entry(master, width=40)
        self.entry_address_delete.pack(pady=10)
        self.button_delete_address = tk.Button(master, text="Delete Address/Account", command=self.delete_address)
        self.button_delete_address.pack(pady=5)

        # Display account/address balance
        self.button_dislay_balance = tk.Button(master, text="Display Address/Account Balance", command=self.display_account_balance)
        self.button_dislay_balance.pack(pady=5)

        # Display all transactions
        self.button_display_account_transactions = tk.Button(master, text="Display Address/Account Transaction", command=self.display_account_transactions)
        self.button_display_account_transactions.pack(pady=5)

        # Get list of all new transactions since last change
        # self.button_dislay_balance = tk.Button(master, text="Display Address/Account Transaction", command=self.display_account_balance)
        # self.button_dislay_balance.pack(pady=5)

        # Send/Receive Money
        input_label = tk.Label(master, text="Enter address to send 10 HYD to")
        input_label.pack(pady=5)
        self.entry_send_address = tk.Entry(master, width=40)
        self.entry_send_address.pack(pady=5)
        self.button_send = tk.Button(master, text="Send Fund 10 HYD", command=self.send_fund)
        self.button_send.pack(pady=5)

        # Recover the wallet using the 24-word phrase
        input_label = tk.Label(master, text="Enter 24-word phrase to recover wallet")
        input_label.pack(pady=5)
        self.entry_recover_wallet = tk.Entry(master, width=40)
        self.entry_recover_wallet.pack(pady=5)

        self.button_recover_wallet = tk.Button(master, text="Recover Wallet using 24-2ord phrase", command=self.recover_wallet)
        self.button_recover_wallet.pack(pady=5)


    def generate_wallet(self):
        unlock_password = self.entry_unlock_password.get()
        if unlock_password == '':
            messagebox.showerror("Error", "Please enter transaction id.")
            return
        
        resp = self.blockchain.generate_wallet(unlock_password)
        self.entry_new_address.insert(0, self.blockchain.address)

    def generate_persona_did(self):
        resp = self.blockchain.generate_persona_did()

    def generate_new_address(self):
        if self.check_vault() == False:
            return
        
        resp = self.blockchain.generate_new_address()
        

    def delete_address(self):
        if self.check_vault() == False:
            return
        
        address_to_delete = self.entry_address_delete.get()
        if address_to_delete == '':
            messagebox.showerror("Error", "You need to create a vault or address")
            return
        
        # self.blockchain.display_address_balance()
        
        messagebox.showinfo("Info", "Under development, Please try again later or wait for update")


    def display_account_balance(self):
        if self.check_vault() == False:
            return
        
        if self.blockchain.address == '':
            messagebox.showerror("Error", "You need to create a vault or address")
            return
        
        resp = self.blockchain.display_address_balance()
        messagebox.showinfo("Info", f"Address '{self.blockchain.address}' balance is {self.blockchain.balance}")


    def display_account_transactions(self):
        if self.check_vault() == False:
            return
        
        if self.blockchain.address == '':
            messagebox.showerror("Error", "You need to create a vault or address")
            return
        
        messagebox.showinfo("Info", "Under development, Please try again later or wait for update")
        # transactions = self.blockchain


    def send_fund(self):
        if self.check_vault() == False:
            return
        
        if self.blockchain.address == '':
            messagebox.showerror("Error", "You need to create a vault or address")
            return
        
        receiver_address = self.entry_send_address.get()
        if receiver_address == '':
            messagebox.showerror("Error", "Enter receiver address")
            return
        
        resp = self.blockchain.send_transaction_with_receiver(10, receiver_address)

        messagebox.showinfo("Info", f"Transaction was successful\nTransaction ID: {self.blockchain.transaction_id}")


    def recover_wallet(self):
        wallet_phrase = self.entry_recover_wallet.get()
        if wallet_phrase == '':
            messagebox.showerror("Error", "Enter your wallet 24-word phrase")
            return
        
        wallet = self.blockchain.create_wallet(wallet)
        messagebox.showinfo("Wallet Recovered!", f"Your wallet has been recovered\n Your wallet address is \n {self.blockchain.address}")


    def check_vault(self):
        if self.blockchain.encrypted_vault == None:
            messagebox.showerror("Error", "Create or Load a wallet/vault first")
            return False
        else:
            return True


if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()
