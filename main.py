import time, os

import pykube
from urllib3.exceptions import ProtocolError
from requests.exceptions import ConnectionError as ReqConnectionError

NODENAME = os.environ.get("NODENAME")
KUBECONFIG = os.environ.get("KUBECONFIG", "~/.kube/config")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "60"))

def main():
  if NODENAME is None:
    raise Exception("NODENAME cannot be None")

  api = pykube.HTTPClient(pykube.KubeConfig.from_file(KUBECONFIG))

  print("Der node doktor ist in für %s, checkup every %s seconds..." % (NODENAME, POLL_INTERVAL))

  while True:
    try:
      found_bad_pods = False

      for pod in pykube.Pod.objects(api).filter(field_selector={"spec.nodeName": NODENAME}):
        for pod_event in pykube.Event.objects(api).filter(field_selector={"involvedObject.name": pod.obj['metadata']['name']}):
          if 'rpc error' in pod_event.obj['message']:
            pod.delete()
            found_bad_pods = True
            break

      if found_bad_pods:
        print("Found bad pods.  Cordoning node...")
        pykube.Node.objects(api).get(name=NODENAME).cordon()

    except (ProtocolError, ConnectionResetError, ConnectionError, ReqConnectionError):
      print("Connection reset...")

    time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
  main()
