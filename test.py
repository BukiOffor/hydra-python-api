import iop_python as iop




phrase = "blind market ability shoot topple round inmate pass lunch symbol average alpha party notice switch sea pass toy alien fuel pull angle weather sca"
try:
    wallet = iop.get_morpheus_vault(phrase,"pass")
    print(wallet)

except Exception as e:
    if "VaultCouldNotBeUnwrapped" in str(e):
        print("The vault could not be unwrapped.")
    else:
        print(f"A RuntimeError occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")