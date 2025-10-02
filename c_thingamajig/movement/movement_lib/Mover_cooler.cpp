
#include "pch.h"
#include "movement_created_1.h"
#include <iostream>
#include <WinUser.h>
using namespace std;

void movement(bool hit, bool jump, bool left, bool right, bool up) {


    INPUT inputs[5] = {};
    ZeroMemory(inputs, sizeof(inputs));

    //hit
    inputs[0].type = INPUT_KEYBOARD;
    inputs[0].ki.wVk = 'C';
    if (!hit)
    {
        inputs[0].ki.dwFlags = KEYEVENTF_KEYUP;
    }

    //jump
    inputs[1].type = INPUT_KEYBOARD;
    inputs[1].ki.wVk = VK_SPACE;
    if (!jump)
    {
        inputs[1].ki.dwFlags = KEYEVENTF_KEYUP;
    }

    //left
    inputs[2].type = INPUT_KEYBOARD;
    inputs[2].ki.wVk = VK_LEFT;
    if (!left)
    {
        inputs[2].ki.dwFlags = KEYEVENTF_KEYUP;
    }

    //right
    inputs[3].type = INPUT_KEYBOARD;
    inputs[3].ki.wVk = VK_RIGHT;
    if (!right)
    {
        inputs[3].ki.dwFlags = KEYEVENTF_KEYUP;
    }

    //up
    inputs[4].type = INPUT_KEYBOARD;
    inputs[4].ki.wVk = VK_UP;
    if (!up)
    {
        inputs[4].ki.dwFlags = KEYEVENTF_KEYUP;
    }

    UINT uSent = SendInput(ARRAYSIZE(inputs), inputs, sizeof(INPUT));
    if (uSent != ARRAYSIZE(inputs))
    {
        cout << "SendInput failed: 0x%x\n" << HRESULT_FROM_WIN32(GetLastError());
    }
}