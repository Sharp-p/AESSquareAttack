from AES import State
from KeyExpansion import Key
import KeyExpansion as ke
import AES
import secrets

class DeltaSet:
    def __init__(self, set: list= []):
        self.set= set

    def __getitem__(self, index: int) -> State:#la prima coordinata indica le colonne
        return self.set[index]
    
    def __str__(self) -> str:
        txt= [x.__str__() for x in self.set]
        return '\n\n'.join(txt)
    
    def __len__(self) -> int:
        return len(self.set)
    
    def __deepcopy__(self):
        copy= DeltaSet([])
        for x in range(len(self.set)):
            copy.append(self.set[x].__deepcopy__())
        return copy

    def append(self, state: State) -> None:
        self.set.append(state)

    def check(self, i: int) -> bool:
        '''Funzione che controlla se l'i-esimo byte di tutti i State 
        nel DeltaSet è attivo'''
        xor= 0        
        for j in range(256):
            xor= xor ^ self.set[j][(i//4+(i%4))%4][i%4]
        if xor == 0:
            return True
        return False

def setup(k: str) -> DeltaSet:
    '''Funzione che genera un particolare set di State
    cifrati fino al quarto round. E' una simulazione di come dovrebbe 
    funzionare un oracolo, che teoricamente ti fornisce ciphertext
    a partire dal plaintext utilizzando la chiave ricercata, 
    ovviamente per motivi didattici forniamo noi la chiave tramite cui
    poi l'oracolo esegue il cifraggio'''
    key= Key(k)
    alphabet= "0123456789abcdef"
    rnd= "".join(secrets.choice(alphabet) for x in range(30))
    dset= DeltaSet([])
    #riempo ogni state con il primo byte che incrementa e gli stessi 
    # byte per i 15 rimanenti
    for x in range(256):
        text= hex(x).removeprefix("0x").zfill(2) + rnd
        state= State(text, hexa= True)
        AES.encrypt(state, key= key.key, nrounds= 4)
        dset.append(state)
    return dset

def reverse_state(guess: str, i: int, dset: DeltaSet) -> None:
    '''Funzione che prende un delta set esegue la decifrazione dell'ultimo 
    round del DeltaSet con un chiave di 0 contenente il byte che si pensa 
    possa essere della RoundKey nell'i-esima posizione della chiave '''
    
    guess= ("00" * i) + guess
    guess= Key(guess)
    for i in range(len(dset)):
        AES.add_roundkey(dset[i], guess)
        AES.rev_shift_rows(dset[i])
        AES.rev_sub_state(dset[i])

def find_guess(dset: DeltaSet, i: int, k: str) -> str:
    '''Funzione che per un certo indice (byte) della chiave del quarto round 
    trova qual'è il byte effettivo della round key'''
    
    valids= []

    for x in range(256):
        copy= dset.__deepcopy__()
        guess= hex(x).removeprefix("0x")
        reverse_state(guess, i, copy)
        if copy.check(i):
            valids.append(guess)
        del copy

    if len(valids) != 1:
        while len(valids) != 1:
            for b in valids:
                states= setup(k)
                reverse_state(b, i, states)
                if not states.check(i):
                    valids.remove(b)

    return valids[0]    

def fourth_key(k: str) -> str:
    '''Funzione che prende in input una chiave in esadecimale, 
    esegue una cifratura tramite AES fino al quarto round, e poi la rompe.'''
    set= setup(k)
    key= ""
    for index in range(16):
        key= key + find_guess(set, index, k)
        if index % 4 == 0: print(index, "-esimo byte trovato")
    return key

def key_deexpansion(k: str):
    '''Funzione che effettua l'inverso dell'espansione della chiave a partire 
    dalla chiave del quarto round, fino a scoprire la chiave originale.'''
    lst= Key(k)
    keys= [lst]
    for i in range(4):
        column4= keys[-1][3].copy()
        column4= int(column4.hex(), 16) ^ int(keys[-1][2].hex(), 16)
        column3= keys[-1][2].copy()
        column3= int(column3.hex(), 16) ^ int(keys[-1][1].hex(), 16)
        column2= keys[-1][1].copy()
        column2= int(column2.hex(), 16) ^ int(keys[-1][0].hex(), 16)

        column2= bytearray.fromhex(hex(column2).removeprefix("0x").zfill(8))
        column3= bytearray.fromhex(hex(column3).removeprefix("0x").zfill(8))
        column4= bytearray.fromhex(hex(column4).removeprefix("0x").zfill(8))

        column1= keys[-1][0].copy()
        column1= int(column1.hex(), 16) ^ int(ke.rcon(3-i+1).hex(), 16)

        cp4= column4.copy()
        ke.rot_word(cp4)
        ke.sub_word(cp4)
        column1= int(cp4.hex(), 16) ^ column1

        column1= bytearray.fromhex(hex(column1).removeprefix("0x").zfill(8))

        chiave= column1.hex() + column2.hex() + column3.hex() + column4.hex()
        keys.append(Key(chiave))
    keys.reverse()
    return keys

k= "aa"
#lst_key= fourth_key(k) #(ci mette un po' tanto tempo il risultato è quello qui sotto)
lst_key= "4483ed3987ef15c3751b75b27e14ee2b"
keys= key_deexpansion(lst_key)
print(keys[0])