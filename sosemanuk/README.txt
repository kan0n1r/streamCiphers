
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

    ----------------------------------------------------------------
    ----------------------------------------------------------------
    ----------------------------------------------------------------
