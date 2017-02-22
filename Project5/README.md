# Item Catalog


### How to run

This simple web application uses GitHub for authorization and authentication.  To simulate security best practices, the API keys are not in the main application file or hard-coded.  
However, to facilitate grading, a shell script, `export_keys.sh`, is available to export API keys 
to server environment variables.

1. Download or clone the `Project5/vagrant` directory.
2. Initialize the Vagrant vm via `vagrant up`, which should set up on `localhost:5000`.
3. Connect to the virtual machine: `vagrant ssh`.
4. (Optional) Obtain your own GitHub API keys by [registering a new application](https://github.com/settings/applications).  Ensure you add `localhost:5000/github-callback` as the authorization callback URL.
5. (Optional) Inside the virtual machine, 
`export GITHUB_CLIENT_ID` and `export GITHUB_CLIENT_SECRET`.
6. `cd /vagrant/catalog`
7. Run the provided key export shell script: `source export_keys.sh`.
8. Start the server: `python application.py`.
9. Navigate to `localhost:5000`.  The first-time run of the server will initialize the database with fixture data.
