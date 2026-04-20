
# Backwards-compatibility wrapper
INCLUDE(OpenCogAtomTypes)

# Macro to add a named test target (if not already defined)
MACRO(OPENCOG_ADD_TEST_TARGET NAME)
    IF (NOT TARGET ${NAME})
        ADD_CUSTOM_TARGET(${NAME})
    ENDIF()
ENDMACRO(OPENCOG_ADD_TEST_TARGET)
