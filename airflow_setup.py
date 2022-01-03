import os
import argparse
from rich import print as rprint

###############
# Parse args
###############
parser = argparse.ArgumentParser()
parser.add_argument('--user', '-u', help="The user name for using workstation.", type= str)
parser.add_argument('--region', '-r', help="AWS region of workstation operations.", type=str)
parser.add_argument('--aws_id', '-i', help="aws_account_id of workstation operations.", type=str)
parser.add_argument('--aws_secret', '-s', help="aws_secrey_access_key of workstation operations.", type=str)

args = parser.parse_args()
OS_USER_NAME = args.user
AWS_ACCOUNT_ID = args.aws_id
AWS_REGION = args.region
AWS_SECRET_ACCESS_KEY = args.aws_secret


###############
# Constants
###############
VIRT_ENV_NAME = "sandbox"
STABLE_HELM_REPO = "https://charts.helm.sh/stable"
USER_NAME = "af_workstation"

MSG_COLOR = "magenta"

def print(text: str):
    rprint(f"[{MSG_COLOR}]{text}[/{MSG_COLOR}]")



######################################
# Configure AWS CLI
######################################
os.system(f"aws configure set aws_access_key_id {AWS_ACCOUNT_ID}")
os.system(f"aws configure set aws_secret_access_key {AWS_SECRET_ACCESS_KEY}")
os.system(f"aws configure set region {AWS_REGION}")
os.system(f"""echo 'export ACCOUNT_ID={AWS_ACCOUNT_ID}' | tee -a ~/.bash_profile""")
os.system(f"""echo 'export AWS_REGION={AWS_REGION}' | tee -a ~/.bash_profile""")

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
os.system("""sudo curl --silent --location https://storage.googleapis.com/kubernetes-release/release/v1.18.2/bin/linux/amd64/kubectl """)
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

###################
# Upgrade AWS CLI Tools
###################
print("Upgrading AWS CLI and adding additional tooling.")
os.system("pip3 install --upgrade awscli --user && hash -r")
os.system("sudo yum -y install jq gettext bash-completion moreutils")
