import click
import psutil
import jinja2
from glob import glob
import os
import shutil

def find_runtime():
    """Find the application runtime running on this server"""
    app_runtimes = []
    for proc in psutil.process_iter():
        if "tomcat" in proc.environ().values():
            app_runtimes.append("tomcat")
        elif "apache2" in proc.environ().values():
            app_runtimes.append("apache2")
    return app_runtimes


def get_artefacts(app_runtime):
    """Get application related environment variable and configurations"""
    artefact = dict()
    for proc in psutil.process_iter():
        if app_runtime in proc.environ().values():
            artefact['APP_RUNTIME'] = app_runtime
            war_files = glob(proc.environ()['CATALINA_BASE'] + '/webapps/*.war')
            artefact['APP_DIR'] = war_files
            artefact['APP_CONFIG'] = proc.environ()['CATALINA_BASE'] + '/conf/tomcat-users.xml'
            for conn in proc.connections():
                if conn.laddr.port == 8005:
                    continue
                else:
                    artefact['APP_PORT'] = conn.laddr.port
    return artefact

def generate_docker_file(artefacts):
    templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    if artefacts['APP_RUNTIME'] == "tomcat":
        TEMPLATE_FILE = "Dockerfile-tomcat.j2"
    template = templateEnv.get_template(TEMPLATE_FILE)
    output_dir = './artefact'
    isExist = os.path.exists(output_dir)
    if not isExist:
        os.makedirs(output_dir)
    artefact_paths = []
    for artefact in artefacts['APP_DIR']:
        dst = output_dir+'/'+artefact.split('/')[-1]
        shutil.copyfile(artefact, dst)
        artefact_paths.append(dst)
    dst = output_dir+'/'+artefacts['APP_CONFIG'].split('/')[-1]
    shutil.copyfile(artefacts['APP_CONFIG'], dst)
    artefacts['APP_CONFIG'] = dst
    artefacts['APP_DIR'] = artefact_paths
    outputText = template.render(artefacts=artefacts)
    return outputText

@click.command()
@click.option('--runtime', default='empty', help='Application runtime, example: tomcat')
def build_dockerfile(runtime):
    artefacts = dict()
    if runtime == 'empty':
        app_runtime = find_runtime()
        if len(app_runtime) == 1:
            artefacts = get_artefacts(app_runtime[0])
        elif len(app_runtime) > 1:
            print(f'Found multiple application runtimes, pass one in --runtime parameter: {",".join(app_runtime)}')
    else:
        artefacts = get_artefacts(runtime)
    if len(artefacts.keys()) > 0:
        print(artefacts)
        dockerfile = generate_docker_file(artefacts)
        with open('Dockerfile', 'w') as f:
            f.write(dockerfile)
        print(f"Generated Dockerfile")
    else:
        print(f"Couldn't find any application running on this server")

if __name__ == '__main__':
    build_dockerfile()

