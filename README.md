[![Build Status](https://dev.azure.com/freedge/freedge/_apis/build/status/freedge.ansibletest?branchName=master)](https://dev.azure.com/freedge/freedge/_build/latest?definitionId=4&branchName=master)


My ansible tester
=================

Test Ansible collections for
- brocade fc switches
- ibm svc
- cisco switches
- palo alto fw
- netapp NFS storage

(TODO: enclosures)


```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml -p ./
ansible-galaxy role install -r requirements.yml  -p ./
```

Description
-----------

Assumptions:

- we have 2 blades, blade1 and blade2, part of the same enclosure
- the enclosure have 1 interconnect, interco1
- interco1 is linked to a cisco switch, switch1
- interco1 is also linked to a brocade switch, brocadea, for storage
- brocadea is linked to interco1, and to some ibm svc nodes

We use:
- HPE Oneview, or Lenovo XClarity, to configure the blade in the enclosure (not shown here)
- cisco.nxos Ansible collection to configure switch1
- brocade.fos Ansible collection to configure the brocade switch
- ibm.spectrum_virtualize Ansible collection to configure the SVC node

Goal:
- use the vendors provided Ansible modules to configure the whole thing
- set-up a CI pipeline with Azure Devops and actually trigger these modules
- validate that the tasks and the Ansible modules work as expected with the provided Python/Ansible/collection versions
