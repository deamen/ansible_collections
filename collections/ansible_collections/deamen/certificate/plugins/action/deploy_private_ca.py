from ansible.plugins.action import ActionBase
from .deploy_certificate import ActionModule as DeployCertificateAction


class ActionModule(ActionBase):
    """
    Action plugin for deploy_private_ca that reuses the deploy_certificate plugin.
    """

    def run(self, tmp=None, task_vars=None):
        # Extract parameters passed to the task
        private_ca = self._task.args.get("private_ca")
        filename = self._task.args.get("filename", "custom-ca.crt")

        # Debug output for filename
        self._display.v(f"Filename: {filename}")

        # Validate required parameters
        if not private_ca:
            return {"failed": True, "msg": "'private_ca' parameter is required."}

        # Define parameters for the deploy_certificate plugin
        ca_trust_dir = "/etc/pki/ca-trust/source/anchors/"
        deploy_certificate_args = {
            "name": filename,
            "cert_content": private_ca,
            "cert_dir": ca_trust_dir,
            "cert_owner": "root",
            "cert_group": "root",
            "cert_mode": "0644",
            "is_ca": True,
        }

        # Update task arguments with deploy_certificate parameters
        self._task.args.update(deploy_certificate_args)

        # Invoke the deploy_certificate action plugin
        deploy_certificate_action = DeployCertificateAction(
            self._task,
            self._connection,
            self._play_context,
            self._loader,
            self._templar,
            self._shared_loader_obj,
        )
        result = deploy_certificate_action.run(
            tmp=tmp, task_vars={**task_vars, **deploy_certificate_args}
        )

        # Execute the update-ca-trust command using a module
        module_result = self._execute_module(
            module_name=self._task.action,
            module_args={},
            task_vars=task_vars,
        )

        # Merge the results from deploy_certificate and update-ca-trust
        result.update(module_result)

        return result
