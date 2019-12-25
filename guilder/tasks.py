from pathlib import Path
from invoke import task

ARCH_DUMB_MAP = {
    'arm/v7': 'arm',
    'arm64/v8': 'arm64',
    'amd64': 'amd64',
    #arch: #label
}

# from https://github.com/docker/cli/blob/ba63a92655c0bea4857b8d6cc4991498858b3c60/cli/command/manifest/util.go#L22
VALID_MANIFEST_ARCH = {
    'amd': "386",
	'amd64': "amd64",
	'arm/v7': "arm",
	'arm64/v8': "arm64",
	# '': "ppc64le",
	# '': "mips64",
	# '': "mips64le",
	# '': "riscv64",
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
    image_base_name = f'{user}/{name}'
    arch_names = architectures.replace(' ','').split(',')
    _separate_builds(ctx, image_base_name, image_version, *arch_names)

# I may be able to do this once I have multiple machines available to me
# def _unified_build(ctx, image_base_name, *architectures):
#     build_command = f'docker buildx build -t {image_base_name} --platform linux/{arch} --push .'
#     push_command = f'docker push {image_base_name}';
#     platforms = ','.join(f'linux/{arch}' for arch in architectures)
#     ctx.run(build_command.format(platforms=platforms))
#     ctx.run(push_command)

def _separate_builds(ctx, image_base_name, image_version, *architectures):
    build_command = 'docker build --pull --platform=linux/{architecture} -t {image_name} -f {dockerfile_name} .'
    push_command = 'docker push {image_name}'
    platforms = []
    image_master_name = f'{image_base_name}:{image_version}'

    print('Building images...')

    for architecture in architectures:
        arch_suffix = ARCH_DUMB_MAP[architecture]
        dockerfile_name = f'Dockerfile.{arch_suffix}'
        image_name = f'{image_base_name}:{arch_suffix}-{image_version}'

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
    manifest_create_cmd = f'docker manifest create {image_master_name} {image_names}'
    print(f'💥Building manifest: {manifest_create_cmd}')
    ctx.run(manifest_create_cmd)

    for platform in platforms:
        image_operating_system = platform['operating_system']
        image_name = platform['image_name']
        image_architecture = VALID_MANIFEST_ARCH[platform['architecture']]
        manifest_annotate_cmd = f'docker manifest annotate {image_master_name} {image_name} --arch {image_architecture} --os {image_operating_system}'
        print(f'💥Annotating manifest: {manifest_annotate_cmd}')
        ctx.run(manifest_annotate_cmd)

    manifest_inspect_cmd = f'docker manifest inspect {image_master_name}'
    print(f'💥Inspecting manifest: {manifest_inspect_cmd}')
    ctx.run(manifest_inspect_cmd)
    manifest_push_cmd = f'docker manifest push {image_master_name}'
    print(f'💥Pushing manifest: {manifest_push_cmd}')
    ctx.run(manifest_push_cmd)
