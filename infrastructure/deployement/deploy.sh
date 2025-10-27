#!/bin/bash
set -e

VM_IP=$1
SSH_USER="debian"
SSH_KEY="~/.ssh/id_rsa"
REMOTE_PATH="/opt/app"

if [ -z "$VM_IP" ]; then
  echo "Usage: ./deploy.sh <VM_IP>"
  exit 1
fi

echo "Connecting to $VM_IP..."

ssh -i "$SSH_KEY" "$SSH_USER@$VM_IP" "sudo mkdir -p $REMOTE_PATH && sudo chown \$USER $REMOTE_PATH"
scp -i "$SSH_KEY" ../compose-prod.yml "$SSH_USER@$VM_IP:$REMOTE_PATH/docker-compose.yml"
scp -i "$SSH_KEY" ../app.service "$SSH_USER@$VM_IP:/tmp/app.service"

ssh -i "$SSH_KEY" "$SSH_USER@$VM_IP" <<'EOF'
  set -e
  sudo gcloud auth configure-docker us-east1-docker.pkg.dev --quiet
  sudo mv /tmp/app.service /etc/systemd/system/app.service
  sudo systemctl daemon-reload
  sudo systemctl enable app.service
  sudo systemctl start app.service
EOF

echo "Deployment to $VM_IP completed."
