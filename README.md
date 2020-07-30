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

