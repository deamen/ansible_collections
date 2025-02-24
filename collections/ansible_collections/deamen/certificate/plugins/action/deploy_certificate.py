from ansible.plugins.action import ActionBase
from ansible.plugins.action.copy import ActionModule as CopyAction


class ActionModule(ActionBase):
    """
    Deploy a certificate and its key using the 'copy' action plugin.
    This action module sanitizes parameters and utilizes the 'copy' plugin
    to deploy certificate and key files with the specified properties.
    """

    SUPPORTED_PARAMS = [
        "_original_basename",
        "attributes",
        "backup",
        "checksum",
        "content",
        "dest",
        "directory_mode",
        "follow",
        "force",
        "group",
        "local_follow",
        "mode",
        "owner",
        "remote_src",
        "selevel",
        "serole",
        "setype",
        "seuser",
        "src",
        "unsafe_writes",
        "validate",
    ]

    DEFAULT_CERT_DIR = "/etc/pki/tls/certs/"
    DEFAULT_KEY_DIR = "/etc/pki/tls/private/"
    DEFAULT_CERT_MODE = "0644"
    DEFAULT_KEY_MODE = "0600"
    DEFAULT_OWNER = "root"
    DEFAULT_GROUP = "root"

    def sanitize_params(self, params):
        """
        Filters the task parameters to only include those supported by the 'copy' module.
        """
        return {k: v for k, v in params.items() if k in self.SUPPORTED_PARAMS}

    def prepare_copy_args(self, dest, content, owner, group, mode):
        """
        Prepares arguments for the 'copy' action.
        """
        return {
            "dest": dest,
            "content": content,
            "owner": owner,
            "group": group,
            "mode": mode,
        }

    def deploy_file(self, copy_action, dest, content, owner, group, mode, tmp, task_vars):
        """
        Deploys a file using the 'copy' action.
        """
        copy_args = self.prepare_copy_args(dest, content, owner, group, mode)
        copy_action._task.args.update(copy_args)
        return copy_action.run(tmp=tmp, task_vars=task_vars)

    def run(self, tmp=None, task_vars=None):
        """
        Main execution method for deploying the certificate and its key.
        """
        params = self._task.args
        is_ca = params.get("is_ca", False)

        # Validate and extract required parameters
        name = params.get("name")
        if not name or (not name.endswith(".crt") and not is_ca):
            return {"failed": True, "msg": "The 'name' parameter must be a valid .crt filename."}

        cert_content = params.get("cert_content")
        key_content = params.get("key_content")
        if not cert_content or (not key_content and not is_ca):
            return {
                "failed": True,
                "msg": "Both 'cert_content' and 'key_content' are required unless 'is_ca' is True.",
            }

        # Extract optional parameters or use defaults
        cert_dir = params.get("cert_dir", self.DEFAULT_CERT_DIR)
        key_dir = params.get("key_dir", self.DEFAULT_KEY_DIR)
        cert_path = f"{cert_dir}/{name}"
        key_path = f"{key_dir}/{name.replace('.crt', '.key')}"

        cert_owner = params.get("cert_owner", self.DEFAULT_OWNER)
        cert_group = params.get("cert_group", self.DEFAULT_GROUP)
        cert_mode = params.get("cert_mode", self.DEFAULT_CERT_MODE)

        key_owner = params.get("key_owner", self.DEFAULT_OWNER)
        key_group = params.get("key_group", self.DEFAULT_GROUP)
        key_mode = params.get("key_mode", self.DEFAULT_KEY_MODE)

        # Sanitize the task parameters
        self._task.args = self.sanitize_params(params)

        # Deploy the certificate file
        cert_result = {"changed": False}
        copy_cert_action = CopyAction(
            self._task,
            self._connection,
            self._play_context,
            self._loader,
            self._templar,
            self._shared_loader_obj,
        )
        cert_result = self.deploy_file(
            copy_cert_action,
            cert_path,
            cert_content,
            cert_owner,
            cert_group,
            cert_mode,
            tmp,
            task_vars,
        )

        key_result = {"changed": False}
        if not is_ca:
            # Deploy the key file
            copy_key_action = CopyAction(
                self._task,
                self._connection,
                self._play_context,
                self._loader,
                self._templar,
                self._shared_loader_obj,
            )
            key_result = self.deploy_file(
                copy_key_action,
                key_path,
                key_content,
                key_owner,
                key_group,
                key_mode,
                tmp,
                task_vars,
            )

        # Combine results
        result = {
            "changed": cert_result.get("changed", False) or key_result.get("changed", False),
            "cert_result": cert_result,
        }

        if not is_ca:
            result["key_result"] = key_result

        return result
