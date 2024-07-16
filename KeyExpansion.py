sbox_en = bytearray(
    [    
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
    ]
)

class Key:
    '''Classe che prende in input una stringa di valori binari e ci crea una 
    tabella 4x4 di byte'''
    def __init__(self, k: str, padl= False):
        if len(k) < 32:
            if not padl:
                k= k + "0" * (32 - len(k))
            else:
                k= "0" * (32 - len(k)) + k
        self.key= k
        self.matrix= [bytearray(), bytearray(), bytearray(), bytearray()]
        hex_k= []

        i= 0
        while i < len(k)-1:
            byte= k[i]+k[i+1]
            hex_k.append(int(byte, 16))
            i+= 2

        i= 0
        while i < len(hex_k):
            self.matrix[i//4].append(hex_k[i])
            i+= 1
            
    def __str__(self) -> str:
        table= f'{hex(self.matrix[0][0]).removeprefix("0x")} {hex(self.matrix[1][0]).removeprefix("0x")} {hex(self.matrix[2][0]).removeprefix("0x")} {hex(self.matrix[3][0]).removeprefix("0x")} \n\
{hex(self.matrix[0][1]).removeprefix("0x")} {hex(self.matrix[1][1]).removeprefix("0x")} {hex(self.matrix[2][1]).removeprefix("0x")} {hex(self.matrix[3][1]).removeprefix("0x")} \n\
{hex(self.matrix[0][2]).removeprefix("0x")} {hex(self.matrix[1][2]).removeprefix("0x")} {hex(self.matrix[2][2]).removeprefix("0x")} {hex(self.matrix[3][2]).removeprefix("0x")} \n\
{hex(self.matrix[0][3]).removeprefix("0x")} {hex(self.matrix[1][3]).removeprefix("0x")} {hex(self.matrix[2][3]).removeprefix("0x")} {hex(self.matrix[3][3]).removeprefix("0x")}'
        return table

    def __repr__(self) -> str:
        return f'Key({self.matrix})'
    
    def __getitem__(self, column: int):#la prima coordinata indica le colonne
        return self.matrix[column]
    
    def take_column(self, index: int):
        return self[index].hex() 
    
            
def rot_word(v: bytearray):
    '''Funzione che prende in input 4 bytes e li ruota a sinistra
      di una posizione'''
    if len(v) != 4:
        print("Errore, numero di bytes passati diverso da 4")
        quit()
    
    temp= v.copy()
    v[0]= temp[1]
    v[1]= temp[2]
    v[2]= temp[3]
    v[3]= temp[0]

    return v

def sub_word(v: bytearray):
    '''Funzione che prende in input 4 byte e gli applica una 
    sostistuzione tramite s-box'''
    if len(v) != 4:
        print("Errore, numero di bytes passati diverso da 4")
        quit()
    
    for i in range(len(v)):
        x= (v[i] & 240) >> 4
        y= (v[i] & 15)
        v[i]= sbox_en[x*16 + y]
    
    return v

def constant(i: int):
    '''Funzione che prende un intero positivo e effettua il calcolo 
    del primo byte della round constant'''
    if i < 0:
        print("Valore deve essere maggiore o uguale a 0")
        quit()
    if i == 0:
        return 0x8d
    
    prev_con= constant(i-1)
    con= prev_con<<1 ^ (0x11b & -(prev_con>>7))

    return con

def rcon(i: int):
    '''Funzione che crea la round constant'''
    if i < 0:
        print("Valore deve essere maggiore o uguale a 0")
        quit()
    
    return bytearray([constant(i), 0x00, 0x00, 0x00])

def key_expansion(k: str, n: int= 10):
    '''Funzione che ti genera il numero di subkeys necessarie ad eseguire 
    una cifratura tramite AES a n round.'''
    org= Key(k)
    expanded_key= [org]
    for i in range(n):
        first_column= expanded_key[-1][-1].copy()
        first_column= rot_word(first_column)
        first_column= sub_word(first_column)
        first_column= int(expanded_key[-1].take_column(0), 16) ^ int(first_column.hex(), 16)
        first_column= int(rcon(i+1).hex(), 16) ^ first_column
        first_column= bytearray.fromhex(hex(first_column).removeprefix("0x").zfill(8))

        second_column= int(first_column.hex(), 16) ^ int(expanded_key[-1].take_column(1), 16)
        third_column= second_column ^ int(expanded_key[-1].take_column(2), 16)
        fourth_column= third_column ^ int(expanded_key[-1].take_column(3), 16)

        second_column= bytearray.fromhex(hex(second_column).removeprefix("0x").zfill(8))
        third_column= bytearray.fromhex(hex(third_column).removeprefix("0x").zfill(8))
        fourth_column= bytearray.fromhex(hex(fourth_column).removeprefix("0x").zfill(8))
        
        chiave= first_column.hex() + second_column.hex() + third_column.hex() + fourth_column.hex()
        expanded_key.append(Key(chiave))
    return expanded_key

""" ex= key_expansion("2b7e151628aed27babf7158809cf4f3c")
for x in ex:
    print(f"{x.take_column(0)}{x.take_column(1)}{x.take_column(2)}{x.take_column(3)}")
    pass """  