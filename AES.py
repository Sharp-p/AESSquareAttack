import KeyExpansion as ke
from KeyExpansion import Key
import secrets

MAT_MIX_COL= [
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2]
]

MAT_MIX_COL_INV= [
    [14, 9, 13, 11],
    [11, 14, 9, 13],
    [13, 11, 14, 9],
    [9, 13, 11, 14]
]

class State:
    '''Classe che prende in input una stringa di valori binari e ci crea una 
    tabella 4x4 di byte'''
    def __init__(self, text: str, padl= False, hexa= False):
        self.ishex= hexa
        if not hexa:
            alphabet= "0123456789abcdefghijklmnopqrstuvxyz"
            if len(text) < 16:
                if not padl:
                    text= text + "".join(secrets.choice(alphabet) for x in range(16-len(text)))
                else:
                    text= "".join(secrets.choice(alphabet) for x in range(16-len(text))) + text   
        else:
            alphabet= "0123456789abcdef"
            if len(text) < 32:
                if not padl:
                    text= text + "".join(secrets.choice(alphabet) for x in range(32-len(text)))
                else:
                    text= "".join(secrets.choice(alphabet) for x in range(32-len(text))) + text
    
        self.text= text
        self.matrix= [bytearray(), bytearray(), bytearray(), bytearray()]
        hex_txt= []

        i= 0
        if not hexa:
            while i < len(text):
                self.matrix[i//4].append(int(hex(ord(text[i])), 16))
                i+= 1
        else:
            while i < len(text)-1:
                byte= text[i]+text[i+1]
                hex_txt.append(int(byte, 16))
                i+= 2

            i= 0
            while i < len(hex_txt):
                self.matrix[i//4].append(hex_txt[i])
                i+= 1
            
            
    def __str__(self) -> str:
        table= f'{hex(self.matrix[0][0]).removeprefix("0x")} {hex(self.matrix[1][0]).removeprefix("0x")} {hex(self.matrix[2][0]).removeprefix("0x")} {hex(self.matrix[3][0]).removeprefix("0x")} \n\
{hex(self.matrix[0][1]).removeprefix("0x")} {hex(self.matrix[1][1]).removeprefix("0x")} {hex(self.matrix[2][1]).removeprefix("0x")} {hex(self.matrix[3][1]).removeprefix("0x")} \n\
{hex(self.matrix[0][2]).removeprefix("0x")} {hex(self.matrix[1][2]).removeprefix("0x")} {hex(self.matrix[2][2]).removeprefix("0x")} {hex(self.matrix[3][2]).removeprefix("0x")} \n\
{hex(self.matrix[0][3]).removeprefix("0x")} {hex(self.matrix[1][3]).removeprefix("0x")} {hex(self.matrix[2][3]).removeprefix("0x")} {hex(self.matrix[3][3]).removeprefix("0x")}'
        return table
    
    def __repr__(self) -> str:
        return f'State({self.matrix})'
    
    def __getitem__(self, column: int):#la prima coordinata indica le colonne
        return self.matrix[column]
    
    def __len__(self):
        return len(self.matrix)
    
    def __deepcopy__(self):
        copy= State(self.text, hexa= self.ishex)
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                copy[x][y]= self.matrix[x][y]
        return copy

    def take_column(self, index: int):
        return self[index].hex() 
    
def sub_state(state: State) -> None:
    '''Funzione che effettua la sostituzione tramite s-box'''
    for i in state:
        i= ke.sub_word(i)

def rev_sub_state(state: State) -> None:
    for column in state:
        for i in range(len(column)):
            for j in range(len(ke.sbox_en)):
                if column[i] == ke.sbox_en[j]:
                    column[i]= (j//16 << 4) | (j%16)
                    break


def shift_rows(state: State) -> None:
    '''Funzione che ruota le righe all'interno di uno stato'''
    for i in range(len(state)):
        for j in range(i):
            temp= state[0][i]
            state[0][i]= state[1][i]
            state[1][i]= state[2][i]
            state[2][i]= state[3][i]
            state[3][i]= temp
    
def rev_shift_rows(state: State) -> None:
    for i in range(len(state)):
        for j in range(i):
            temp= state[3][i]
            state[3][i]= state[2][i]
            state[2][i]= state[1][i]
            state[1][i]= state[0][i]
            state[0][i]= temp

def molAES(byte: int, coe: int) -> bytearray:
    '''Funzione che effettua la moltiplicazione nel campo finito di AES'''
    if coe == 1:
        return byte
    if coe == 2:
        return byte<<1 ^ (0x11b & -(byte>>7))
    return molAES(byte, coe-1) ^ byte


def mix_columns(state: State, dec: bool= False) -> None:
    '''Funzione che applica una trasformazione, 
    contenente XOR ad ogni byte dello state'''
    temp= state.__deepcopy__()
    if not dec:    
        for i in range(len(state)):
            for j in range(len(state[i])):
                state[i][j]= (molAES(temp[i][0], MAT_MIX_COL[j][0]) ^ 
                              molAES(temp[i][1], MAT_MIX_COL[j][1]) ^
                              molAES(temp[i][2], MAT_MIX_COL[j][2]) ^
                              molAES(temp[i][3], MAT_MIX_COL[j][3]))
    else:
        for i in range(len(state)):
            for j in range(len(state[i])):
                state[i][j]= (molAES(temp[i][0], MAT_MIX_COL_INV[j][0]) ^ 
                              molAES(temp[i][1], MAT_MIX_COL_INV[j][1]) ^
                              molAES(temp[i][2], MAT_MIX_COL_INV[j][2]) ^
                              molAES(temp[i][3], MAT_MIX_COL_INV[j][3]))
    
def add_roundkey(state: State, key: Key) -> None:
    '''Funzione che prende in input lo state e una chiave 
    e ne effettua lo XOR byte a byte'''
    for i in range(len(state)):
            for j in range(len(state[i])):
                state[i][j]= state[i][j] ^ key[i][j]


def encrypt(state: State, key: str, nrounds: int= 10):
    '''Funzione che esegue il cifraggio di uno State data una certa key 
    con nrounds rounds'''
    round_keys= ke.key_expansion(key, nrounds)
    add_roundkey(state, round_keys[0])
    for x in range(nrounds-1):
        round(state, round_keys[x+1])
    sub_state(state)
    shift_rows(state)
    add_roundkey(state, round_keys[nrounds])
    
    

def round(state: State, key: Key):
    '''Funzione che effettua un round di AES completo'''
    sub_state(state)
    shift_rows(state)
    mix_columns(state)
    add_roundkey(state, key)

