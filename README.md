# Dataset Explorative Platform

## Authors
Group 14 : 
- Tarun Krishnan (24697928)
- Muhsin Dawood  (24897124)
- <first and last name> (<UTS student id>)
- <first and last name> (<UTS student id>)

## Description
The application aims to provide a front end web exploration interface for datasets that will be used in various data science applications.  
It provides a simple and intuitive user interface to upload and explore a dataset, with detailed information about the components of the dataset.  

In the development of this application, most of the development was fairly straight forward, with a few obstales to iron out, namely in the domain of version control and collaborative development.  
In addition to the overal development scheme, there was an emphasis on the deployment requirements, of which we were mindful of python versioning and standard library criteria. 

A few features we could add going forward would be to include more graphs and measures that could visually aid a user to explore the facets of the dataset and its nuances with a statistical approach.

## How to Setup
The first step is to ensure you have python installed and running.
You also need to install a package manager, and we have used pip3 for this project.

The version for the python runtime is Python 3.9

After doing this, we can create and populate the project files into a working directory.

The next step is to create a virtual environment.
The following steps are for a UNIX based operating system, and the implemenation differs for Windows.

Using the following command will create a new virtual environment :
	`python3 -m venv venv_name/`
where,
	venv_name/ is the subfolder that will contain the virtual environment files
	-m venv is the command to create the virtual environment

We will then activate the virtual environment using the following command :
	`source venv/bin/activate`

We can then install the required external packages for the project to work, namely Streamlit.
You can either manually install the packages by going through the requirements.txt file :
	`pip3 install streamlit`

Alternatively, you can just install all the packages in one go, using :
	`pip3 install -r requirements.txt`

 The specific version of Streamlit used was 1.27.0, however, the latest version would also work just fine.

---

## How to Run the Program
The fastest way to run this project is to run the following command :
	`streamlit run app/streamlit_app.py`

You can optionally add flags for different run situations such as specifying a port number, or logger level:
	`streamlit run your_script.py --server.port 80`
	`streamlit run your_script.py --logger.level info`

	`streamlit run your_script.py [-- script args]`

Additional flags are available at the Streamlit documentation website, at :
	<https://docs.streamlit.io/library/advanced-features/cli>

## Project Structure
|-app
	|-__init__.py
	|-streamlit_app.py
|-tab_date
	|-__init__.py
	|-display.py
	|-logics.py
|-tab_df
	|-__init__.py
	|-display.py
	|-logics.py
|-tab_num
	|-__init__.py
	|-display.py
	|-logics.py
|-tab_text
	|-__init__.py
	|-display.py
	|-logics.py
|-.gitignore
|-README.md
|-requirements.txt
---

## Citations
Streamlit Documentation : <https://streamlit.io>
