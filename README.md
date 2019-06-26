# primehub-admin-notebook
[![CircleCI](https://circleci.com/gh/InfuseAI/primehub-admin-notebook.svg?style=svg)](https://circleci.com/gh/InfuseAI/primehub-admin-notebook)

# Kubernetes Management Tasks

This is a notebook for common kubernetes operations against PrimeHub.
These listed operations can be executed independently.

*Note: You should be aware of where and how the jupyter session is running, as kubernetes credentials are sensitive information and leakage posts security risks.*

## Caution: Configure kubectl

If you did not start this notebook with pre-configured KUBECONFIG, you may paste your `kubectl config view --raw --minify` output here. Otherwise skip to the next section.

Notes: 

- if you use gke, your `kubectl config` contains a token that a valid for an hour. Run `kubectl get cs` to refresh token locally before copying the config.

    import ipywidgetsfrom kubeconfig 
    import KubeConfig
    k = KubeConfig()
    k.test()

Set up your `KubeConfig`

    k.setup()

## Check version and cluster health

Display the Kubernetes version running on the client and server.

    !! kubectl version

Display *ComponentStatus* resource.

    !! kubectl get cs

Display *Node* resource.

    !! kubectl get node

## Delete user pvc

Executing the cell below,

    user_pvcs = !! kubectl get -l component=singleuser-storage  pvc -n hub -o jsonpath='{range.items[*]}{.metadata.name}{"\n"}{end}'
    pvc = ipywidgets.Dropdown(
    	options=user_pvcs,
    	description='Target:',
    	disabled=False,
    )
    pvc

It shows a dropdown list, select user pvc which you want to delete.

![](/img/Untitled-04de7b40-77ce-4259-a225-ea4098074bc8.png)

After selection, executes cell below for deletion.

    def execute():
    	if pvc.value is None:
    		print("No selected PVC")
    		return
    	mounted_by = !! ~/bin/kubectl -n hub describe pvc {pvc.value} | grep -o 'jupyter-.*'
    if mounted_by:
    	print("PVC %s can't be deleted because it's mounted by: %s" % (pvc.value, mounted_by[0]))
    else:result = !! ~/bin/kubectl -n hub delete pvc {pvc.value}
    	print(result)
    
    execute()

## Create pv-type dataset

Executing the cell below,

    pv_type_datasets = !! kubectl -n hub get datasets -o=custom-columns=VOLUME_NAME:spec.volumeName,NAME:metadata.name,TYPE:spec.type | grep -e 'pv$' | grep -v -e '^hostpath:' | awk '{print $1","$2}'
    temp_datasets = {}
    for ds in pv_type_datasets:
    	[volume_name, name] = ds.split(',')
    	temp_datasets[name] = volume_name
    dataset_name = ipywidgets.Dropdown(
    	options=temp_datasets.keys(),
    	description='Target:',
    	disabled=False,
    )
    dataset_name

It shows a dropdown list, select Target where to create dataset.

![](/img/Untitled-fbf85ce4-cd5e-42ce-8b66-aea82388d9e5.png)

Executing the cell below to specify the size of dataset.

    dataset_size = ipywidgets.IntText(description='Size:', value=200)dataset_size

![](/img/Untitled-f1804dff-04c5-4cc3-818d-bc08267db290.png)

Executing the cell below to determine the storage_class

    is_rook_block = !! kubectl get sc | grep rook-block
    storage_class = 'rook-block' if is_rook_block else 'standard'
    
    storage_class

![](/img/Untitled-8fe271b1-dbe6-42fb-8e9e-42d2357671b3.png)

Executing the cell below to prepare specific yaml string.

    dataset_volume = temp_datasets[dataset_name.value]
    pv_type_dataset_yaml_string = '''apiVersion: v1
    	kind: PersistentVolumeClaim
    	metadata:
    		annotations:
    			primehub-group: dataset-%s
    			primehub-group-sc: %s
    		name: dataset-%s
    		namespace: hub
    spec:
    	accessModes:
    	- ReadWriteMany
    	dataSource: null
    	resources:
    		requests:
    			storage: %s
    	selector:
    		matchLabels:
    		primehub-group: 
    		dataset-%s
    		primehub-namespace: hub
    	storageClassName: ''
    ''' % (dataset_volume, storage_class, dataset_volume, str(dataset_size.value)+'Gi', dataset_volume)
    print(pv_type_dataset_yaml_string)

![](/img/Untitled-14734d67-417d-4b23-9573-e2a8e0b7ce08.png)

Executing the cell below to apply the yaml to create the pv-type dataset.

    !! echo "{pv_type_dataset_yaml_string}" | kubectl -n hub apply -f -

![](/img/Untitled-cf5bb3bf-af72-4f2f-befa-70724130d4ef.png)
