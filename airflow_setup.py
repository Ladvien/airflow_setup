import os
from rich import print

###############
# Constants
###############
VIRT_ENV_NAME = "sandbox"
STABLE_HELM_REPO = "https://charts.helm.sh/stable"
USER_NAME = "af_workstation"

##############################
# Setup virtual Environment
##############################
print(f"Setting up virtual environment: {VIRT_ENV_NAME}")
print(f"Activate with: source .{VIRT_ENV_NAME}/bin/activate")
os.system("pip3 install --upgrade pip --user")
os.system(f"python3 -m venv .{VIRT_ENV_NAME}")
os.system(f"source .{VIRT_ENV_NAME}/bin/activate")

############################################
# Setup eksctl for managing Kubernetes
############################################
print("Installing eksctl")
print("For info visit: https://eksctl.io/")
os.system("""curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/0.23.0/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp """)
os.system("sudo mv /tmp/eksctl /usr/local/bin")

############################################
# Setup kubectl
############################################
print("Installing kubectl")
print("For info visit: https://kubernetes.io/docs/tasks/tools/")
os.system("""curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.18.2/bin/linux/amd64/kubectl """)
os.system("sudo chmod +x ./kubectl")
os.system("sudo mv ./kubectl /usr/local/bin/kubectl")

###################
# Install Helm3
# https://helm.sh/
###################
print("Installing helm")
print("For info visit: https://helm.sh/")
os.system("curl -sSL https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash")

print(f"Adding stable Helm repository: {STABLE_HELM_REPO}")
os.system(f"helm repo add stable {STABLE_HELM_REPO}")


###################
# Setup git
###################
print(f"Setting git user.name to '{USER_NAME}'")
os.system(f"git config --global user.name '{USER_NAME}'")