# primehub-admin-notebook
[![CircleCI](https://circleci.com/gh/InfuseAI/primehub-admin-notebook.svg?style=svg)](https://circleci.com/gh/InfuseAI/primehub-admin-notebook)

# Kubernetes Management Tasks

This is a notebook for common kubernetes operations against PrimeHub.
These listed operations can be executed independently.

*Note: You should be aware of where and how the jupyter session is running, as kubernetes credentials are sensitive information and leakage posts security risks.*

## Caution: 
Before you execute operations, please check your kubectl and cluster health according to section **1.1 Configure kubectl** and section **1.2 Check version and cluster health** respectively first.


## 1.3 Delete user pvc

Executing 1st cell in the section, it shows a dropdown list as below, select user pvc which you want to delete.

![](/img/Untitled-04de7b40-77ce-4259-a225-ea4098074bc8.png)

After selection, executes 2nd cell for deletion.


## 1.4 Create pv-type dataset

Executing 1st cell in the section, it shows a dropdown list as below, select Target where to create dataset.

![](/img/Untitled-fbf85ce4-cd5e-42ce-8b66-aea82388d9e5.png)

Executing next cell to have a input field of size of a dataset.

![](/img/Untitled-f1804dff-04c5-4cc3-818d-bc08267db290.png)

Executing next cell below to determine the `storage_class` as below.

![](/img/Untitled-8fe271b1-dbe6-42fb-8e9e-42d2357671b3.png)

Executing next cell below to prepare specific yaml string.

![](/img/Untitled-14734d67-417d-4b23-9573-e2a8e0b7ce08.png)

Executing next cell to apply the yaml to create the pv-type dataset.

![](/img/Untitled-cf5bb3bf-af72-4f2f-befa-70724130d4ef.png)
