#include <iostream>

int main()
{
    for(int i = 0 ; i < 256; ++i)
        std::cout<<i<<"\t"<<(char)i<<std::endl;
    system("pause");
    return 0;
}
