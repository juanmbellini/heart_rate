# Heart Rate
Second Advanced Numerical Methods Project

## Getting Started
These instructions will install the development environment into your local machine.

### Prerequisites
1. Clone the repository

	```
	$ git clone https://github.com/juanmbellini/heart_rate.git
	```
2. Install Python and pip
	
	#### MacOS
	A. Install packages
	
	```
	$ brew install python
	```
	
	B. Update the ```PATH``` variable to use the Homebrew's python packages
	
	```
	$ echo 'export PATH="/usr/local/opt/python/libexec/bin:$PATH" # Use Homebrew python' >> ~/.bash_profile
	$ source ~/.bash_profile
	```
	
	#### Ubuntu
	```
	$ sudo apt-get install python python-pip
	```
	
3. Install [Virtualenv](https://virtualenv.pypa.io/en/latest/) 
	and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
	
	```
	$ pip install virtualenv virtualenvwrapper
	$ echo 'source /usr/local/bin/virtualenvwrapper.sh # Virtualenv/VirtualenvWrapper' >> ~/.bash_profile
	$ source ~/.bash_profile
	```

4. Create a virtual environment for the project

	```
	$ mkvirtualenv heart_rate
	```

	**Note:** This will install ```setuptools```, ```pip``` and ```wheel``` modules in the new virtual environment.

### Build
1. Move to the new virtual environment and change working directory to project's root

	```
	$ workon heart_rate
	```
	**Note:** To leave the virtual environment, execute 
   
    ```
    $ deactivate
    ```

2. Install dependencies

	```
	$ pip install -r requirements.txt
	```

3. Install module

	```
	$ python setup.py clean --all install
	```

## Usage
The application can be run executing the ``heart_rate`` command. 
The following sections will explain the different options and arguments that can be used.

### Displaying usage message
You can display the usage message using the ```-h``` or ```--help``` arguments. For example:
```
$ heart_rate --help
```

### Displaying version number
You can check the version of the module using the ```-V``` or ```--version``` arguments. For example:
```
$ heart_rate -V
```

### Logging verbosity

#### Logging levels
There are three levels of logging verbosity: 
* **Normal**
* **Verbose** 
* **Very Verbose**.

Normal verbosity logging will log **WARNING**, **ERROR** and **CRITICAL** messages.
Verbose logging will log what Normal logging logs, and **INFO** messages.
Very Verbose logging is the same as Verbose logging, adding **DEBUG** messages.

#### Selecting a logging level
##### Normal Verbosity Logging
To use **Normal** verbosity logging just execute the command. **Normal** verbosity logging is the default
##### Verbose Logging
To use **Verbose** logging, add the ```-v``` or ```--verbose``` arguments. For example:
```
$ heart_rate --verbose
```
##### Very Verbose Logging
To use **Very Verbose** logging, add the ```-vv``` or ```--very-verbose``` arguments. For example:
```
$ heart_rate -vv
```

### Setting video path
To set the video's path to analize, use the ```-vp``` or ```--video_path``` arguments. For example:
```
$ heart_rate -vp ~/video.mp4
```
The default value is the directory ```./video```.

### Setting region of interest (ROI)
The rectangular region of interest consist of four limits. Each one specified by a parameter. This parameters are required and
must be consistent, else the program will no work\
To set the upper limit, use the ```-rUL``` or ```--roi-upper-limit``` argument. For example:
```
$ heart_rate -rUL 200
```

To set the lower limit, use the ```-rLL``` or ```--roi-lower-limit``` argument. For example:
```
$ heart_rate -rLL 250
```

To set the right limit, use the ```-rrL``` or ```--roi-right-limit``` argument. For example:
```
$ heart_rate -rrL 100
```

To set the left limit, use the ```-rlL``` or ```--roi-left-limit``` argument. For example:
```
$ heart_rate -rlL 150
```

### Setting bandpass frequencies
To set the bandpass maximum frequency, use the ```-MF``` or ```--max-freq``` arguments. For example:
```
$ heart_rate --MF 7.0
```
The default value is ``7.0``.

To set the bandpass minimum frequency, use the ```-mF``` or ```--min-freq``` arguments. For example:
```
$ heart_rate --mF 0.4
```
The default value is ``0.4``.


### Setting the channel to process
To set BLUE channel, use the ```-B``` or ```--blue``` arguments. For example:
```
$ heart_rate -B
```

To set RED channel, use the ```-R``` or ```--red``` arguments. For example:
```
$ heart_rate -R
```

To set GREEN channel, use the ```-G``` or ```--green``` arguments. For example:
```
$ heart_rate -G
```

The default channel is GREEN.

### Example
Here is a full example usign all arguments:
```
$ heart_rate -rUL 600 -rLL 630 -rlL 300 -rrL 360  -mF 2.2 -MF 4.0 -G -vp videos/1_seg_120ppm.MOV
```

## Authors
* [Juan Marcos Bellini](https://github.com/juanmbellini)
* [Tomás de Lucca](https://github.com/tomidelucca)
* [José Noriega](https://github.com/jcnoriega)
* [Agustín Scigliano](https://github.com/agustinscigliano)