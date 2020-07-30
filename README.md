# Plant-e

## Installation

It is recccomended to use VSCode as an IDE, along with [micropy-cli](https://github.com/BradenM/micropy-cli) as it provides:

* Linting
* Dependency management
* Version Control System (VCS) compatibility

```
# Clone project
git clone https://github.com/LoJunKai/Plant-e.git
cd Plant-e

# Create virtual environment
python3 -m venv env
source env/bin/activate

# Install packages
python3 -m pip install micropy-cli pylint

# Set up Micropy environment locally
micropy
```