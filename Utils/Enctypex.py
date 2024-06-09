class GSEncodingData(object):
    encoding_key = bytearray(261)
    offset = None
    start = None


class Enctypex(object):
    @staticmethod
    def copy(arr_1, arr_2):
        for i in range(0, len(arr_2)):
            arr_1[i] = arr_2[i]
        return arr_1

    @staticmethod
    def constrained_copy(s_array, s_copy_start, d_array, d_store_start, num_elems_to_copy):
        elems_copied = 0
        for index in range(s_copy_start, len(s_array)):
            d_array[d_store_start] = s_array[index]
            elems_copied += 1
            d_store_start += 1
            if elems_copied >= num_elems_to_copy:
                break
        return d_array

    @staticmethod
    def encode(key, validate, data):

        size = len(data)
        num_array = bytearray(size + 23)
        num_array_1 = bytearray(23)

        if key is None or validate is None or data is None or size < 0:
            print("Enctypex input error.")
            return None

        length = len(key)
        num = len(validate)
        num_1 = 100000000  # randint(100000000, 999999999) I mean, who cares?

        for i in range(0, len(num_array_1)):
            num_1 = num_1 * 214013 + 2531011
            num_array_1[i] = ((num_1 ^ key[i % length] ^ validate[i % num]) % 256)

        num_array_1[0] = 235
        num_array_1[1] = 0
        num_array_1[2] = 0
        num_array_1[8] = 228

        for x in range(size - 1, -1, -1):
            num_array[len(num_array_1) + x] = data[x]

        num_array = Enctypex.copy(num_array, num_array_1)
        size = size + len(num_array_1)

        num_array_2 = Enctypex.two(key, validate, num_array, size, None)
        num_array_3 = bytearray(len(num_array_2) + len(num_array_1))
        num_array_3 = Enctypex.constrained_copy(num_array_1, 0, num_array_3, 0, len(num_array_1))
        num_array_3 = Enctypex.constrained_copy(num_array_2, 0, num_array_3, len(num_array_1), len(num_array_2))

        # DEBUG - BEGIN
        #    print ("Enctypex Debug --- BEGIN")
        #    for i in range(0, len(num_array_3)):
        #        print str(i) + " : " + str(num_array_3[i])
        #    print ("Enctypex Debug --- END")
        # DEBUG - END

        return num_array_3

    @staticmethod
    def two(u0002, u0003, u0005, u0008, u0006):

        num_array_1 = bytearray(261)
        num_array = u0006.encoding_key if u0006 is not None else num_array_1
        # u0002, u0008, u0006, u000e passed back respectively
        # PPN: numArray, u0005, u0008, u0006
        if u0006 is None or u0006.start == 0:
            result = Enctypex.three(num_array, u0002, u0003, u0005, u0008, u0006)
            num_array = result[0]
            u0005 = result[1]
            u0008 = result[2]
            u0006 = result[3]
            if u0005 == None:
                return None

        if u0006 is None:
            result = Enctypex.four(num_array, u0005, u0008)
            # Do not remove num_array
            num_array = result[0]
            u0005 = result[1]
            return u0005

        # TODO: Never validated below here.. might be problematic

        if u0006.start == 0:
            return None

        print("Enctypex: u0006 is None. Data (u0006): " + str(u0006))

        num_array_2 = bytearray(u0008 - u0006.offset)
        num_array_2 = Enctypex.constrained_copy(u0005, u0006.offset, num_array_2, 0, u0008 - u0006.offset)

        result = Enctypex.four(num_array, num_array_2, (u0008 - u0006.offset))
        # Do not remove num_array
        num_array = result[0]
        num_array_2 = result[1]
        num = result[2]
        u0005 = Enctypex.constrained_copy(num_array_2, 0, u0005, u0006.offset, u0008 - u0006.offset)
        offset = u0006
        offset.offset = offset.offset + num
        num_array_3 = bytearray(u0008 - u0006.start)
        num_array_3 = Enctypex.constrained_copy(u0005, u0006.start, num_array_3, 0, u0008 - u0006.start)
        return num_array_3

    @staticmethod
    def three(u0002, u0003, u0005, u0008, u0006, u000e):
        # OK
        # u0002, u0008, u0006, u000e passed back respectively
        # Call: numArray, u0005, u0008, u0006
        num = ((u0008[0] ^ 236) + 2)

        if u0006 < 1:
            return None

        if u0006 < num:
            return None

        num_1 = (u0008[num - 1] ^ 234)

        if u0006 < num + num_1:
            return None

        num_array = u0005[:8]
        num_array_1 = u0008[num:u0006]
        # PB (u0002, skip, skip, not ref, not ref)
        u0002 = Enctypex.six(u0002, u0003, num_array, num_array_1, num_1)
        u0008 = Enctypex.constrained_copy(num_array_1, 0, u0008, num, u0006 - num)
        num = num + num_1

        if u000e is not None:
            u000e.offset = num
            u000e.start = num
        else:
            num_array_2 = u0008[num:u0006]
            u0008 = num_array_2
            u0006 = u0006 - num

        return [u0002, u0008, u0006, u000e]

    @staticmethod
    def four(u0002, u0003, u0005):
        # OK
        for i in range(0, u0005):
            u0003[i] = Enctypex.five(u0002, u0003[i])
        return [u0002, u0003, u0005]

    @staticmethod
    def five(u0002, u0003):
        # OK
        num = u0002[256]
        num_1 = u0002[257]
        num_2 = u0002[num]
        u0002[256] = ((num + 1) % 256)
        u0002[257] = ((num_1 + num_2) % 256)
        num = u0002[260]
        num_1 = u0002[257]
        num_1 = u0002[num_1]
        num_2 = u0002[num]
        u0002[num] = num_1
        num = u0002[259]
        num_1 = u0002[257]
        num = u0002[num]
        u0002[num_1] = num
        num = u0002[256]
        num_1 = u0002[259]
        num = u0002[num]
        u0002[num_1] = num
        num = u0002[256]
        u0002[num] = num_2
        num_1 = u0002[258]
        num = u0002[num_2]
        num_2 = u0002[259]
        num_1 = (num_1 + num) % 256
        u0002[258] = num_1
        num = num_1
        num_2 = u0002[num_2]
        num_1 = u0002[257]
        num_1 = u0002[num_1]
        num = u0002[num]
        num_2 = (num_2 + num_1) % 256
        num_1 = u0002[260]
        num_1 = u0002[num_1]
        num_2 = (num_2 + num_1) % 256
        num_1 = u0002[num_2]
        num_2 = u0002[256]
        num_2 = u0002[num_2]
        num = (num + num_2) % 256
        num_2 = u0002[num_1]
        num_1 = u0002[num]
        num_2 = (num_2 ^ num_1 ^ u0003) % 256
        u0002[260] = num_2
        u0002[259] = u0003
        return num_2

    @staticmethod
    def six(u0002, u0003, u0005, u0008, u0006):
        # OK
        # Call (u0002, skip, skip, non ref, non ref)
        length = len(u0003)
        for i in range(0, u0006):
            u0005[u0003[i % length] * i & 7] = (u0005[u0003[i % length] * i & 7] ^ u0005[i & 7] ^ u0008[i])
        num = 8
        u0002 = Enctypex.seven(u0002, u0005, num)
        return u0002

    @staticmethod
    def seven(u0002, u0003, u0005):
        # OK
        num = 0
        num_1 = 0

        if u0005 < 1:
            return

        for i in range(0, 256):
            u0002[i] = i

        for i in range(255, -1, -1):
            result = Enctypex.eight(u0002, i, u0003, u0005, num, num_1)
            # num and num_1 are refs
            num = result[1]
            num_1 = result[2]
            num_2 = result[0]
            num_3 = u0002[i]

            u0002[i] = u0002[num_2]
            u0002[num_2] = num_3

        u0002[256] = u0002[1]
        u0002[257] = u0002[3]
        u0002[258] = u0002[5]
        u0002[259] = u0002[7]
        u0002[260] = u0002[num & 255]

        return u0002

    @staticmethod
    def eight(u0002, u0003, u0005, u0008, u0006, u000e):
        # OK
        num_1 = 0
        num_2 = 1

        if u0003 == 0:
            return [0, u0006, u000e]

        if u0003 > 1:
            while True:
                num_2 = (num_2 << 1) + 1
                if num_2 < u0003:
                    continue
                else:
                    break

        while True:
            u0006 = (u0002[u0006 & 255] + u0005[u000e])
            u000e = u000e + 1

            if u000e >= u0008:
                u000e = 0
                u0006 = u0006 + u0008

            num_1 = num_1 + 1
            num = u0006 & num_2 if num_1 <= 11 else u0006 & num_2 % u0003

            if num > u0003:
                continue
            else:
                break

        # PB
        return [num, u0006, u000e]
