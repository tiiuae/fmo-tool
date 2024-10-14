#!/bin/python3

import os
import yaml
import argparse

DOCKER_COMPOSE_FILE = 'docker-compose.yml'
OUT_DIR = 'dimage'
CONTAINERS_DIR = 'containers'
CONF_NAME = 'image_conf.yaml'
IMAGE = 'dimage.img'
LABEL = 'fmoos-containers'

CLEARIFY = [OUT_DIR, IMAGE]

def verify(args):

    if args.c:
        for p in CLEARIFY:
            cmd = f"rm -rf {p}"
            print(cmd)
            os.system(cmd)
        exit(0)


    try:
        open(DOCKER_COMPOSE_FILE)
    except FileNotFoundError:
        print(f"{DOCKER_COMPOSE_FILE} has not been found.. exit")
        exit(-1)


    if not args.d:
        for p in CLEARIFY:
            if os.path.exists(p):
                print(f"{p} is already exist.. use -c to clear. exit")
                exit(-1)

        path = os.path.join(OUT_DIR, CONTAINERS_DIR)
        os.system(f"mkdir -p {path}")

def main(args):
    verify(args)

    with open(DOCKER_COMPOSE_FILE) as f:
        print('='*10, "docker-compose pull", '='*10)
        os.system("docker-compose pull")

        data = yaml.safe_load(f)
        serv = data['services']
        imgs = [serv[name]['image'] for name in serv]

        containers = []
        print('='*10, "store containers", '='*10)
        for img in imgs:
            name = img.split(':')[0].split('/')[-1]
            name = f"{name}.tar.gz"
            path = os.path.join(OUT_DIR, CONTAINERS_DIR, name)
            cmd = f"docker save -o {path} {img}"

            print(cmd)
            if not args.d:
                os.system(cmd)

            containers.append(name)

        config = {'containers': containers}

        print('='*10, "store config", '='*10)
        print(yaml.dump(config))
        if not args.d:
            with open(os.path.join(OUT_DIR, CONF_NAME), 'w') as f:
                yaml.dump(config, f)
        if not args.d:
            with open(os.path.join(OUT_DIR, "containers.list"), 'w') as f:
                f.write("\n".join(containers))

        if args.d:
            return

        print('='*10, "store docker-compose", '='*10)
        os.system(f"cp docker-compose.yml {OUT_DIR}")

        print('='*10, "store leaf.conf", '='*10)
        os.system(f"cp leaf.conf {OUT_DIR}")

        print('='*10, "create an image", '='*10)
        os.system(f"truncate -s 20G {IMAGE}")
        os.system(f"mkfs.ext4 {IMAGE} -L {LABEL}")
        os.system(f"mkdir ./mnt")
        os.system(f"sudo mount {IMAGE} ./mnt")
        os.system(f"sudo cp -r {OUT_DIR}/* ./mnt")
        os.system(f"sudo umount ./mnt")
        os.system(f"rm -rf ./mnt")
        os.system(f"e2fsck -fy {IMAGE}")
        os.system(f"resize2fs -M {IMAGE}")

        print('='*10, "done", '='*10)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare pre-uploaded containers for FMO-OS')
    parser.add_argument('-d', action='store_true', help='dry run')
    parser.add_argument('-c', action='store_true', help='clear')

    args = parser.parse_args()
    main(args)
