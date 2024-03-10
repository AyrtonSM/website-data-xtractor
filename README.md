# website-data-xtractor

The project consists of given a file of websites listing, extract the available logo url
any possible phones that might exist in the page, and also the website name. 

The project was build using Python 3.12, and one can execute the project by executing 
any of the following approaches.

## Using Docker
Before proceeding execute your docker daemon. Once it has started do the following

#### Clone

`$ git clone https://github.com/AyrtonSM/website-data-xtractor.git`

Enter the cloned folder

`$ cd website-data-xtractor`

Execute docker build, to create an image of the project

`docker build -t website-data-xtractor .`

After finished the built, execute the following command:

`cat tests/files/websites.txt | docker run -i website-data-xtractor`

You can create your own test files and run as the above command.

That's all, have fun :) 


## Cloning and Executing

The direct approach to execute this project is to have it cloned and executed directly.

### Install Python
First, make sure you have 3.12 installed and running on your machine:
You can check it by execute the following command on your terminal window.

`$ python --version`

It should display the version of the python installed on your machine. 
On the hand, if you do not have it installed, I recommend downloading and installing before proceeding.
`https://www.python.org/downloads/release/python-3121/`

Please, make sure to add to PATH during install, so you can execute it through the terminal window.
After installing try running `$ python --version` again. 

### Cloning and Creating an environment

If you are on windows, open your cmd prompt. If you are on mac/linux, open your terminal.

type the following:

#### Clone
`$ git clone https://github.com/AyrtonSM/website-data-xtractor.git`

#### Create an environment on your cloned project.
Enter the cloned folder

`$ cd website-data-xtractor`

Create an env for this project

`$ python -m venv xtractor-env`

Activate your env:

If on Mac/Linux use: `$ source xtractor-env/Scripts/activate`

If on Windows use Powershell: `$ xtractor-env\Scripts\Activate.ps1` if you face any permission kind of error, try executing the following command on powershell
`Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process`

Your terminal/cmd should display something like this:

`(xtractor-env) YOUR_PATH_TO_PROJECT\website-data-xtractor>`

### Install Project Dependencies

Once you're in your new environment, please execute the following command to install the project dependencies:

`$ pip install -r requirements.txt`

### Run the project
To run, you can use your own files, or use the example provided below.

`cat tests/files/websites.txt | python -m app`

For an ease experience, please add your test files into the tests/files folder.
otherwise you might face issues trying to find the path to the app module. 
