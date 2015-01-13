#!/usr/bin/env python

import sys
import traceback

FIRSTCH = 0x20
LASTCH = 0x7e
TABSZ = (LASTCH - FIRSTCH + 1)


# xlate_out() - xlate_out the given character
# borrowed from alpine/imap.c (re-alpine 2.03)
def xlate_out(c, xlate_key):
    if c >= FIRSTCH and c <= LASTCH:
        xch = c - xlate_key
        dti = xlate_key

        if xch < (FIRSTCH - TABSZ):
            xch = xch + 2 * TABSZ
        else:
            if xch < FIRSTCH:
                xch = xch + TABSZ

        dti = (xch - FIRSTCH) + dti

        if dti >= 2 * TABSZ:
            dti = dti - 2 * TABSZ
        else:
            if dti >= TABSZ:
                dti = dti - TABSZ

        xlate_key = dti
        return xch, xlate_key
    else:
        return c, xlate_key


def xlate_in(c, xlate_key):
    eti = xlate_key
    if c >= FIRSTCH and c <= LASTCH:
        eti += (c - FIRSTCH)
        if eti >= 2*TABSZ:
            eti = eti - 2*TABSZ
        else:
            if eti >= TABSZ:
                eti = eti - TABSZ
        xlate_key = eti
        return eti + FIRSTCH, xlate_key
    else:
        return c, xlate_key


def decode_line(s, xlate_key):
    a = bytearray(s)

    for i in range(0, len(s)):
        try:
            a[i], xlate_key = xlate_out(a[i], xlate_key)
        except:
            traceback.print_exc()

    return a


def decode_passfile(filename):
    xlate_key = 0
    for line in open(filename, "rb"):  # "rb"
        sys.stdout.write("%s\n" % bytes(decode_line(line.rstrip(), xlate_key)).decode("utf-8"))
        xlate_key = xlate_key + 1


def encode_line(s, xlate_key):
    a = bytearray(s.encode("utf-8"))

    for i in range(0, len(s)):
        try:
            a[i], xlate_key = xlate_in(a[i], xlate_key)
        except:
            traceback.print_exc()

    return a.decode("utf-8")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s <.pine-passfile>\n" % sys.argv[0])
        sys.exit(-1)

    decode_passfile(sys.argv[1])
