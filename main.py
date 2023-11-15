import iop_python as iop
import asyncio


async def get_wallet(wallet):
    await iop.call_wallet(wallet)



main_wallet = "blind market ability shoot topple round inmate pass lunch symbol average alpha party notice switch sea pass toy alien fuel pull angle weather scan"
seedPhrase = iop.generate_phrase()
#print(seedPhrase)
ark_wallet = iop.get_ark_wallet(main_wallet)
hyd_wallet = iop.get_wallet(main_wallet)
print("ark wallet: ",ark_wallet)
print('hyd wallet: ',hyd_wallet)
asyncio.run(get_wallet("tfzy3zXYUuEPoX17GkJzQnavdbRmmmFLk6"))



