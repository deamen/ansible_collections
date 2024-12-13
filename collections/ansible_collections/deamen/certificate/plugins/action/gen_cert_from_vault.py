from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError
from ansible.plugins.loader import connection_loader


class ActionModule(ActionBase):
    supported_sub_module_args = [
        "alt_names",
        "common_name",
        "engine_mount_point",
        "ip_sans",
        "role_name",
        "ttl",
        "url",
        "token",
        "auth_method",
    ]

    def sanitize_params(self, params):
        """
        Filters the task parameters to only include those supported by the 'community.hashi_vault.vault_pki_generate_certificate' module.
        """
        return {k: v for k, v in params.items() if k in self.supported_sub_module_args}

    def validate_params(self, params):
        """
        Validates that all required parameters are present.
        """
        required_params = ["common_name", "engine_mount_point", "role_name", "token"]
        missing_params = [p for p in required_params if p not in params]

        if missing_params:
            raise AnsibleError(f"Missing required parameters: {', '.join(missing_params)}")

    def prepare_module_args(self, params):
        """
        Prepares the arguments for the module execution.
        """
        return {
            "alt_names": params.get("alt_names"),
            "common_name": params["common_name"],
            "engine_mount_point": params["engine_mount_point"],
            "ip_sans": params.get("ip_sans"),
            "role_name": params["role_name"],
            "ttl": params.get("ttl"),
            "url": params.get("vault_addr"),
            "token": params["token"],
            "auth_method": "token",
            "on_target": params.get("on_target", False),
        }

    def run(self, task_vars=None):
        if task_vars is None:
            task_vars = {}

        # Extract and validate parameters
        params = self._task.args
        self.validate_params(params)

        # Prepare module arguments
        module_args = self.prepare_module_args(params)
        sub_module_args = self.sanitize_params(module_args)

        # Save the original connection
        original_connection = self._connection

        try:
            # Set up local connection
            local_connection = connection_loader.get("local", self._play_context)
            local_connection.set_options()  # Set default options for local connection

            # Override the current connection with the local connection if not on target
            if not module_args["on_target"]:
                self._connection = local_connection

            # Execute the module locally
            result = self._execute_module(
                module_name="community.hashi_vault.vault_pki_generate_certificate",
                module_args=sub_module_args,
                task_vars=task_vars,
            )
        finally:
            # Restore the original connection
            self._connection = original_connection

        return result
