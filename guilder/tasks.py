from pathlib import Path
from invoke import task

ARCH_DUMB_MAP = {
    'arm/v7': 'arm',
    'arm64/v8': 'arm64',
    'amd64': 'amd64',
}

@task(
    default=True,
    help={
        'name': 'Name of image',
        'version': 'Version of image',
        'user': 'Docker user account namespace',
        'architectures': 'Architecture(s) for which the image will be built'
    }
)
def build(ctx, name, version='', user='marcstreeter', architectures='amd64,arm/v7,arm64/v8'):
    # constants
    image_version = f'v{version}' if version else 'latest'
    image_base_name = f'{user}/{name}:{image_version}'
    arch_names = architectures.replace(' ','').split(',')
    _separate_builds(ctx, image_base_name, *arch_names)


def _separate_builds(ctx, image_base_name, *architectures):
    build_command = 'docker build --pull --platform=linux/{architecture} -t {image_name} -f {dockerfile_name} .'
    push_command = 'docker push {image_name}'
    platforms = []

    print('Building images...')

    for architecture in architectures:
        arch_suffix = ARCH_DUMB_MAP[architecture]
        dockerfile_name = f'Dockerfile.{arch_suffix}'
        image_name = f'{image_base_name}-{arch_suffix}'

        if not Path.exists(Path.cwd() / dockerfile_name):
            print(f"Dockerfile, '{dockerfile_name}', not found. Skipping")
            continue

        rendered_build_command = build_command.format(
            architecture=architecture,
            image_name=image_name,
            dockerfile_name=dockerfile_name)
        print(f'💥Building Image: {rendered_build_command}')
        ctx.run(rendered_build_command)
        platforms.append({
            'architecture': architecture,
            'operating_system': 'linux',
            'image_name': image_name,
        })
    
    print('Pushing images...')

    for platform in platforms:
        image_name = platform['image_name']
        rendered_push_command = push_command.format(image_name=image_name)
        print(f'\t\t\t💥Pushing image: {rendered_push_command}')
        ctx.run(rendered_push_command)

    image_names = ' '.join(platform['image_name'] for platform in platforms)
    manifest_create_cmd = f'docker manifest create {image_base_name} {image_names} --amend'
    print(f'💥Building manifest: {manifest_create_cmd}')
    ctx.run(manifest_create_cmd)
    manifest_inspect_cmd = f'docker manifest inspect {image_base_name}'
    print(f'💥Inspecting manifest: {manifest_inspect_cmd}')
    ctx.run(manifest_inspect_cmd)
    manifest_push_cmd = f'docker manifest push {image_base_name}'
    print(f'💥Pushing manifest: {manifest_push_cmd}')
    ctx.run(manifest_push_cmd)
