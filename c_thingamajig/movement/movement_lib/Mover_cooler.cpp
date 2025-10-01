
#include "pch.h"
#include "movement_created_1.h"
#include <iostream>
#include <WinUser.h>
using namespace std;

void movement_init() {


    INPUT inputs[8] = {};
    ZeroMemory(inputs, sizeof(inputs));

    //right
    inputs[0].type = INPUT_KEYBOARD;
    inputs[0].ki.wVk = VK_RIGHT;

    //left
    inputs[1].type = INPUT_KEYBOARD;
    inputs[1].ki.wVk = VK_LEFT;

    //hit
    inputs[2].type = INPUT_KEYBOARD;
    inputs[2].ki.wVk = 'c';

    //jump
    inputs[3].type = INPUT_KEYBOARD;
    inputs[3].ki.wVk = VK_SPACE;

    //right
    inputs[4].type = INPUT_KEYBOARD;
    inputs[4].ki.wVk = VK_RIGHT;
    inputs[4].ki.dwFlags = KEYEVENTF_KEYUP;

    //left
    inputs[5].type = INPUT_KEYBOARD;
    inputs[5].ki.wVk = VK_LEFT;
    inputs[5].ki.dwFlags = KEYEVENTF_KEYUP;

    //hit
    inputs[6].type = INPUT_KEYBOARD;
    inputs[6].ki.wVk = 'c';
    inputs[6].ki.dwFlags = KEYEVENTF_KEYUP;

    //jump
    inputs[7].type = INPUT_KEYBOARD;
    inputs[7].ki.wVk = VK_SPACE;
    inputs[7].ki.dwFlags = KEYEVENTF_KEYUP;

    UINT uSent = SendInput(ARRAYSIZE(inputs), inputs, sizeof(INPUT));
    if (uSent != ARRAYSIZE(inputs))
    {
        cout << "SendInput failed: 0x%x\n" << HRESULT_FROM_WIN32(GetLastError());
    }
}