from ansible.plugins.action import ActionBase
from .deploy_certificate import ActionModule as DeployCertificateAction


class ActionModule(ActionBase):
    """
    Action plugin for deploy_private_ca that reuses the deploy_certificate plugin.
    """

    def run(self, task_vars=None):
        # Extract parameters passed to the task
        private_ca = self._task.args.get("private_ca")
        filename = self._task.args.get("filename", "custom-ca.crt")
        ca_trust_dir = self._task.args.get("ca_trust_dir", "/etc/pki/ca-trust/source/anchors/")
        update_ca_command = self._task.args.get("update_ca_command", "update-ca-trust")

        # Validate required parameters
        if not private_ca:
            return {"failed": True, "msg": "'private_ca' parameter is required."}

        # Define parameters for the deploy_certificate plugin
        deploy_certificate_args = {
            "name": filename,
            "cert_content": private_ca,
            "cert_dir": ca_trust_dir,
            "cert_owner": "root",
            "cert_group": "root",
            "cert_mode": "0644",
            "is_ca": True,
            "update_ca_command": update_ca_command,
        }

        # Update task arguments with deploy_certificate parameters
        self._task.args.update(deploy_certificate_args)
        new_module_args = self._task.args.copy()

        # Invoke the deploy_certificate action plugin
        deploy_certificate_action = DeployCertificateAction(
            self._task,
            self._connection,
            self._play_context,
            self._loader,
            self._templar,
            self._shared_loader_obj,
        )
        result = deploy_certificate_action.run(task_vars=task_vars)

        # Execute the module to run update-ca-trust command
        module_result = self._execute_module(
            module_name=self._task.action,
            module_args={k: v for k, v in new_module_args.items() if k == "update_ca_command"},
            task_vars=task_vars,
        )

        # Merge the results from deploy_certificate and module
        result.update(module_result)

        # Only if cert_result changed, set changed to True
        if result.get("cert_result", {}).get("changed"):
            result["changed"] = True
        else:
            result["changed"] = False

        return result
