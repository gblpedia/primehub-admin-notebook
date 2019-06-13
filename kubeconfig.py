import subprocess
import tempfile
import ipywidgets
import os


class KubeConfig:
    def __init__(self):
        self.kubectl = '/home/jovyan/bin/kubectl'
        self.kubeconfig = None

    def _get_cluster_info(self):
        output = subprocess.run(
            [self.kubectl, "cluster-info"], capture_output=True)
        return output.stdout.decode().split('\n')[0]

    def test(self):
        if not self._get_cluster_info():
            self.kubeconfig = ipywidgets.Textarea(
                description='kubeconfig:',
                placeholder='kubectl config view --raw --minify | pbcopy',
                layout=ipywidgets.Layout(
                    width='95%',
                    height='100px'))
        return self.kubeconfig

    def setup(self):
        cluster_info = self._get_cluster_info()
        if not self.kubeconfig:
            print(cluster_info)
            return ipywidgets.Valid(value=True, description='Use existing service account.', style={
                                    'description_width': 'auto'}, layout=ipywidgets.Layout(width='100%'))
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(bytearray(self.kubeconfig.value, 'utf-8'))
        temp.close()
        os.environ['KUBECONFIG'] = temp.name
        if not cluster_info:
            return ipywidgets.Valid(value=False, description='kubeconfig')
        print(cluster_info)
        return ipywidgets.Valid(value=True, description='kubeconfig')
