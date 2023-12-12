from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from api.hydra import HydraChain, HydraWallet
import json


class BlockchainApp(App):

    def build(self):
        self.blockchain = HydraWallet()
        self.wallets = self.get_vaults()
        self.active_acc = 0
        
        layout = BoxLayout(orientation='vertical')


        # Milestone 2
        milestone2_label = Label(text="Welcome to your Wallet")
        layout.add_widget(milestone2_label)

        # Display Account in Use

        address = self.get_state()
        account_label = Label(text=f"Account: {address}")
        layout.add_widget(account_label)

        # display balance
        wallet = self.get_acc_details()
        if wallet != None:
            balance = self.blockchain.display_address_balance()
            input_label = Label(text=f"Balance: {balance}")
            layout.add_widget(input_label)


         #Acoounts Availaible
        acc_num = len(self.wallets)
        input_label = Label(text=f"{acc_num} Accounts Availaible")
        layout.add_widget(input_label)

        # get unlock password from user
        input_label = Label(text="Enter password to create new account: ⬇️")
        layout.add_widget(input_label)
        self.entry_unlock_password = TextInput(multiline=False,width=40)
        layout.add_widget(self.entry_unlock_password)
        self.button_generate_wallet = Button(text="Generate Mnemonic & Wallet ✅", on_press=self.generate_wallet) #here
        layout.add_widget(self.button_generate_wallet)

        #Mnemonic phrase generated will display in the box below
        input_label = Label(text="The generated 24-word phrase will be shown below: ⬇️")
        layout.add_widget(input_label)
        self.entry_new_address = TextInput(multiline=True, width=300)
        layout.add_widget(self.entry_new_address)


        #Select Account to use
        # input_label = Label(, text="Change Account to Use")
        # input_label.pack()
        # self.active_num = TextInput(, width=20)
        # self.active_num.pack(padx=10,pady=5)
        # self.button_set_active_account = Button(, text="swap account", command=self.active_account) #here
        # self.button_set_active_account.pack(padx=3,pady=3)



        # Generate a persona DID
        input_label = Label(text="Enter Password to Generate DID: ⬇️")
        layout.add_widget(input_label)        
        self.did_password = TextInput(multiline=False,width=200)
        layout.add_widget(self.did_password)
        self.button_generate_persona_did = Button(text="Generate Persona DID ✅", on_press=self.generate_persona_did)
        layout.add_widget(self.button_generate_persona_did)
        self.entry_persona_did = TextInput(multiline=False, width=300)
        layout.add_widget(self.entry_persona_did)
        


        #Delete Account to use
        input_label = Label(text="Enter Index of Account to delete: ⬇️")
        layout.add_widget(input_label)
        self.delete_id = TextInput(multiline=False, width=300)
        layout.add_widget(self.delete_id)
        self.button_set_delete_account = Button(text="delete account ‼️", on_press=self.delete_account) #here
        layout.add_widget(self.button_set_delete_account)


        # Recover the wallet using the 24-word phrase
        input_label = Label(text="Enter 24-word phrase to recover wallet: ⬇️")
        layout.add_widget(input_label)
        self.entry_recover_wallet = TextInput(multiline=False, width=300)
        layout.add_widget(self.entry_recover_wallet)
        input_label = Label(text="Enter password to recover wallet: ⬇️")
        layout.add_widget(input_label)
        self.entry_recover_password = TextInput(multiline=False, width=300)
        layout.add_widget(self.entry_recover_password)
        self.button_recover_wallet = Button(text="Recover Wallet ✅", on_press=self.recover_wallet)
        layout.add_widget(self.button_recover_wallet)

        # Send/Receive Money
        input_label = Label(text="Enter address to send HYD to: ⬇️")
        layout.add_widget(input_label)
        self.entry_send_address = TextInput(multiline=False, width=300)
        layout.add_widget(self.entry_send_address)
        input_label = Label(text="Enter the amount to send: ⬇️")
        layout.add_widget(input_label)
        self.entry_send_amount = TextInput(multiline=False, width=300)
        layout.add_widget(self.entry_send_amount)
        input_label = Label(text="Enter wallet password: ⬇️")
        layout.add_widget(input_label)
        self.wallet_password = TextInput(multiline=False, width=300)
        layout.add_widget(self.wallet_password)
        self.button_send = Button(text="Send ✅", on_press=self.send_hyd) #here
        layout.add_widget(self.button_send)

        # Create a Listbox and display transaction history
        input_label = Label(text="Transaction History 🏦")
        layout.add_widget(input_label)
        address = self.get_state()
        transactions = self.blockchain.get_account_transactions()
        if transactions != None:
            for item in transactions:
                sender, recipient = item['sender'],item['recipient']
                amount = item['amount']
                if sender == address:
                    layout.add_widget(Label(text=f"Sent {amount} hyd to {recipient}"))
                else:
                    layout.add_widget(Label(text=f"Received {amount} hyd from {sender}"))
        return layout


    def send_hyd(self,instance):
        address = self.entry_send_address.text
        amount = self.entry_send_amount.text
        password = self.wallet_password.text
        if len(self.wallets) > 0 and address != "" and amount != "" and password != "":    
            txhash = self.blockchain.send_transaction(address, int(amount),password)
            popup = Popup(title='Info', content=Label(text=f'Transaction was successful\nTransaction ID: {txhash}'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            popup = Popup(title='Error', content=Label(text='Something went wrong with your transaction.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()

    def delete_account(self,instance):
        delete_id = self.delete_id.text
        if delete_id != "":
            self.blockchain.delete_account(delete_id)
            popup = Popup(title='Info', content=Label(text=f'Transaction was successful\nAccount with ID: {delete_id} has been deleted'),
                      size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            popup = Popup(title='Error', content=Label(text='Account index is not specified'),
                      size_hint=(None, None), size=(400, 200))
            popup.open()

    def get_state(self):
        if len(self.wallets) > 0:
            address = self.blockchain.get_wallet_address()
            return address
        
    def get_acc_details(self):
        if len(self.wallets) > 0:
            address = self.blockchain.get_wallet_address()
            return address

    def active_account(self,instance):
        if len(self.wallets) > 0:
            acc_active = self.active_num.text
            self.active_num = int(acc_active)
            print(self.active_num)
        else:
            popup = Popup(title='Error', content=Label(text='You do not have an active wallet.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()


    def generate_wallet(self,instance):
        unlock_password = self.entry_unlock_password.text
        if unlock_password == '':
            popup = Popup(title='Error', content=Label(text='Please enter a password for your wallet.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return
        phrase = self.blockchain.generate_phrase()
        resp = self.blockchain.generate_wallet(unlock_password,phrase)
        self.entry_new_address.text = resp


    def generate_persona_did(self,instance):
        password = self.did_password.text
        if len(self.wallets) > 0 and password != "":
            resp = self.blockchain.generate_did(password)
            self.entry_persona_did.text = resp
        else:
            popup = Popup(title='Error', content=Label(text='You do not have an active wallet or no password given.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()


    def recover_wallet(self,instance):
        wallet_phrase = self.entry_recover_wallet.text
        password = self.entry_recover_password.text
        if wallet_phrase == '' or password == "":
            popup = Popup(title='Error', content=Label(text='Enter your wallet 24-word phrase and password.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return     
        self.blockchain.recover_wallet(password,wallet_phrase)
        popup = Popup(title='Wallet Recovered!', content=Label(text='Your wallet has been recovered.'),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    # def display_account_transactions(self):
    #     if self.check_vault() == False:
    #         return
        
    #     if self.blockchain.address == '':
    #         popup = Popup(title='Error', content=Label(text='You need to create a vault or address.'),
    #                       size_hint=(None, None), size=(400, 200))
    #         popup.open()
    #         return
    #     address = self.get_state()
    #     transactions = self.blockchain.get_account_transactions()
    #     popup_content = BoxLayout(orientation='vertical')
    #     for item in transactions:
    #         sender, recipient = item['sender'], item['recipient']
    #         amount = item['amount']
    #         if sender == address:
    #             popup_content.add_widget(Label(text=f"Sent {amount} hyd to {recipient}"))
    #         else:
    #             popup_content.add_widget(Label(text=f"Received {amount} hyd from {sender}"))

    #     popup = Popup(title='Transaction History 🏦', content=popup_content, size_hint=(None, None), size=(400, 300))
    #     popup.open()
        
        

    def get_vaults(self):
        try:
            wallets = self.blockchain.load_wallets()
            return wallets
        except FileNotFoundError:
            return []



if __name__ == "__main__":
    BlockchainApp().run()
