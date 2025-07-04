




// 1. Обмен значениями

    a ^= b      a=a+b
    b ^= a      b=a-b
    a ^= b      a=a-b


// 2. Выполнение ровно n раз
    while (n-->0)
        { use(n) }

// 3. меняем 0 на 1, потом снова на 0, и на 1
    x = 0 // или 1
    x = 1-x

// 4. Как считать ненулевые биты?
    res = 0;
    while(a){
        a&= a-1;
        res++; 
    }

// 5. Трюки от Крыса. Журнал Хакер 122 февраль 2009


// 6. Этот алгоритм позволяет быстро и эффективно определить количество значащих битов в числе, используя минимальное количество операций.
// https://s-o-c.org/using-de-bruijn-sequences-for-faster-count-leading-zeros-clz/
    static const int DeBruijnClz[32] = {0, 9, 1, 10, 13, 21, 2, 29, 11, 14, 16, 18, 22, 25, 3, 30,
            8, 12, 20, 28, 15, 17, 24, 7, 19, 27, 23, 6, 26, 5, 4, 31};

    static inline uint32_t get_bit_length(uint32_t v)
    {
      v |= v >> 1;
      v |= v >> 2;
      v |= v >> 4;
      v |= v >> 8;
      v |= v >> 16;

      return DeBruijnClz[(unsigned int)(v * 0x07C4ACDDU) >> 27] + 1;
    }
