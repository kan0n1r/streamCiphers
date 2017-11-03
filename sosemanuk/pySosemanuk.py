#!/usr/bin/env python
# coding: utf-8

"""

    Sosemanuk: a Fast Streaming Cipher
    ----------------------------------

    Sosemanuk is a fast stream cipher and one of the "winners" 
    of the eSTREAM competition.  Sosemanuk effectively creates a 
    one-time pad that is XORed with the data, making encryption 
    and decryption the same operation.  
    
        design strength     128 bits
        key length          1-32 bytes
        IV, aka nonce       0-16 bytes
        chunk size          in increments of 80 bytes
    
    Sosemanuk was created by Come Berbain, Olivier Billet, 
    Nicolas Courtois, Henri Gilbert, Louis Goubin, Aline Gouget, 
    Louis Granboulan, Cedric Lauradoux, Marine Minier, Thomas 
    Pornin and Herve Sibert.  Their reference implementation is 
    free software; its license is "as close to Public Domain as 
    any software license can be under French law".  See:
      http://www.ecrypt.eu.org/stream/sosemanukpf.html
      http://www.ecrypt.eu.org/stream/p3ciphers/sosemanuk/sosemanuk_p3.pdf
    
    
    pySosemanuk.py
    --------------
    
    pySosemanuk is a simple Python ctypes wrapper for Sosemanuk.  
    
      Usage:
        sm = Sosemanuk(key, IV)
        dataout = sm.encryptBytes(datain)   # same for decrypt
    
    To make your learning and experimentation less cumbersome, 
    pySosemanuk.py is free for any use, but...

      Copyright (c) 2007-2011 by Larry Bugbee, Kent, WA
      ALL RIGHTS RESERVED.

      pySosemanuk.py IS EXPERIMENTAL SOFTWARE FOR EDUCATIONAL 
      PURPOSES ONLY. IT IS MADE AVAILABLE "AS-IS" WITHOUT 
      WARRANTY OR GUARANTEE OF ANY KIND, NO EXCEPTIONS. USE 
      SIGNIFIES ACCEPTANCE OF ALL RISK.
    
    Enjoy,
      
    Larry Bugbee
    bugbee@seanet.com
    March 12, 2007
    rev Dec 2008
    rev Jul 2011


    
    Prerequisites:
    --------------
      - Python 2.5 (or 2.4 with ctypes added)
      - Download and unpack 
          http://www.ecrypt.eu.org/stream/p3ciphers/sosemanuk/sosemanuk_p3source.zip

    Installation:
    -------------
      MacOSX - compile and install libsosemanuk.so:
          export MACOSX_DEPLOYMENT_TARGET=10.4
          gcc -fPIC -O3 -dynamiclib   \
                        -o libsosemanuk.so  sosemanuk.c
          sudo cp libsosemanuk.so /usr/local/lib
      
      Linux - compile and install libsosemanuk.so:
          gcc -fPIC -O3 -shared -o libsosemanuk.so sosemanuk.c
          sudo cp libsosemanuk.so /usr/local/lib  # Mandrivia: /usr/lib
      
      Install pySosemanuk.py:
        sudo python setup.py install
            
    Notes:
    ------
      be sure to compile sosemanuk.c and install as a shared 
      library, not a Python extension.
    
      If you disable #define SOSEMANUK_ECRYPT near the top of 
      sosemanuk.h, you get the following functions instead of 
      the eSTREAM APIs.
            sosemanuk_encrypt
            sosemanuk_init
            sosemanuk_internal
            sosemanuk_prng
            sosemanuk_schedule

    
"""

from ctypes import *
import sys

_version = '0.01'

#---------------------------------------------------------------

class Sosemanuk(object):
    def __init__(self, key, IV=''):
        self._ctx = c_buffer(452)   # fm ECRYPT_ctx_size(), see below
        self.setKey(key)
        self.IV = None
        if IV:  self.init(IV)

    def setKey(self, key):
        assert 1 <= len(key) <= 32, 'key not 1..32 bytes'
        libsosemanuk.ECRYPT_keysetup(byref(self._ctx), 
                                     key, 
                                     len(key)*8,
                                     128)       # IV len in bits
        
    def init(self, IV):
#        assert 1 <= len(IV) <= 16, 'nonce (IV) not 1..16 bytes'
        assert len(IV) == 16, 'ECRYPT nonce (IV) not 128 bits'
        self.IV = IV
        self.reset()
    
    def reset(self):
        assert self.IV, 'IV not set'
        libsosemanuk.ECRYPT_ivsetup(byref(self._ctx), self.IV)
    
    def encryptBytes(self, data):
        assert self.IV, 'IV not set'
        munged = c_buffer(len(data))
        libsosemanuk.ECRYPT_process_bytes(0,  # encrypt same as decrypt
                                          byref(self._ctx), 
                                          data, byref(munged), 
                                          len(data))
        return munged.raw

    decryptBytes = encryptBytes

# disabled because not sufficently tested.....    
#    def prng(self, numkeystreambytes):
#        keystream = c_buffer(numkeystreambytes)
#        libsosemanuk.ECRYPT_keystream_bytes(byref(self._ctx), 
#                                            byref(keystream), 
#                                            numkeystreambytes)
#        return keystream.raw

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# load the shared library into ctypes

def loadLib(name):
    # prefix might need to change for some platforms       ???
    prefix = ''
    # get the correct library suffix
    libsuffixes = {'darwin': '.so',     # .dylib           ???
                   'linux':  '.so', 
                   'linux2': '.so', 
                   'win32':  '.dll'}    # .so  .lib        ???
    try:
        libsuffix = libsuffixes[sys.platform]
    except:
        raise Exception('library suffix for "%s" is what?' % 
                                                  sys.platform)
    libname = prefix+'lib'+name+libsuffix
    return CDLL(libname)                # load the library


libsosemanuk = loadLib('sosemanuk')
# if add this to ecrypt-sync.h, then get and print size...
# currently 452
#    int ECRYPT_ctx_size() { return sizeof(ECRYPT_ctx); }
# print libsosemanuk.ECRYPT_ctx_size()


#---------------------------------------------------------------
#---------------------------------------------------------------
# a quick self-test.  Invoke with:  python pySosemanuk.py

def test():
    # message = loadfmfile('testdata.txt')
    message = 'Kilroy was here!  ...and there.'
    key     = 'myKey'               # do better in real life
    nonce   = 'aNonce'              # do better in real life
    IV      = (nonce+'*'*16)[:16]   # force to exactly 128 bits
    print '  pySosemanuk version: %s' % _version
    
    # encrypt
    sm = Sosemanuk(key, IV)
    # time.clock()
    ciphertxt = sm.encryptBytes(message)
    # print time.clock()
    
    # decrypt (really the same as encrypt)
    sm.reset()
    plaintxt  = sm.encryptBytes(ciphertxt[:160]) # 80-byte incr
    plaintxt += sm.decryptBytes(ciphertxt[160:])

    if message == plaintxt:
        print '    *** good ***'
    else:
        print '    *** bad ***'

#    print [hex(ord(i)) for i in sm.prng(10)]
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == '__main__':
    test()

#---------------------------------------------------------------
#---------------------------------------------------------------
#---------------------------------------------------------------
