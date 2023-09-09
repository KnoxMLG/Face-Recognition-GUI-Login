# Face Recognition GUI Login
> An account creation and login application utilizing MySQL to authenticate users using instances of their face.

#### Table of Contents 
- [Usage Guide](#inst)
- [License](#lics)

<a name="inst"></a>
## Usage Guide
> This is an explicit Windows-Only application, as it utilizes the win32crypt library.

As long as a user has login credentials to a mysql server, the application will create the necessary tables and columns on first startup to allow the processes to function properly. All data then stored on that table is encrypted, and can only be decrypted by the windows login that had encrypted them in the first place.

<a name="lics"></a>
## License
This project is licensed under the MIT License. [License Details](../master/LICENSE)
