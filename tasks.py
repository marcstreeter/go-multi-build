from invoke import task

image = 'marcstreeter/commodus-api'

@task
def build(ctx, version):
    # constants
    image_name = f'{image}:v{version}'
    amd_name = f'{image_name}-amd'
    arm_name = f'{image_name}-arm'

    # commands
    build_command = 'docker build --pull -t {image_name}  -f ../Dockerfile.{arch} ..'
    push_command = 'docker push {image_name}'

    for arch_name, arch in ((amd_name, 'amd'), (arm_name, 'arm')):
        print(f'Building Image for {arch}: {arch_name}')
        ctx.run(build_command.format(image_name=arch_name, arch=arch))
        print(f'Pushing Image for {arch}: {arch_name}')
        ctx.run(push_command.format(image_name=arch_name))

    print('Building manifest...')
    ctx.run(f'docker manifest create {image_name} {amd_name} {arm_name}')
    ctx.run(f'docker manifest annotate {image_name} {arm_name} --os linux --arch arm')
    ctx.run(f'docker manifest push {image_name}')
    



