#pragma once

#ifdef MOVEMENTLIB_EXPORTS
#define MOVEMENTLIB_API __declspec(dllexport)
#else
#define MOVEMENTLIB_API __declspec(dllimport)
#endif

extern "C" MOVEMENTLIB_API void movement(bool hit, bool jump, bool left, bool right, bool up);