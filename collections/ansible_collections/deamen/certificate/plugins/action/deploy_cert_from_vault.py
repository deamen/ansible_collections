from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError
from .gen_cert_from_vault import ActionModule as GenCertFromVaultAction
from .deploy_certificate import ActionModule as DeployCertificateAction


class ActionModule(ActionBase):
    """
    Action plugin to generate a certificate using HashiCorp Vault and deploy it.
    """

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        # Extract parameters
        params = self._task.args
        gen_cert_params = {
            "common_name": params.get("common_name"),
            "engine_mount_point": params.get("engine_mount_point"),
            "role_name": params.get("role_name"),
            "token": params.get("token"),
            "alt_names": params.get("alt_names"),
            "ip_sans": params.get("ip_sans"),
            "ttl": params.get("ttl"),
            "vault_addr": params.get("vault_addr"),
            "on_target": params.get("on_target", False),
        }

        # Validate required parameters for generating certificate
        required_params = ["common_name", "engine_mount_point", "role_name", "token"]
        missing_params = [p for p in required_params if p not in gen_cert_params or not gen_cert_params[p]]
        if missing_params:
            raise AnsibleError(f"Missing required parameters for generating certificate: {', '.join(missing_params)}")

        # Call gen_cert_from_vault action plugin to generate the certificate
        gen_cert_action = GenCertFromVaultAction(
            self._task,
            self._connection,
            self._play_context,
            self._loader,
            self._templar,
            self._shared_loader_obj,
        )
        gen_cert_result = gen_cert_action.run(task_vars=task_vars)

        if gen_cert_result.get("failed"):
            return gen_cert_result

        # Extract certificate and key content from the result
        cert_content = gen_cert_result.get("certificate")
        key_content = gen_cert_result.get("private_key")
        if not cert_content or not key_content:
            return {"failed": True, "msg": "Failed to generate certificate or key from Vault."}

        # Prepare parameters for deploying the certificate
        deploy_cert_params = {
            "name": params.get("name", f"{gen_cert_params['common_name']}.crt"),
            "cert_content": cert_content,
            "key_content": key_content,
            "cert_dir": params.get("cert_dir"),
            "key_dir": params.get("key_dir"),
            "cert_mode": params.get("cert_mode"),
            "key_mode": params.get("key_mode"),
            "cert_owner": params.get("cert_owner"),
            "cert_group": params.get("cert_group"),
            "key_owner": params.get("key_owner"),
            "key_group": params.get("key_group"),
            "is_ca": params.get("is_ca", False),
        }

        # Call deploy_certificate action plugin to deploy the certificate
        deploy_cert_action = DeployCertificateAction(
            self._task,
            self._connection,
            self._play_context,
            self._loader,
            self._templar,
            self._shared_loader_obj,
        )
        deploy_cert_result = deploy_cert_action.run(task_vars=task_vars)

        return deploy_cert_result
