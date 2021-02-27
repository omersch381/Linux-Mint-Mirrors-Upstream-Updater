import docker


def build_docker_file(**build_params):
    """
    Builds an existing docker file.

    Keywords Args:
        https://docker-py.readthedocs.io/en/stable/images.html

    Returns:
        tuple: The first item is the Image object for the image that was build.
                The second item is a generator of the build logs as JSON-decoded objects.
    """
    return docker.from_env().images.build(**build_params)
