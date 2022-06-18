import click
import psutil
import jinja2


@click.command()
@click.option('--runtime', default='empty', help='Application runtime, example: tomcat')



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
        if app_runtime == proc.environ().values():
            artefact['APP_RUNTIME'] = app_runtime
            artefact['APP_DIR'] = proc.environ()['CATALINA_BASE'] + '/webapps/*.war'
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
    outputText = template.render(artefacts)
    return outputText

if __name__ == '__main__':
    artefacts = dict()
    if runtime == 'empty':
        app_runtime = find_runtime()
        if len(app_runtime) == 1:
            artefacts = get_artefacts(app_runtime[0])
        else:
            print(f'Found multiple application runtimes, pass one in --runtime parameter: {",".join(app_runtime)}')
    else:
        artefacts = get_artefacts(runtime)
    if len(artefacts.keys()) > 0:
        dockerfile = generate_docker_file(artefacts)
        print(dockerfile)
    else:
        print(f"Couldn't find any application running on this server")

