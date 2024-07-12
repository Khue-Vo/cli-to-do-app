"""Top-level package for CLI To-Do"""
# clitodo/__init__.py

#Two module level names to hold the application's name and version
__app_name__ = "clitodo"
__version__ = "0.1.0"

(
     SUCCESS,
     DIR_ERROR,
     FILE_ERROR,
     DB_READ_ERROR,
     DB_WRITE_ERROR,
     JSON_ERROR,
     ID_ERROR,
 ) = range(7) # A series of return and error codes


ERRORS = {
     DIR_ERROR: "config directory error",
     FILE_ERROR: "config file error",
     DB_READ_ERROR: "database read error",
     DB_WRITE_ERROR: "database write error",
     ID_ERROR: "to-do id error",
 } #A dictionary that maps error codes to human-readable error messages