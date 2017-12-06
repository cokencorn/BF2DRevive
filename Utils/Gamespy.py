import base64


class Gamespy:
    @staticmethod
    def int32(x):
        # This function treats a number as unsigned 32-bit integer (Like C pretty much)
        if x > 0xFFFFFFFF:
            raise OverflowError
        if x > 0x7FFFFFFF:
            x = int(0x100000000 - x)
            if x < 2147483648:
                return -x
            else:
                return -2147483648
        return x

    @staticmethod
    def encode_password(password):
        # Convert to byte array
        password_bytes = bytearray(password)
        # Convert to Base64
        password = base64.b64encode(Gamespy.gs_pass_encode(password_bytes))
        # Convert Standard Base64 to Gamespy Base 64
        password = password.replace('=', '_')
        password = password.replace('+', '[')
        password = password.replace('/', ']')
        return password

    @staticmethod
    def decode_password(password):
        # Convert Gamespy Base64 to Standard Base 64
        password = password.replace('_', '=')
        password = password.replace('[', '+')
        password = password.replace(']', '/')
        password_bytes = bytearray(base64.b64decode(password))
        return Gamespy.gs_pass_encode(password_bytes)

    @staticmethod
    def gs_pass_encode(pass_bytes):
        a = 0
        num = 0x79707367  # GSPY
        for i in range(0, len(pass_bytes), 1):
            num = Gamespy.gs_lame(num)
            a = num % 0xFF
            pass_bytes[i] ^= a

        return pass_bytes

    @staticmethod
    def gs_lame(num):
        c = (num >> 16) & 0xffff
        a = num & 0xffff
        c *= 0x41a7
        a *= 0x41a7
        # Intentional 32-bit integer overflow here
        a = Gamespy.int32(a + ((c & 0x7fff) << 16))
        if a < 0:
            a &= 0x7fffffff
            a += 1
        # and here..
        a = Gamespy.int32(a + (c >> 15))
        if a < 0:
            a &= 0x7fffffff
            a += 1
        return a
