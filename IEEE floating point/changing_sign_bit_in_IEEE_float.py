



import struct

import sys
flt_max = sys.float_info.max 




for v in [-5.0, 5.0, 0.0, -0.0, flt_max, -flt_max, 1e+0, 1.0, -1.0, 2.0, -2.0, 3.0, -3.0, 4.0, -4.0, 5.0, -5.0, 6.0, -6.0, 6.9, -6.9, 0.0000000000010, 0.0, 0.1, 0.5, 0.05, -0.5, -0.05, float('inf'), float('NaN')]:
    data = struct.pack('d', v)
    hex_str = data.hex()

    # for b in data:
    #     # print(b, end=' ')
    #     print(, end=' ')

    group_len = 4
    hex_str = [hex_str[i:i+group_len] for i in range(0, len(hex_str), group_len)]
    hex_str = " ".join(hex_str)
    bin_str = " ".join(["{0:08b}".format(b) for b in data])
    print( str(v).rjust(35), ":", hex_str, ":", bin_str )

print(struct.unpack("d", b'\xff\xff\xff\xff\xff\xff\xff\x7f'))
print(struct.unpack("d", b'\xff\xff\xff\xff\xff\xff\xff\xff'))


# #include <stdio.h>

# int main()
# {
#     unsigned char a1 = 0x3a;
#     double value = 5.0;
#     unsigned char a2 = 0x3a;
#     double *address = &value;
#     printf("init value: %f\n", value);
    
#     //здесь можно видеть что компилятор перемещеет
#     //переменные и адреса у них распределяются в  
#     //другом порядке, а не в порядке объявления 
#     printf("%u %u %u\n", &a1, &value, &a2);
#   
#     printf("a1: %u\n", address);
#     //printf("%u\n", sizeof(unsigned long));
#     double *address2 = (double *)((unsigned long)address+7);
#     printf("a2: %u\n", address2);
#     //unsigned char value = 200;

#     printf("%u\n", *(unsigned char*)((&value)));
#     printf("%X\n", *(unsigned char*)(address2));
    
#     unsigned char data = *(unsigned char*)(address2);
#     //data &= ~(1 << 7); //unset sign bit
#     //data |= (1 << 7); // set sign bit
#     data ^= (1 << 7); //toggle sign bit
#     *(unsigned char*)(address2) = data;
    
#     printf("result value: %f", value);
#     return 0;
# }








    # unsigned char a1 = 0x80;
    # //a1 <<= 6;
    # printf("result value: %u\n", a1);
    # printf("%X\n", a1);

    # printf("%c", a1 & 0x80 ? '1' : '0' );
    # printf("%c", a1 & 0x40 ? '1' : '0' );
    # printf("%c", a1 & 0x20 ? '1' : '0' );
    # printf("%c", a1 & 0x10 ? '1' : '0' );
    # printf("%c", a1 & 0x08 ? '1' : '0' );
    # printf("%c", a1 & 0x04 ? '1' : '0' );
    # printf("%c", a1 & 0x02 ? '1' : '0' );
    # printf("%c", a1 & 0x01 ? '1' : '0' );

    # return 0;
