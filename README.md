[![Build Status](https://dev.azure.com/freedge/freedge/_apis/build/status/freedge.ansibletest?branchName=master)](https://dev.azure.com/freedge/freedge/_build/latest?definitionId=1&branchName=master)


My ansible tester
=================

Test Ansible collections for
- brocade fc switches
- ibm svc switches
- cisco switches

(TODO: enclosures)


```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml -p ./
ansible-galaxy role install -r requirements.yml  -p ./
```

