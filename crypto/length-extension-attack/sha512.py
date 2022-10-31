#!/usr/bin/python3.8

import hashlib

ROTR = lambda x, n: (x >> n) | (x << (64 - n))
SHR = lambda x, n: x >> n
mod_add = lambda x: x % 2**64

Ch = lambda x, y, z : (x & y) ^ (~x & z)
Maj = lambda x, y, z : (x & y) ^ (x & z) ^ (y & z)
sum_0 = lambda x : ROTR(x, 28) ^ ROTR(x, 34) ^ ROTR(x, 39)
sum_1 = lambda x : ROTR(x, 14) ^ ROTR(x, 18) ^ ROTR(x, 41)
sigma_0 = lambda x : ROTR(x, 1) ^ ROTR(x, 8) ^ SHR(x, 7)
sigma_1 = lambda x : ROTR(x, 19) ^ ROTR(x, 61) ^ SHR(x, 6)


K = (
	0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,  
	0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
	0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
	0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694, 
	0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65, 
	0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5, 
	0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4, 
	0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70, 
	0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df, 
	0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b, 
	0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30, 
	0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
	0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
	0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
	0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
	0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
	0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
	0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
	0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
	0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817,
)

H_0 =[
    0x6a09e667f3bcc908, # H_0_0
    0xbb67ae8584caa73b, # H_0_1
    0x3c6ef372fe94f82b, # H_0_2
    0xa54ff53a5f1d36f1, # H_0_3
    0x510e527fade682d1, # H_0_4
    0x9b05688c2b3e6c1f, # H_0_5
    0x1f83d9abfb41bd6b, # H_0_6
    0x5be0cd19137e2179, # H_0_7
]


class sha512():

    def __init__(self, msg, H_0 = H_0) -> None:
        self.msg = msg
        self.msg_pad = b''
        self.M = []
        self.H = list(H_0)

        self.padding()
        self.parssing()
        self.chunkProcess()


    def padding(self) -> None:

        # Cálculo de longitud, midiendo el número de bits usados en base decimal
        L = len(self.msg) # 51 bytes
        l_bits = L*8 # 408 bits

        len_big_endian = l_bits.to_bytes(16,'big')
        K = 128 - (L + 1 + 16)%128 # 128 - (51 + 1 + 16)%128 = 60

        self.msg_pad = self.msg + b"\x80" + b"\x00"*K + len_big_endian


    def parssing(self) -> None:

        for i in range(0, len(self.msg_pad), 128):
            M_i = self.msg_pad[i:i+128]
            self.M.append(M_i)


    def chunkProcess(self) -> None :

        for M_i in self.M:
            # Step 1 ----------------------------------------------------
            w = [0 for _ in range(80)]
            w[:16] = [ 
                int.from_bytes(M_i[i:i+8], 'big') 
                for i in range(0,len(M_i),8)
            ]

            for t in range(16,80):
                w[t] = mod_add(
                    sigma_1(w[t-2]) + w[t-7] + sigma_0(w[t-15]) + w[t-16]
                )

            # Step 2 ----------------------------------------------------
            a, b, c, d, e, f, g, h = self.H

            # Step 3 ----------------------------------------------------
            for t in range(80):
                T_1 = mod_add(h + sum_1(e) + Ch(e, f, g) +K[t] + w[t])
                T_2 = mod_add(sum_0(a) + Maj(a, b, c))

                h = g
                g = f
                f = e
                e = mod_add(d + T_1)
                d = c
                c = b
                b = a
                a = mod_add(T_1 + T_2)

            # Step 4 ----------------------------------------------------
            for i, val in enumerate([a, b, c, d, e, f, g, h]):
                self.H[i] = mod_add(self.H[i] + val)


    def hexdigest(self) -> str:
        return ''.join(map(lambda x: f"{hex(x)[2:]:0>16}", self.H))


if __name__== '__main__':
    # Mensaje a Hashear de prueba
    msg = b"Para_encontrarlo_debes_mirar_mas_alla_de_lo_que_ves"

    msg_hash = sha512(msg)
    msg_hash_hex = msg_hash.hexdigest()

    standard_hash = hashlib.sha512(msg)
    standard_hash_hex = standard_hash.hexdigest()

    print(f"Mensaje: {msg}")
    print(f"Hash con hashlib.sha512:\n {standard_hash_hex}")
    print(f"Custom SHA512:\n {msg_hash_hex}")
    print(f"¿Son iguales los hash?: {standard_hash_hex==msg_hash_hex}")


