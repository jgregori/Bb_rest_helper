# Bb_rest_helper

This library is intended to explore Blackboard´s REST APIs and to help create POCs for integrations. **Please note this tool is not oficially supported by Anthology and no warranties of any kind are provided.**

## DESCRIPTION

The Bb Rest Helper includes 5 classes to simpilfy common API operations with Blackboard APIs;

1. **Get_Config.** This class is used to get configuration variables (url,key,secret)from an external configuration file in Json format. If you are authenticating for more than one API you will need separate configuration files.

2. **Auth_Helper.** This class is used to get the token that then will be used in the API calls. Provides different methods for the different APIs.

3. **Bb_Requests.** This class is used to simplify calls to the Blackboard Rest APIs. Provides methods for GET, POST, PUT, PATCH and DELETE requests. It also provides some other convenience methods to upload and download files from Blackboard Learn.

4. **Bb_Utils.** A set of convenience functions (Logging, printing...), this will be extended over time.

5. **Ally_Helper** This class is used to simplify interaction with Ally as a service, includes methods to authenticate, upload a file, check processing status and retrieve the feedback. As it is an initial release for this API with limited features, it is implemented as a separate class to provide easier access to these methods rather than having to code them manually or with the Bb_rest_helper library.

## Changes in NEXT release (V3) --> Expected end of October 22

>⚠️ **DEPRECATION NOTE FOR COLLABORATE RELATED FEATURES IN BB REST HELPER LIBRARY**

>Blackboard Collaborate has been aquired by Class technologies in June 2022. The product is now "Class collaborate" and no longer part of the Anthology portfolio. All methods and documentation references to Collaborate have now been removed for V3. If you still need those, consider using a previous version of the library (2.0.5) but please consider that functionality as deprecated.

### Main features in this release

1. Documentation has been updated and moved to the wiki in github.An effort has been made to provide better and more clear documentation, also making sure that only one version has to be maintained.
2. Improvements to the **Auth_Helper** to automatically request a new token upon expiration
3. Implements **log rotation** to avoid log files affecting script performance in long runs
4. Implements **connection check**. This comes in handy to pause scripts when connectivty is lost
5. Added methods to **write and read csv files** in **Bb_utils**
6. Updated the **starter template** and provided an **starter notebook** for jupyter.
7. Provides a github repository template to make starting a new project easy and convenient.

## Usage

Find the documentation and examples for this library in the [wiki](https://github.com/JgregoriBb/Bb_rest_helper/wiki)
