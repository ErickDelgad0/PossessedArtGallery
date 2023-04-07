# Possessed Art Gallery

## Description
A website that allows any visitor to collectivly organize their fan art for the 
Possessed NFT. It provides an interactive timeline with the most recently submitted art.

## How To Use
When first connecting to the website you are greeted with why you should use the possessed art gallery 
that has some examples underneath. Here you can find three tabs in the top right corner of the page, Home, Register,
and Login. To register an account click the register button. Here you can type in your username and password. Choose your username carefully because this cannot be changed. After registering, you can then login or go back to the home page. Once
logged in and at the gallery homepage, you can update youre profile's first name, last name, email, and description by clicking profile in the upper right corner then manage account. Once satisfied with these changes you can then click the upload button in the upper right conrer to add a piece of art that you like. You need the image url, and can add a desciption and collection you so choose, also there is a art style drop down list you can choose.

## How To Setup Enviroment
To run this program you first want to clone the repository from GitHub, then you create a virtual environment. Once your enviroment is active, install the requirments using "pip install -r requirements.txt". Now that your first time setup is done, you are ready to run the program. 

## How To Run 
The first step is to make sure you are still in your virtual enviroment. Next, you will want to run "flask initdb". This will setup your database and destroy anything inside of it. Now all you have to do is "flask run" and the program is running.
