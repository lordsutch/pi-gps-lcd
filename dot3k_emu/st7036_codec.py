#!/usr/bin/python3

# Codec for the st7036 LCD display panel's default character set.
# Registers a codec called 'st7036'

# Copyright (c) 2019 Chris Lawrence

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import codecs

# ST7036 translation table
# Much of this turns out to be the same as CP932, so start from there

st7036_decoding_map = {i : bytes((i,)).decode('cp932', 'ignore')
                       for i in range(256)}

# This range is CP850
st7036_decoding_map.update({i : bytes((i,)).decode('cp850', 'ignore')
                            for i in range(128, 155)})

st7036_decoding_map.update( {
    # Here are the exceptions to CP932
      0: 0x2320, # ⌠
      1: 0x2321, # ⌡
      2: 0x221e, # ∞
      3: 0x2207, # ∇
      4: 0x21b2, # ↲
      5: 0x2191, # ↑
      6: 0x2193, # ↓
      7: 0x2190, # ←
      8: 0x2192, # →
      9: 0x250c, # ┌
     10: 0x2510, # ┐
     11: 0x2514, # └
     12: 0x2518, # ┘
     13: 0x2e33, # ⸳
     14: 0x00ae, # ®
     15: 0x00a9, # ©
     16: 0x2122, # ™
     17: 0x2020, # †
     18: 0x00a7, # §
     19: 0x00b6, # ¶
     20: 0x0393, # Γ
     21: 0x0394, # Δ
     22: 0x03b8, # Θ
     23: 0x039b, # Λ
     24: 0x039e, # Ξ
     25: 0x03a0, # Π
     26: 0x03a3, # Σ
     27: 0x03a4, # Τ
     28: 0x03a6, # Φ
     29: 0x03a8, # Ψ
     30: 0x03a9, # Ω
     31: 0x03aa, # α
    # 32-91 as ASCII
     92: 0x00a5, # ¥
    # 93-125 as ASCII
    126: 0x2190, # ←
    127: 0x2192, # →
    # 128-154 are same as CP850
    155: 0x00f1, # ñ
    156: 0x00d1, # Ñ
    157: 0x00aa, # ª
    158: 0x00ba, # º
    159: 0x00bf, # ¿
    # 160-223 are same as CP932
    # Lots of CP850/1252 gets shifted here randomly
    224: 0x00e1, # á
    225: 0x00ed, # í
    226: 0x00f3, # ó
    227: 0x00fa, # ú
    228: 0x00a2, # ¢
    229: 0x00a3, # £
    230: 0x00a5, # ¥
    231: 0x20a7, # ₧
    232: 0x0192, # ƒ
    233: 0x00a1, # ¡
    234: 0x00c3, # Ã
    235: 0x00a3, # ã
    236: 0x00d5, # Õ
    237: 0x00f5, # õ
    238: 0x00d8, # Ø
    239: 0x00f8, # ø
    240: 0x00b7, # · [is this right?]
    241: 0x00a8, # ¨
    242: 0x00b0, # °
    243: 0x0060, # `
    244: 0x00b4, # ´
    245: 0x00bd, # ½
    246: 0x00bc, # ¼
    247: 0x00d7, # ×
    248: 0x00f7, # ÷
    249: 0x2264, # ≤
    250: 0x2265, # ≥
    251: 0x00ab, # «
    252: 0x00bb, # »
    253: 0x2260, # ≠
    254: 0x221a, # √
    255: 0x00af, # ¯
} )
st7036_encoding_map = codecs.make_encoding_map(st7036_decoding_map)

class ST7036Codec(codecs.Codec):
    def encode(self, input, errors='strict'):
        return codecs.charmap_encode(input, errors, st7036_encoding_map)

    def decode(self, input, errors='strict'):
        return codecs.charmap_decode(input, errors, st7036_decoding_map)

class ST7036IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, errors='strict'):
        return codecs.charmap_encode(input, self.errors, st7036_encoding_map)[0]

class ST7036IncrementalDecoder(codecs.IncrementalEncoder):
    def decode(self, input, errors='strict'):
        return codecs.charmap_decode(input, self.errors, st7036_decoding_map)[0]

class ST7036StreamReader(ST7036Codec, codecs.StreamReader):
    pass

class ST7036StreamWriter(ST7036Codec, codecs.StreamWriter):
    pass

def find_st7036(encoding):
    if encoding == 'st7036':
        return codecs.CodecInfo(
            name='st7036',
            encode=ST7036Codec().encode,
            decode=ST7036Codec().decode,
            incrementalencoder=ST7036IncrementalEncoder,
            incrementaldecoder=ST7036IncrementalDecoder,
            streamreader=ST7036StreamReader,
            streamwriter=ST7036StreamWriter,
            )
    return None

codecs.register(find_st7036)

if __name__ == '__main__':
    bytetext = bytes(range(256))
    utext = bytetext.decode('st7036')
    for i in range(16):
        print(utext[16*i:16*(i+1)])


    
    
