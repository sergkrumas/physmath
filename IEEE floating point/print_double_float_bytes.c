/******************************************************************************

                            Online C Compiler.
                Code, Compile, Run and Debug C program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <stdio.h>
#include <math.h>

#define BYTE_TO_BINARY_PATTERN "%c%c%c%c%c%c%c%c"
#define BYTE_TO_BINARY(byte)  \
  (byte & 0x80 ? '1' : '0'), \
  (byte & 0x40 ? '1' : '0'), \
  (byte & 0x20 ? '1' : '0'), \
  (byte & 0x10 ? '1' : '0'), \
  (byte & 0x08 ? '1' : '0'), \
  (byte & 0x04 ? '1' : '0'), \
  (byte & 0x02 ? '1' : '0'), \
  (byte & 0x01 ? '1' : '0') 

typedef unsigned char UCH;
int main()
{
    double f = sqrt(-4);
    double m = sqrt(-4);
    double mm = sqrt(-4);
    m = 0.5f;
    int i = 2;
    
    printf("%u \n", &m);
    printf("%u \n", &mm);
    printf("%i \n", sizeof(void*));
    printf("%u \n", (char*)((unsigned int)(&m)+8));

//    printf("m: "BYTE_TO_BINARY_PATTERN" "BYTE_TO_BINARY_PATTERN" "BYTE_TO_BINARY_PATTERN" "BYTE_TO_BINARY_PATTERN"\n" ,
//        BYTE_TO_BINARY((UCH)m>>32)), 
//        BYTE_TO_BINARY((UCH)m>>16),
//        BYTE_TO_BINARY((UCH)m>>8),
//        BYTE_TO_BINARY((UCH)m) 
    ///);
    //printf("%f", f);

    return 0;
}
