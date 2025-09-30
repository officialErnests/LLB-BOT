#include <iostream>

class Foo{
    public:
        void bar(){
            std::cout << "Hello" << std::endl;
        }
};

int main() {
    
    
    __declspec(dllexport) Foo* Foo_new(){ return new Foo(); }    
    __declspec(dllexport) void Foo_bar(Foo* foo){ foo->bar(); } 
}
