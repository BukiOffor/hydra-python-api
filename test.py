import iop_python as iop


phrase = "blind market ability shoot topple round inmate pass lunch symbol average alpha party notice switch sea pass toy alien fuel pull angle weather scan"

vault = iop.get_hyd_vault(phrase, "password", 'mainnet')

print(vault)