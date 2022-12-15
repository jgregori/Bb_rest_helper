# Bb_rest_helper

This library is intended to explore Blackboard´s REST APIs and to help create POCs for integrations. **Please note this tool is not oficially supported by Anthology and no warranties of any kind are provided.**

## DESCRIPTION

The Bb Rest Helper includes 4 classes to simpilfy common API operations with Blackboard APIs;

1. **Get_Config.** This class is used to get configuration variables (url,key,secret)from an external configuration file in Json format. If you are authenticating for more than one API (i.e. Learn and Collaborate) you will need separate configuration files (i.e. learn_config.json and collab_config.json).

2. **Auth_Helper.** This class is used to get the token that then will be used in the API calls. Provides different methods for the different APIs.

3. **Bb_Requests.** This class is used to simplify calls to the Blackboard Rest APIs. Provides methods for GET, POST, PUT, PATCH and DELETE requests. It also provides some other convenience methods to upload and download files from Blackboard Learn.

4. **Bb_Utils.** A set of convenience functions (Logging, printing...), this will be extended over time.

## Changes in V3 --Current version.

>⚠️ **DEPRECATION NOTE FOR COLLABORATE RELATED FEATURES IN BB REST HELPER LIBRARY**
>Blackboard Collaborate has been aquired by Class technologies in June 2022. The product is now "Class collaborate" and no longer part of the Anthology portfolio. All methods and documentation references to Collaborate have now been removed for V3. If you still need those, consider using a previous version of the library (2.0.5) but please note that functionality as deprecated.

>⚠️ **REMOVAL OF THE ALLY HELPER CLASS**
>A decision was made to remove the Ally helper class in order to keep the library generalistic and more manageable. This will likely published as a separate repository in the future.

## Main features in this release

1. Documentation has been updated and moved to the wiki in github. An effort has been made to provide better and more clear documentation, also making sure that only one version has to be maintained.
2. Includes **Unittest tests** to ensure that the code will not break due to changes and updates in the library. Tests are run before each commit.
3. Improvements to the **Auth_Helper** method to automatically request a new token upon expiration.While this will not affect many use cases, it is important for scripts that take longer to run, just note that it will be needed to call the **learn_auth** frequently. A new token will only be requested if the previous one is 1 second from expiring.
4. Implements **log rotation** to avoid log files affecting script performance in long runs.
5. Implements **connection check**. This comes in handy to pause scripts when connectivty is lost.
6. Added methods to **write and read csv files** in **Bb_utils**. These use the Python csv methods in the standard library.
7. Updated the **starter template** and provided an **starter notebook** for jupyter.
8. As part of this release a **github repository template** is provided to make starting a new project easy and convenient.
9. Provides fixes and updates for different methods in the library, these are
    * Fix a bug in Bb_PUT
    * Update **check_course_id** to use library methods instead of using requests directly
    * Update **learn_convert_external_id** to use library methods instead of using requests directly


## Usage

Find the documentation and examples for this library in the [wiki](https://github.com/JgregoriBb/Bb_rest_helper/wiki)
