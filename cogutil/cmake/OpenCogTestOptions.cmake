# OpenCogTestOptions.cmake
# Provides the OPENCOG_SETUP_TESTING macro for configuring test infrastructure.
# This macro should be called after all dependencies have been found to set up
# the testing framework for OpenCog-based projects.

MACRO(OPENCOG_SETUP_TESTING)
	ENABLE_TESTING()
	IF (NOT TARGET tests)
		ADD_CUSTOM_TARGET(tests)
	ENDIF()
ENDMACRO(OPENCOG_SETUP_TESTING)
