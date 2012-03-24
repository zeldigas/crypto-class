#!/usr/bin/env python

from itertools import combinations, chain

msg = (
'315c4eeaa8b5f8aaf9174145bf43e1784b8fa00dc71d885a804e5ee9fa40b16349c146fb778cdf2d3aff021dfff5b403b510d0d0455468aeb98622b137dae857553ccd8883a7bc37520e06e515d22c954eba50',
'234c02ecbbfbafa3ed18510abd11fa724fcda2018a1a8342cf064bbde548b12b07df44ba7191d9606ef4081ffde5ad46a5069d9f7f543bedb9c861bf29c7e205132eda9382b0bc2c5c4b45f919cf3a9f1cb741',
'32510ba9a7b2bba9b8005d43a304b5714cc0bb0c8a34884dd91304b8ad40b62b07df44ba6e9d8a2368e51d04e0e7b207b70b9b8261112bacb6c866a232dfe257527dc29398f5f3251a0d47e503c66e935de812',
'32510ba9aab2a8a4fd06414fb517b5605cc0aa0dc91a8908c2064ba8ad5ea06a029056f47a8ad3306ef5021eafe1ac01a81197847a5c68a1b78769a37bc8f4575432c198ccb4ef63590256e305cd3a9544ee41',
'3f561ba9adb4b6ebec54424ba317b564418fac0dd35f8c08d31a1fe9e24fe56808c213f17c81d9607cee021dafe1e001b21ade877a5e68bea88d61b93ac5ee0d562e8e9582f5ef375f0a4ae20ed86e935de812',
'32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd2061bbde24eb76a19d84aba34d8de287be84d07e7e9a30ee714979c7e1123a8bd9822a33ecaf512472e8e8f8db3f9635c1949e640c621854eba0d',
'32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd90f1fa6ea5ba47b01c909ba7696cf606ef40c04afe1ac0aa8148dd066592ded9f8774b529c7ea125d298e8883f5e9305f4b44f915cb2bd05af513',
'315c4eeaa8b5f8bffd11155ea506b56041c6a00c8a08854dd21a4bbde54ce56801d943ba708b8a3574f40c00fff9e00fa1439fd0654327a3bfc860b92f89ee04132ecb9298f5fd2d5e4b45e40ecc3b9d59e941',
'271946f9bbb2aeadec111841a81abc300ecaa01bd8069d5cc91005e9fe4aad6e04d513e96d99de2569bc5e50eeeca709b50a8a987f4264edb6896fb537d0a716132ddc938fb0f836480e06ed0fcd6e9759f404',
'466d06ece998b7a2fb1d464fed2ced7641ddaa3cc31c9941cf110abbf409ed39598005b3399ccfafb61d0315fca0a314be138a9f32503bedac8067f03adbf3575c3b8edc9ba7f537530541ab0f9f3cd04ff50d',
'32510ba9babebbbefd001547a810e67149caee11d945cd7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e77472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904'
)

class DecryptTable:
    
    def __init__(self, crypt_messages_hex):
        self.crypt_messages = crypt_messages_hex
        self.xor_hash = {}
        self.key = len(self.crypt_messages[0])*[None]
        self.decoded_message = [len(m.decode('hex'))*[None] for m in self.crypt_messages]
        
        self.__gen_xored_strings()
        
    def __gen_xored_strings(self):
        for p in combinations(self.crypt_messages, 2):
        	self.xor_hash[p] = xor(p[0].decode('hex'),p[1].decode('hex'))

    def find_all_possible_spaces(self):
        spaces = []
        counter = 0
        for m in self.crypt_messages:
        	spaces = spaces + [(p[0], p[1], counter) for p in self.find_spaces(self.select_xored_strings(m))]
        	counter = counter + 1
        return sorted(sorted(spaces,key=lambda s: s[2]),key=lambda s: s[0])
    def __checkChar(self, c):
    	return ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z')
        
    def find_spaces(self, messages):
	    space_counts = len(messages[0])*[0]
	    for i in range(len(messages[0])):
		    for m in messages:
			    if self.__checkChar(m[i]):
				    space_counts[i] = space_counts[i] + 1
	    return filter(lambda p: p[1] > 6, [(i, space_counts[i]) for i in range(len(space_counts))])
    
    def select_xored_strings(self, sample):
	    list = []
	    for key in filter(lambda k: k[0] == sample or k[1] == sample, self.xor_hash):
		    list.append(self.xor_hash[key])
	    return list
    
    def decrypt_all_with_space_guess(self):
        spaces = self.find_all_possible_spaces()
        for space in spaces:
            self.decrypt_position_for_char_with_install(space[0], ' ', space[2], space[1])
            
    def decrypt_position_for_char_with_install(self, position, char, msg_with_char, space_hits=None):
        key_char, decodings = self.decrypt_position(position, char, msg_with_char);
        self.key[position] = key_char
        self.install_decoded_chars(position, decodings)
        
    def decrypt_position(self, position, char, msg_with_char):
        key = xor(char, self.crypt_messages[msg_with_char].decode('hex')[position])
        return (key, self.get_decodings(position, key))
        
    def get_decodings(self, position, key_char):
        decodings = []
        for m in self.crypt_messages:
            decodings.append(xor(key_char, m.decode('hex')[position]))
        return decodings
        
    def install_decoded_chars(self, position, decodings):
        for i in range(len(decodings)):
            self.decoded_message[i][position] = decodings[i]
            
    def print_decoded_message(self, index):
        print "".join(map(lambda c: c is None and "<None>" or c, self.decoded_message[index]))
        
def xor(m1, m2):
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(m1, m2))	

	

def print_spaces(list):
	counter = 1
	for founds in list:
		print counter, "spaces", founds
		counter = counter + 1

