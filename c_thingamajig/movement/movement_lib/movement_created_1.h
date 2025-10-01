#pragma once

#ifdef MOVEMENTLIB_EXPORTS
#define MOVEMENTLIB_API __declspec(dllexport)
#else
#define MOVEMENTLIB_API __declspec(dllimport)
#endif

extern "C" MOVEMENTLIB_API void test_AGH();