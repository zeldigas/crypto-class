#!/usr/bin/env python

import os
from Crypto.Hash import SHA256 as sha256

class MessageHolder:
    def __init__(self):
        self.messages = set()
        self.hashes = {}

    def rand_message(self):
        return os.urandom(30)

    def next_unique_message(self):
        message = self.rand_message()
        while message in self.messages:
            message = self.rand_message()
        self.messages.add(message)
        return message;

def lsb(msg):
    msg_len = len(msg)
    trunc_msg = msg[msg_len-6:msg_len]
    return ''.join([chr( ( ord(msg[msg_len-7]) | 252 ) ^ 252 ), trunc_msg])

iteration = 1
while True:
    msg_holder = MessageHolder()
    msg_num = 0
    border = 2**25
    while msg_num < border:
        message = msg_holder.next_unique_message()
        msg_hash_lsb = lsb(sha256.new(message).digest())
        if msg_hash_lsb in msg_holder.hashes:
            print "found collision:x=%s\ny=%s\nhash=%s" % (message.encode('hex'), msg_holder.hashes[msg_hash_lsb].encode('hex'), msg_hash_lsb.encode('hex'))
            exit()
        else:
            msg_holder.hashes[msg_hash_lsb] = message
        msg_num = msg_num + 1
    print "Finished search in %d iteration" % iteration
    iteration = iteration + 1
