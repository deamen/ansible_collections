from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        # Initialize task variables
        if task_vars is None:
            task_vars = {}

        # Extract user-supplied parameters
        params = self._task.args

        required_params = ["common_name", "engine_mount_point", "role_name", "token"]
        missing_params = [p for p in required_params if p not in params]

        if missing_params:
            raise AnsibleError(f"Missing required parameters: {', '.join(missing_params)}")

        # Set default parameters for the module
        module_args = {
            "alt_names": params.get("alt_names"),
            "common_name": params["common_name"],
            "engine_mount_point": params["engine_mount_point"],
            "ip_sans": params.get("ip_sans"),
            "role_name": params["role_name"],
            "ttl": params.get("ttl"),
            "url": params.get("vault_addr"),
            "token": params["token"],
            "auth_mode": "token",
        }

        # Call the community.hashi_vault.vault_pki_generate_certificate module
        result = self._execute_module(
            module_name="community.hashi_vault.vault_pki_generate_certificate",
            module_args=module_args,
            task_vars=task_vars,
            delegate_to="localhost",
        )

        return result
