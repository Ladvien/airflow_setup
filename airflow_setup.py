import os
import argparse
import subprocess

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

MSG_COLOR_START = "\\033[0;35;40m"
MSG_COLOR_STOP = "\\033[0;0m'"
    
def exec(cmd: str) -> None:
    subprocess.call(cmd)
    
def print(text: str):
    rprint(f"echo '{MSG_COLOR_START}{text}{MSG_COLOR_STOP}'")

################################
# Switch to user dir
################################
exec(f"cd /home/{OS_USER_NAME}")


######################################
# Configure AWS CLI
######################################
exec(f"aws configure set aws_access_key_id {AWS_ACCOUNT_ID}")
exec(f"aws configure set aws_secret_access_key {AWS_SECRET_ACCESS_KEY}")
exec(f"aws configure set region {AWS_REGION}")
exec(f"""echo 'export ACCOUNT_ID={AWS_ACCOUNT_ID}' | tee -a ~/.bash_profile""")
exec(f"""echo 'export AWS_REGION={AWS_REGION}' | tee -a ~/.bash_profile""")

##############################
# Setup virtual Environment
##############################
print(f"Setting up virtual environment: {VIRT_ENV_NAME}")
print(f"Activate with: source .{VIRT_ENV_NAME}/bin/activate")
exec("pip3 install --upgrade pip --user")
exec(f"python3 -m venv .{VIRT_ENV_NAME}")
exec(f"source .{VIRT_ENV_NAME}/bin/activate")

############################################
# Setup eksctl for managing Kubernetes
############################################
print("Installing eksctl")
print("For info visit: https://eksctl.io/")
exec("""curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/0.23.0/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp """)
exec("sudo mv /tmp/eksctl /usr/local/bin")

############################################
# Setup kubectl
############################################
print("Installing kubectl")
print("For info visit: https://kubernetes.io/docs/tasks/tools/")
exec("""sudo curl --silent --location https://storage.googleapis.com/kubernetes-release/release/v1.18.2/bin/linux/amd64/kubectl """)
exec("sudo chmod +x ./kubectl")
exec("sudo mv ./kubectl /usr/local/bin/kubectl")

###################
# Install Helm3
# https://helm.sh/
###################
print("Installing helm")
print("For info visit: https://helm.sh/")
exec("curl -sSL https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash")

print(f"Adding stable Helm repository: {STABLE_HELM_REPO}")
exec(f"helm repo add stable {STABLE_HELM_REPO}")


###################
# Setup git
###################
print(f"Setting git user.name to '{USER_NAME}'")
exec(f"git config --global user.name '{USER_NAME}'")

###################
# Upgrade AWS CLI Tools
###################
print("Upgrading AWS CLI and adding additional tooling.")
exec("pip3 install --upgrade awscli --user && hash -r")
exec("sudo yum -y install jq gettext bash-completion moreutils")
